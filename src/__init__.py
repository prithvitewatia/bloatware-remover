import os
import sys  # Ensure src directory is in sys.path for PyInstaller executable

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Ensure project root is in sys.path for PyInstaller and direct execution
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
