"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    This script controls user input by blocking and unblocking the keyboard and mouse on Windows.
    It also manages the touchpad state by enabling or disabling it accordingly.

Date: March 2025
"""

import ctypes
import subprocess
import logging
import sys
import io

# Ensure console and file output use UTF-8 (for Arabic/log readability)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("input_control.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def block_input():
    """Disables keyboard & mouse input (Windows only, requires admin)."""
    try:
        if not ctypes.windll.user32.BlockInput(True):
            raise RuntimeError("Failed to block user input.")
        # enable_touchpad()
        logger.info("⛔ User input has been blocked.")
    except Exception as e:
        logger.error(f"⚠️ Error while blocking input: {e}")
        raise RuntimeError(f"Error while blocking input: {e}") from e


def unblock_input():
    """Re-enables keyboard & mouse input."""
    try:
        if not ctypes.windll.user32.BlockInput(False):
            raise RuntimeError("Failed to unblock user input.")
        # disable_touchpad()
        logger.info("✅ User input has been unblocked.")
    except Exception as e:
        logger.error(f"⚠️ Error while unblocking input: {e}")
        raise RuntimeError(f"Error while unblocking input: {e}") from e


def disable_touchpad():
    """Disables the touchpad using PowerShell."""
    try:
        subprocess.run(
            ['powershell', '-Command', 'Disable-PnpDevice -InstanceId "HID\\VID_04F3&PID_0903" -Confirm:$false'],
            check=True
        )
        logger.info("✅ Touchpad has been disabled.")
    except subprocess.CalledProcessError as e:
        logger.error(f"⚠️ Error disabling touchpad: {e}")
        raise RuntimeError(f"Error disabling touchpad: {e}") from e


def enable_touchpad():
    """Enables the touchpad using PowerShell."""
    try:
        subprocess.run(
            ['powershell', '-Command', 'Enable-PnpDevice -InstanceId "HID\\VID_04F3&PID_0903" -Confirm:$false'],
            check=True
        )
        logger.info("✅ Touchpad has been enabled.")
    except subprocess.CalledProcessError as e:
        logger.error(f"⚠️ Error enabling touchpad: {e}")
        raise RuntimeError(f"Error enabling touchpad: {e}") from e
