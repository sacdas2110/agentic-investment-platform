#!/usr/bin/env python3
"""Database migration runner - uses Alembic"""

import os
import sys
from alembic import command
from alembic.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run all pending database migrations"""
    try:
        # Alembic config
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        
        # Set database URL from environment
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://investment_user:investment_password@localhost:5432/investment_db"
        )
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        # Run migrations
        logger.info(f"Running migrations against {database_url}")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully")
        
        return True
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
