# Student Remedial Learning Application

A self-contained, fully local Django application designed to help students master subjects systematically. It features an intelligent content engine that generates quizzes based on uploaded study materials.

## Features
- **Local Priority**: Designed to run entirely on your local machine and LAN.
- **Role-Based Portals**: Dedicated portals for Students (Learning, Quizzes, Leaderboard) and Admins (Post Material, View Performance).
- **Gamification**: Weekly leaderboards, level multipliers, daily streaks, and completion certificates.
- **Intelligent Engine**: Generates 3 tiers of quizzes natively without using outside interfaces.

## Setup Instructions
The application includes a `setup_wizard.py` that will run automatically the first time you execute `launcher.py`.

### Prerequisites
- Python 3.9+
- MySQL 8.0+ running on your system.

### Running from Source
1. **Install Requirements:**
   ```powershell
   # Open Command Prompt or PowerShell in this directory
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Run the App Launcher:**
   ```powershell
   python launcher.py
   ```
   *The launcher will automatically invoke the Setup Wizard if `config.json` is missing. It will handle database schema setup and create the master admin user.*

3. **Access the App:**
   - On the host machine: `http://localhost:8000`
   - On LAN devices (Mobile/Tablet): Check the launcher console for your Local IP (e.g. `http://192.168.1.X:8000`).

## Building the Desktop Executable
If you wish to distribute this application as a single folder containing an executable rather than requiring Python installations on target machines, run the build script:

```powershell
.\build.ps1
```

This uses PyInstaller to bundle the application. The output will be located in the `dist/StudentRemedialApp/` directory. You can zip that directory and share it. The end-user simply double-clicks `launcher.exe`.
