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
    """Disables the touchpad using PowerShell (Windows only, requires admin)."""
    try:
        command = 'powershell Get-PnpDevice | Where-Object { $_.FriendlyName -like "*Touchpad*" } | Disable-PnpDevice -Confirm:$false'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)  
        if result.returncode != 0:
            raise RuntimeError(f"PowerShell error: {result.stderr}")
        print("⛔ Touchpad disabled.")
    except subprocess.CalledProcessError as e:
        error_msg = f"⚠️ Error disabling touchpad: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow with detailed context.

def enable_touchpad():
    """Enables the touchpad using PowerShell (Windows only, requires admin)."""
    try:
        command = 'powershell Get-PnpDevice | Where-Object { $_.FriendlyName -like "*Touchpad*" } | Enable-PnpDevice -Confirm:$false'
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)  
        if result.returncode != 0:
            raise RuntimeError(f"PowerShell error: {result.stderr}")
        print("✅ Touchpad enabled.")
    except subprocess.CalledProcessError as e:
        error_msg = f"⚠️ Error enabling touchpad: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow with debugging details.
