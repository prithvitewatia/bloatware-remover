# Ensure src directory is in sys.path for PyInstaller executable
import logging
import sys

from fastapi import FastAPI
import uvicorn

from src.routes import router
from src.utils import check_adb, show_cli_help

logger = logging.getLogger(__name__)


# Create FastAPI app with better metadata
app = FastAPI(
    title="Bloatware Remover",
    description="A modern web-based tool for safely removing bloatware from Android devices using ADB",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.include_router(router)


def start_server():
    """Start the web server"""
    logger.info(" Starting Bloatware Remover...")
    logger.info("📱 Open your browser and go to: http://localhost:8000")
    logger.info("⏹️  Press Ctrl+C to stop the application")

    try:
        # Use direct app reference for PyInstaller executable
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for production
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
