import json
import re
import requests
from flask import current_app


class AIError(Exception):
    pass


SYSTEM_PROMPT = (
    "You are an AI career guidance assistant for school students.\n"
    "You are given a student's profile and a list of available opportunities.\n\n"
    "RULES:\n"
    "1. Recommend only opportunities that genuinely match the student's interests, subjects, "
    "achievements, or goals. Two strong matches are better than six weak ones.\n"
    "2. If there are no suitable opportunities in the list, return an empty recommendations "
    "array and explain in the gap field what types of opportunities are missing.\n"
    "3. Check the 'Who it's for' field carefully. Do not recommend opportunities that the "
    "student is not eligible for based on age, grade, or citizenship.\n"
    "4. In reason, always mention a specific detail from the student's profile. "
    "Do not use generic phrases like 'this will help you develop.'\n"
    "5. The score should be from 0-100. Use the full range: 90+ means an excellent match, "
    "70-89 means a strong connection, and 50-69 means a related area. Do not include scores below 50.\n\n"
    "Respond ONLY with valid JSON without markdown:\n"
    '{"recommendations": [{"opportunity_id": <int>, "score": <int 0-100>, '
    '"reason": "<1-2 sentences in English referring to the profile>"}], '
    '"gap": "<string or null>"}\n'
    "Include 0 to 6 options, sorted by score from highest to lowest."
)


def build_user_prompt(profile, opportunities):
    profile_dict = dict(profile) if profile else {}
    
    profile_text = (
        f"Name: {profile_dict.get('full_name') or 'not provided'}\n"
        f"Grade/Course: {profile_dict.get('grade') or 'not provided'}\n"
        f"Strong subjects: {profile_dict.get('subjects') or 'not provided'}\n"
        f"Interests and hobbies: {profile_dict.get('interests') or 'not provided'}\n"
        f"Achievements: {profile_dict.get('achievements') or 'not provided'}\n"
        f"Career goal: {profile_dict.get('career_goal') or 'not provided'}\n"
    )

    options_text = "\n\n".join(
        f"id={o['id']}\n"
        f"Name: {o['title']}\n"
        f"Category: {o['category']}\n"
        f"Description: {o['description']}\n"
        f"Who it's for: {o['audience']}\n"
        f"Deadline: {o['deadline']}"
        for o in opportunities
    )

    return (
        f"STUDENT PROFILE:\n{profile_text}\n"
        f"AVAILABLE OPPORTUNITIES ({len(opportunities)} total):\n{options_text}\n\n"
        "Return JSON using the specified format."
    )


def extract_json(text):
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise AIError("The AI returned a response that was not valid JSON format.")

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise AIError(f"Failed to parse JSON from AI response: {e}")


def get_ai_recommendations(profile, opportunities):
    api_key = current_app.config.get("BOTHUB_API_KEY")
    if not api_key:
        raise AIError("AI recommendations are not configured. The API token is missing.")

    base_url = current_app.config["BOTHUB_BASE_URL"].rstrip("/")
    model = current_app.config["BOTHUB_MODEL"]

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(profile, opportunities)},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
    except requests.RequestException as error:
        raise AIError(f"Could not connect to BotHub service: {error}")

    if response.status_code != 200:
        raise AIError(f"BotHub returned error status {response.status_code}: {response.text[:300]}")

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed_response = extract_json(content)
        recommendations = parsed_response.get("recommendations", [])
        gap = parsed_response.get("gap")
    except (KeyError, IndexError, TypeError) as error:
        raise AIError(f"Could not process the structure of the AI response: {error}")

    valid_ids = {o["id"] for o in opportunities}
    cleaned_recommendations = []

    for item in recommendations:
        try:
            opp_id = int(item["opportunity_id"])
            score = int(item["score"])
        except (ValueError, TypeError, KeyError):
            continue

        if opp_id not in valid_ids or score < 50:
            continue

        cleaned_recommendations.append({
            "opportunity_id": opp_id,
            "score": max(0, min(100, score)),
            "reason": str(item.get("reason", "")).strip()[:500],
        })

    cleaned_recommendations.sort(key=lambda x: x["score"], reverse=True)

    return {"recommendations": cleaned_recommendations, "gap": gap}