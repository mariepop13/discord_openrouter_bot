import logging
from typing import List
from .database_connection import execute_query

logging.basicConfig(level=logging.INFO)

async def create_tables():
    logging.debug("Creating tables if they do not exist.")
    await execute_query('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_id INTEGER,
            content TEXT,
            model TEXT,
            message_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    logging.debug("Created 'messages' table.")
    
    await execute_query('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    logging.debug("Created 'comments' table.")
    
    await execute_query('''
        CREATE TABLE IF NOT EXISTS personalization (
            user_id INTEGER PRIMARY KEY,
            personality TEXT,
            tone TEXT,
            language TEXT,
            ai_model TEXT,
            max_output INTEGER
        )
    ''')
    logging.debug("Created 'personalization' table.")

async def run_migrations():
    logging.debug("Running migrations.")
    migrations = {
        'personalization': ['ai_model', 'max_output'],
        'messages': ['message_type', 'channel_id']
    }
    
    for table, new_columns in migrations.items():
        existing_columns = await get_existing_columns(table)
        for column in new_columns:
            if column not in existing_columns:
                logging.debug(f"Adding {column} column to {table} table")
                column_type = 'INTEGER' if column == 'channel_id' else 'TEXT'
                await execute_query(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
    logging.debug("Migrations completed.")

async def get_existing_columns(table: str) -> List[str]:
    logging.debug(f"Fetching existing columns for table {table}.")
    result = await execute_query(f"PRAGMA table_info({table})")
    columns = [column[1] for column in result]
    logging.debug(f"Existing columns in {table}: {columns}")
    return columns

async def setup_database():
    logging.debug("Setting up the database.")
    await create_tables()
    await run_migrations()
    logging.debug("Database setup completed.")
