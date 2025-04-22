from setuptools import setup, find_packages

setup(
    name="whatsapp-auto-sender",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pywinauto",
        "watchdog",
    ],
    entry_points={
        "console_scripts": [
            "whatsapp-auto-sender=src.run:main",
        ],
    },
) 