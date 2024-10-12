import sqlite3
import logging
from typing import List
from .database_connection import execute_query

async def create_tables():
    await execute_query('''
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

async def run_migrations():
    migrations = {
        'personalization': ['ai_model', 'max_output'],
        'messages': ['message_type']
    }
    
    for table, new_columns in migrations.items():
        existing_columns = await get_existing_columns(table)
        for column in new_columns:
            if column not in existing_columns:
                logging.info(f"Adding {column} column to {table} table")
                await execute_query(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")

async def get_existing_columns(table: str) -> List[str]:
    result = await execute_query(f"PRAGMA table_info({table})")
    return [column[1] for column in result]

async def setup_database():
    await create_tables()
    await run_migrations()
