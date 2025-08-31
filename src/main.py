from contextlib import asynccontextmanager
import logging
import sys

from fastapi import FastAPI
import uvicorn

from src.db import db_manager
from src.routes import router
from src.utils import check_adb, show_cli_help

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.connect()
    if not await db_manager.is_connected():
        logger.error("Failed to connect to the db")
        sys.exit(1)
    logger.info("Connected to database")
    await db_manager.create_tables()
    logger.info("Created db tables")
    yield
    await db_manager.close()
    logger.info("Closed db connection")


app = FastAPI(
    title="Bloatware Remover",
    description="A modern web-based tool for safely removing bloatware from Android devices using ADB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)
app.include_router(router)


def start_server():
    """Start the web server"""
    logger.info(" Starting Bloatware Remover...")
    logger.info("📱 Open your browser and go to: http://localhost:8000")
    logger.info("⏹️  Press Ctrl+C to stop the application")

    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
        )
    except KeyboardInterrupt:
        logger.info("Shutting down Bloatware Remover...")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_cli_help()
        return
    if not check_adb():
        sys.exit(1)

    start_server()


if __name__ == "__main__":
    main()
