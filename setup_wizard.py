import sys
import json
import secrets
import socket
from pathlib import Path
import MySQLdb # type: ignore

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return '127.0.0.1'

def run_setup():
    print("=========================================================")
    print("Welcome to Student Remedial Learning App — First Time Setup")
    print("=========================================================\n")

    db_host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    db_port = input("MySQL Port (default: 3306): ").strip() or "3306"
    db_name = input("MySQL Database Name (default: remedial_db): ").strip() or "remedial_db"
    db_user = input("MySQL Username: ").strip()
    db_password = input("MySQL Password: ").strip()
    lan_access_input = input("Enable LAN access for mobile/tablet? (y/n - default: y): ").strip().lower()
    lan_access = lan_access_input != 'n'

    print("\nTesting database connection...")
    try:
        # Test connection first
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=int(db_port)
        )
        print("✅ Database connected successfully")
        
        # Create database if it doesn't exist
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        print("Please check your credentials and make sure MySQL is running.")
        sys.exit(1)

    secret_key = secrets.token_urlsafe(50)
    local_ip = get_local_ip()

    config = {
        "DB_NAME": db_name,
        "DB_USER": db_user,
        "DB_PASSWORD": db_password,
        "DB_HOST": db_host,
        "DB_PORT": db_port,
        "SECRET_KEY": secret_key,
        "LAN_ACCESS": lan_access,
        "FIRST_RUN_COMPLETE": True
    }

    config_path = Path(__file__).resolve().parent / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    if lan_access:
        print(f"\n📱 Mobile access will be available at: http://{local_ip}:8000")
    
    print("\n✅ Setup complete! Launching the app...\n")

if __name__ == "__main__":
    run_setup()
