from fastapi import FastAPI
import uvicorn
import sys
import os

# Ensure src directory is in sys.path for PyInstaller executable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Ensure project root is in sys.path for PyInstaller and direct execution
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.routes import router

# Create FastAPI app with better metadata
app = FastAPI(
    title="Bloatware Remover",
    description="A modern web-based tool for safely removing bloatware from Android devices using ADB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(router)

def check_adb():
    """Check if ADB is available"""
    import subprocess
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ADB found and working")
            return True
        else:
            print("⚠️  ADB found but not working properly")
            return False
    except FileNotFoundError:
        print("❌ ADB not found. Please install Android SDK Platform Tools.")
        print("   Download from: https://developer.android.com/studio/releases/platform-tools")
        return False

def start_server():
    """Start the web server"""
    print(" Starting Bloatware Remover...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Check ADB availability
    if not check_adb():
        print("\n⚠️  Warning: ADB not available. Some features may not work.")
        print("   Please install ADB to use all features.\n")
    
    try:
        # Use direct app reference for PyInstaller executable
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for production
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Bloatware Remover...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Bloatware Remover - Remove unwanted apps from Android devices")
        print("\nUsage:")
        print("  bloatware-remover          # Start the web server")
        print("  bloatware-remover --help   # Show this help")
        print("\nAfter starting, open http://localhost:8000 in your browser")
        return
    
    start_server()

if __name__ == "__main__":
    main()