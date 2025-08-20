import logging
import subprocess

logger = logging.getLogger(__name__)


def check_adb():
    """Check if ADB is available"""

    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("ADB found and working")
            return True
        else:
            logger.error("ADB found but not working properly")
            return False
    except FileNotFoundError:
        logger.error("ADB not found. Please install Android SDK Platform Tools.")
        logger.info("Download from: https://developer.android.com/studio/releases/platform-tools")
        return False


def show_cli_help():
    logger.info("Bloatware Remover - Remove unwanted apps from Android devices")
    logger.info("\nUsage:")
    logger.info("  bloatware-remover          # Start the web server")
    logger.info("  bloatware-remover --help   # Show this help")
    logger.info("\nAfter starting, open http://localhost:8000 in your browser")
    return
