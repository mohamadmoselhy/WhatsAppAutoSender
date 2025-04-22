from setuptools import setup, find_packages

setup(
    name="whatsapp_auto_sender",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml==6.0.1",
        "pyautogui==0.9.54",
        "pillow==10.0.0",
        "watchdog==3.0.0",
        "python-dotenv==1.0.0"
    ],
    python_requires=">=3.7",
) 