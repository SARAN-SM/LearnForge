# Build Script for PyInstaller
Write-Host "Building Student Remedial Pro Executable..." -ForegroundColor Cyan

# Ensure dependencies
pip install -r requirements.txt

# Run PyInstaller
# Using --onedir to pack everything into a single distribution folder
# We bundle the templates and static folders manually to ensure Django finds them
pyinstaller --name "StudentRemedialApp" `
            --onedir `
            --add-data "core/templates;core/templates" `
            --add-data "core/static;core/static" `
            --add-data "accounts/templates;accounts/templates" `
            --add-data "admin_portal/templates;admin_portal/templates" `
            --add-data "students/templates;students/templates" `
            --hidden-import "pymysql" `
            --hidden-import "MySQLdb" `
            --hidden-import "markdown" `
            --hidden-import "anthropic" `
            launcher.py

Write-Host "Build complete! Check the /dist/StudentRemedialApp/ directory." -ForegroundColor Green
