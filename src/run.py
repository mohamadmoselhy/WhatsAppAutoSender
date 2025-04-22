#!/usr/bin/env python
"""
Run script for WhatsApp Auto Sender
"""

import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main application
from main import main

if __name__ == "__main__":
    main() 