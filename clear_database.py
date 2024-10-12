import sqlite3
import os

DATABASE_NAME = 'bot_database.db'

def clear_database():
    # Remove the existing database file
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    
    # Create a new connection (this will create a new empty database file)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Recreate the tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            model TEXT,
            message_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS personalization (
            user_id INTEGER PRIMARY KEY,
            personality TEXT,
            tone TEXT,
            language TEXT,
            ai_model TEXT,
            max_output INTEGER
        );
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Database cleared and tables recreated.")

if __name__ == "__main__":
    clear_database()
