import sqlite3

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
            language TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def insert_message(cursor, user_id, content, model):
    cursor.execute('INSERT INTO messages (user_id, content, model) VALUES (?, ?, ?)', (user_id, content, model))

def get_personalization(cursor, user_id):
    cursor.execute('SELECT personality, tone, language FROM personalization WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

def set_personalization(cursor, user_id, field, value):
    cursor.execute(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)', (user_id, value))

def get_history(cursor, user_id, limit):
    cursor.execute('SELECT content, model FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', (user_id, limit))
    return cursor.fetchall()

def clear_user_history(cursor, user_id):
    cursor.execute('DELETE FROM messages WHERE user_id = ?', (user_id,))
    return cursor.rowcount  # Return the number of rows affected
