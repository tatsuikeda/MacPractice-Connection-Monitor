#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root. Rerunning with sudo...")
        args = ['sudo', sys.executable] + sys.argv
        os.execvp('sudo', args)

def create_project_structure():
    # Base directories
    project_dir = Path('/usr/local/mp_connection_monitor')
    log_dir = Path('/var/log/mp_monitor')
    
    directories = {
        project_dir: 0o755,
        project_dir / 'config': 0o755,
        project_dir / 'tests': 0o755,
        log_dir: 0o755
    }

    # Create directories with proper permissions
    for directory, permission in directories.items():
        directory.mkdir(parents=True, exist_ok=True)
        os.chmod(directory, permission)

    # Create log files
    log_files = [
        log_dir / 'connection.log',
        log_dir / 'traffic.pcap',
        log_dir / 'monitor.log'
    ]
    
    for log_file in log_files:
        log_file.touch(exist_ok=True)
        os.chmod(log_file, 0o644)

    # Create project files
    files = {
        project_dir / 'requirements.txt': '''python-dotenv==1.0.0
mysql-connector-python==8.3.0
scapy==2.5.0''',
        
        project_dir / '.env.example': '''SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD="your_app_password"
RECIPIENT_EMAILS="email1@example.com, email2@example.com"
COMPANY_NAME="BNS"
SERVER_NAME="MP-Server-01"''',

        project_dir / '.gitignore': '''__pycache__/
*.pyc
.env
*.log
*.pcap
.venv/
''',
    }

    for file_path, content in files.items():
        file_path.write_text(content)
        os.chmod(file_path, 0o644)

def setup_virtual_environment():
    venv_dir = Path('/usr/local/mp_connection_monitor/.venv')
    if not venv_dir.exists():
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
        
    # Install requirements
    pip_path = venv_dir / 'bin' / 'pip'
    subprocess.run([str(pip_path), 'install', '-r', '/usr/local/mp_connection_monitor/requirements.txt'], check=True)

def main():
    check_root()
    print("Creating MacPractice Connection Monitor project structure...")
    create_project_structure()
    setup_virtual_environment()
    
    print("""
Project setup complete!

To run the monitor:
    sudo /usr/local/mp_connection_monitor/.venv/bin/python /usr/local/mp_connection_monitor/mp_connection_monitor.py

To test email configuration:
    sudo /usr/local/mp_connection_monitor/.venv/bin/python /usr/local/mp_connection_monitor/mp_connection_monitor.py --test_email

Configuration:
1. Copy .env.example to .env
2. Edit .env with your settings
3. Ensure proper permissions on .env file
""")

if __name__ == "__main__":
    main()
