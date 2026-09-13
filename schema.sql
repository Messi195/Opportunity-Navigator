CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL DEFAULT '',
    grade TEXT NOT NULL DEFAULT '',
    subjects TEXT NOT NULL DEFAULT '',
    interests TEXT NOT NULL DEFAULT '',
    achievements TEXT NOT NULL DEFAULT '',
    career_goal TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))

);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    audience TEXT NOT NULL,
    deadline TEXT NOT NULL,
    link TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    opportunity_id INTEGER NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    score INTEGER NOT NULL, 
    reason TEXT NOT NULL DEFAULT '', 
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
); 



CREATE INDEX IF NOT EXISTS idx_recommendations_user ON  recommendations(user_id);