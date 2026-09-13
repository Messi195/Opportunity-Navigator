Opportunity Navigator

Opportunity Navigator is a Flask web app that helps students discover opportunities that match their interests, skills, achievements, and career goals.

Features

🔐 Student registration and login

👤 Student profile with interests, strengths, achievements, and career goals

🎯 Personalized opportunity recommendations

🤖 AI-powered matching and career guidance

📚 Opportunity discovery for scholarships, competitions, internships, volunteering, and mentorship

🗄️ SQLite database for storing users, profiles, and opportunities

🎨 Clean, responsive web interface

Tech Stack

Python

Flask

SQLite

HTML / CSS

Jinja2

AI API integration

python-dotenv

Project Structure

diploy/
├── app.py
├── ai.py
├── auth.py
├── db.py
├── schema.sql
├── requiremts.txt
├── .env
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── landing.html
    ├── dashboard.html
    ├── opportunities.html
    ├── profile_edit.html
    └── auth/
        ├── login.html
        └── register.html

Getting Started

1. Clone the project

git clone <your-repository-url>
cd diploy

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

3. Install dependencies

pip install -r requiremts.txt

4. Configure environment variables

Create a .env file and add your AI API configuration.

Example:

SECRET_KEY=your_secret_key
BOTHUB_API_KEY=your_api_key

Never commit real API keys or other secrets to GitHub.

5. Initialize the database

Use the provided schema.sql to create the required SQLite tables.

6. Run the app

python app.py

Then open the local address shown by Flask in your browser.

How It Works

A student creates an account.

The student completes their profile.

Opportunity Navigator uses the profile information to understand the student's goals and interests.

The AI system helps match the student with relevant opportunities.

Recommended opportunities are displayed through the dashboard.

Configuration

Keep private configuration such as API keys and secret keys inside .env.

For production, use a strong secret key and configure environment variables through your hosting provider instead of committing .env to the repository.

Future Improvements

Add more opportunity sources

Add filters by deadline, category, and eligibility

Add saved opportunities

Add email notifications for deadlines

Improve AI recommendation accuracy

Add student progress tracking

Deploy the application online

License

This project is for educational and personal development purposes.
