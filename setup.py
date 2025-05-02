"""
Setup script for WhatsApp Auto Sender
"""

from setuptools import setup, find_packages

setup(
    name="WhatsAppAutoSender",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pywinauto',
        'pyautogui',
        'pyperclip',
        'hijri-converter',
        'pillow',  # Required for screenshots
    ],
    entry_points={
        'console_scripts': [
            'whatsapp-auto-sender=run:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated WhatsApp file sender with monitoring capabilities",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/WhatsAppAutoSender",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
) 