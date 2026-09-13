import os 
from flask import Flask, render_template, request, redirect, url_for, flash, g
from dotenv import load_dotenv
from db import get_db, init_db
import auth
from auth import login_required
from ai import get_ai_recommendations, AIError

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_only")
    app.config["DATABASE_PATH"] = os.environ.get("DATABASE_PATH", "talant.db")
    app.config["BOTHUB_API_KEY"] = os.environ.get("BOTHUB_API_KEY", "")
    app.config["BOTHUB_BASE_URL"] = os.environ.get("BOTHUB_BASE_URL", "https://bothub.chat/api/v2/openai/v1")
    app.config["BOTHUB_MODEL"] = os.environ.get("BOTHUB_MODEL", "gpt-4o-mini")

    init_db(app)
    app.register_blueprint(auth.bp)

    CATEGORY_LABELS = {
        'stipend': 'Scholarship',
        'contest': 'Contest / Olympiad',
        'internship': 'Internship',
        'volunteer': 'Volunteering',
        'mentor': 'Mentorship',
        'community': 'Community',
        'course': 'Course',
    } 
    app.jinja_env.globals['CATEGORY_LABELS'] = CATEGORY_LABELS

    @app.route('/')
    def landing():
        if g.user:
            return redirect(url_for('dashboard'))
        return render_template('landing.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        db = get_db()
        profile = db.execute(
            "SELECT * FROM profiles WHERE user_id = ?", (g.user['id'],)
        ).fetchone()
        recs = db.execute(
            """
            SELECT r.*, o.title, o.category, o.description, o.deadline, o.link
            FROM recommendations r
            JOIN opportunities o ON o.id = r.opportunity_id
            WHERE r.user_id = ?
            ORDER BY r.score DESC, r.created_at DESC
            """,
            (g.user['id'],)
        ).fetchall()
        profile_filled = any([
            profile['subjects'], profile['interests'],
            profile['achievements'], profile['career_goal'],
        ])
        return render_template(
            'dashboard.html', profile=profile, recs=recs, profile_filled=profile_filled
        )

    @app.route('/profile', methods=('GET', 'POST'))
    @login_required
    def profile_edit():
        db = get_db()

        if request.method == 'POST':
            fields = (
                request.form.get('full_name', '').strip(),
                request.form.get('grade', '').strip(),
                request.form.get('subjects', '').strip(),
                request.form.get('interests', '').strip(),
                request.form.get('achievements', '').strip(),
                request.form.get('career_goal', '').strip(),
                g.user['id']
            )

            db.execute(
                """
                UPDATE profiles
                SET full_name=?, grade=?, subjects=?, interests=?,
                    achievements=?, career_goal=?, updated_at=datetime('now')
                WHERE user_id=?
                """,
                fields
            )

            db.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for("dashboard"))
            
        profile = db.execute(
            "SELECT * FROM profiles WHERE user_id = ?", (g.user['id'],)
        ).fetchone()

        return render_template('profile_edit.html', profile=profile)
    
    @app.route("/recommendations/generate", methods=("POST",))
    @login_required
    def generate_recommendations():
        db = get_db()
        profile = db.execute(
            "SELECT * FROM profiles WHERE user_id = ?", (g.user['id'],)
        ).fetchone()
        opportunities = db.execute("SELECT * FROM opportunities").fetchall()
        
        try:
            result = get_ai_recommendations(profile, opportunities)
        except AIError as e:
            flash(str(e), "error")
            return redirect(url_for('dashboard'))

        recs = result["recommendations"]
        gap = result.get("gap")

        db.execute('DELETE FROM recommendations WHERE user_id = ?', (g.user['id'],))

        if not recs:
            db.commit()
            flash(
                gap or "The AI could not find suitable opportunities for your profile. Try describing your interests in more detail.",
                "error",
            )
            return redirect(url_for('dashboard'))

        db.executemany(
            """
                INSERT INTO recommendations (user_id, opportunity_id, score, reason)
                VALUES (?, ?, ?, ?)
            """,
            [(g.user['id'], r['opportunity_id'], r['score'], r['reason']) for r in recs],
        )
        db.commit()
        flash(f'Successfully matched options: {len(recs)}', 'success')
        return redirect(url_for('dashboard')) 

    @app.route('/opportunities')
    @login_required
    def opportunities():
        db = get_db()
        category = request.args.get("category", "")
        if category:
            rows = db.execute(
                "SELECT * FROM opportunities WHERE category = ? ORDER BY title",
                (category,),
            ).fetchall()
        else:
            rows = db.execute('SELECT * FROM opportunities ORDER BY title').fetchall()

        return render_template(
            'opportunities.html', opportunities=rows, active_category=category
        )
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)