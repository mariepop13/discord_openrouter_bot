from src.utils.logging.logging_utils import get_logger
from src.database.schema.database_schema import setup_database

logger = get_logger(__name__)

async def initialize_database():
    """Initialize the database schema."""
    logger.info("Setting up the database...")
    await setup_database()
    logger.info("Database setup completed.")
