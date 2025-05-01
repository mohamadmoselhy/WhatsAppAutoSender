@echo off
echo Building WhatsApp Auto Sender Installer...

REM Check if Inno Setup is installed
if not exist "%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe" (
    echo Error: Inno Setup 6 is not installed.
    echo Please download and install Inno Setup 6 from http://www.jrsoftware.org/isinfo.php
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build the executable using PyInstaller
echo Building executable...
pyinstaller --clean --onefile --windowed --add-data "src;src" --icon=resources/icon.ico --name WhatsAppAutoSender run.py

REM Copy MessageTemplates to dist folder
echo Copying MessageTemplates...
xcopy /E /I /Y "src\MessageTemplates" "dist\MessageTemplates"

REM Create the installer
echo Creating installer...
"%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe" installer\WhatsAppAutoSender.iss

echo Done!
echo Installer is located in the dist folder.
pause 