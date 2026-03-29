import os
import sys
import json
import socket
import subprocess
import webbrowser
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'config.json'

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return '127.0.0.1'

def main():
    if not CONFIG_PATH.exists():
        subprocess.run([sys.executable, 'setup_wizard.py'])
        if not CONFIG_PATH.exists():
            print("Setup was not completed. Exiting.")
            sys.exit(1)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    # Inject config values into environment for Django
    for key, value in config.items():
        os.environ[key] = str(value)

    print("Running database migrations...")
    subprocess.run([sys.executable, 'manage.py', 'migrate', '--run-syncdb'], check=False)

    print("Seeding database (idempotent)...")
    subprocess.run([sys.executable, 'manage.py', 'seed_db'], check=False)

    local_ip = get_local_ip()
    lan_access = config.get("LAN_ACCESS", True)

    bind_address = '0.0.0.0:8000' if lan_access else '127.0.0.1:8000'
    
    # Start Django development server
    server_process = subprocess.Popen([sys.executable, 'manage.py', 'runserver', bind_address])

    time.sleep(2)  # Wait for server to start

    webbrowser.open('http://127.0.0.1:8000')

    print("\n" + "="*50)
    print("✅ Remedial Learning App is running!")
    print("   Desktop access: http://127.0.0.1:8000")
    if lan_access:
        print(f"   Mobile/LAN access: http://{local_ip}:8000")
        print("   (connect other devices to the same Wi-Fi network)")
    print("   Close this terminal window to stop the app.")
    print("="*50 + "\n")

    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        server_process.wait()
        print("\nApp stopped.")

if __name__ == "__main__":
    main()
