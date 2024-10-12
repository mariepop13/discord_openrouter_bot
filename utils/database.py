import sqlite3
import logging

def setup_database():
    conn = sqlite3.connect('bot_database.sqlite')
    cursor = conn.cursor()

    # Create messages table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            model TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create comments table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create personalization table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personalization (
            user_id INTEGER PRIMARY KEY,
            personality TEXT,
            tone TEXT,
            language TEXT,
            ai_model TEXT,
            max_output INTEGER
        )
    ''')

    conn.commit()
    
    # Run database migrations
    run_migrations(cursor)
    
    conn.commit()
    return conn, cursor

def run_migrations(cursor):
    # Check if ai_model column exists in personalization table
    cursor.execute("PRAGMA table_info(personalization)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'ai_model' not in columns:
        logging.info("Adding ai_model column to personalization table")
        cursor.execute("ALTER TABLE personalization ADD COLUMN ai_model TEXT")
    
    if 'max_output' not in columns:
        logging.info("Adding max_output column to personalization table")
        cursor.execute("ALTER TABLE personalization ADD COLUMN max_output INTEGER")

def insert_message(cursor, user_id, content, model):
    cursor.execute('INSERT INTO messages (user_id, content, model) VALUES (?, ?, ?)', (user_id, content, model))

def get_personalization(cursor, user_id):
    cursor.execute('SELECT personality, tone, language, ai_model, max_output FROM personalization WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

def set_personalization(cursor, user_id, field, value):
    cursor.execute(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)', (user_id, value))

def get_ai_preferences(cursor, user_id):
    cursor.execute('SELECT ai_model, max_output FROM personalization WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result if result else ("google/gemini-flash-1.5", 150)  # Default values if not set

def set_ai_preferences(cursor, user_id, ai_model=None, max_output=None):
    cursor.execute('INSERT OR REPLACE INTO personalization (user_id, ai_model, max_output) VALUES (?, ?, ?)',
                   (user_id, ai_model, max_output))

def get_history(cursor, user_id, limit):
    cursor.execute('SELECT content, model FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', (user_id, limit))
    return cursor.fetchall()

def clear_user_history(cursor, user_id):
    cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
    return cursor.rowcount  # Return the number of rows affected
