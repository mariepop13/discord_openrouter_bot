import sqlite3
import logging
from contextlib import asynccontextmanager

DATABASE_NAME = 'bot_database.sqlite'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_db_connection():
    logger.debug("Connecting to the database.")
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()
        logger.debug("Database connection closed.")

async def execute_query(query: str, params: tuple = (), fetchone: bool = False):
    logger.debug(f"Executing query: {query} with params: {params}")
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            logger.debug("Query executed successfully.")
            if fetchone:
                result = cursor.fetchone()
                logger.debug(f"Fetched one result: {result}")
                return result
            results = cursor.fetchall()
            logger.debug(f"Fetched all results: {results}")
            return results
        except sqlite3.Error as e:
            logger.error(f"An error occurred: {e}")
            raise
