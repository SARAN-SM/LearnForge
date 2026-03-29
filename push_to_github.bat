@echo off
echo Starting GitHub push process...
git --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Git is still not recognized. Please install Git from https://gitforwindows.org/ and restart your computer.
    pause
    exit /b
)

echo Configuring Git...
git config --global user.email "saran@example.com"
git config --global user.name "Saran"

echo Initializing repository...
git init
git add .
git commit -m "Initial commit of Student Remedial Pro project"

echo Setting up remote...
git branch -M main
git remote add origin https://github.com/SARAN-SM/LearnForge.git
git push -u origin main

echo.
echo Process complete!
pause
