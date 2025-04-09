"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    This script controls user input by blocking and unblocking the keyboard and mouse on Windows.
    It also manages the touchpad state by enabling or disabling it accordingly.

Date: March 2025
"""

import ctypes  # Provides access to Windows system calls.
import subprocess  # Allows execution of system commands.
import time

def block_input():
    """Disables keyboard & mouse input (Windows only, requires admin)."""
    try:
        if not ctypes.windll.user32.BlockInput(True):  # Blocks input using Windows API.
            raise RuntimeError("Failed to block user input.")  
        #enable_touchpad()  # Ensures the touchpad is enabled while input is blocked.
        print("⛔ Input has been blocked.")
    except Exception as e:
        error_msg = f"⚠️ Error blocking input: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow the exception for higher-level handling.

def unblock_input():
    """Re-enables keyboard & mouse input."""
    try:
        if not ctypes.windll.user32.BlockInput(False):  # Unblocks input using Windows API.
            raise RuntimeError("Failed to unblock user input.")  
        #disable_touchpad()  # Ensures the touchpad is disabled after input is unblocked.
        print("✅ Input has been unblocked.")
    except Exception as e:
        error_msg = f"⚠️ Error unblocking input: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow for better debugging.


def disable_touchpad():
    try:
        # PowerShell command to disable touchpad (you'll need to identify the right device ID)
        subprocess.run(['powershell', '-Command', 'Disable-PnpDevice -InstanceId "HID\VID_04F3&PID_0903"'], check=True)
        print("✅ Touchpad disabled.")
    except subprocess.CalledProcessError as e:
        error_msg = f"⚠️ Error disabling touchpad: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e

def enable_touchpad():
    try:
        # PowerShell command to enable touchpad (again, make sure the correct device ID is used)
        subprocess.run(['powershell', '-Command', 'Enable-PnpDevice -InstanceId "HID\VID_04F3&PID_0903"'], check=True)
        print("✅ Touchpad enabled.")
    except subprocess.CalledProcessError as e:
        error_msg = f"⚠️ Error enabling touchpad: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e
