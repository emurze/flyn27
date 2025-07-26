import os
import sys

# Add the 'src' folder (adjust the path as needed) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app import create_app

app = create_app()
