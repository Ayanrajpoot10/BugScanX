import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from bugscanx.main import main_menu

if __name__ == "__main__":
    main_menu()