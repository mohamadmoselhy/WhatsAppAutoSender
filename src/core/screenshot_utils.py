"""
Screenshot utility functions
"""

import os
from datetime import datetime
import pyautogui
from src.core.constants import *
from src.core.logger import logger

def take_screenshot(error_context: str = None) -> str:
    """
    Take a screenshot and save it to the logs directory
    
    Args:
        error_context: Optional context about the error for the filename
        
    Returns:
        str: Path to the saved screenshot
    """
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join("logs", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate filename with timestamp and context
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        context = f"_{error_context}" if error_context else ""
        filename = f"error_screenshot_{timestamp}{context}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        logger.log_info(f"Screenshot saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.log_error(e, "Failed to take screenshot")
        return None 