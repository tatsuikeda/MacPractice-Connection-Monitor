# MacPractice Connection Monitor

Created by Tatsu Ikeda, 2025

## Description

This Python script monitors MacPractice server and client connections by tracking MySQL connections, network traffic, and VPN connectivity. It provides real-time monitoring and email notifications for connection issues.

## Quick Start

```bash
# Clone repository
git clone https://github.com/tatsuikeda/mp_connection_monitor.git
cd ~/projects/mp_connection_monitor

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Features

- MySQL connection monitoring (port 3306)
- Network traffic capture and analysis
- Email notifications for connection drops
- Detailed logging system
- Automatic log rotation
- VPN connection status tracking
- DNS configuration monitoring

## Configuration

1. Create a `.env` file in the project directory:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD="your_app_password"
RECIPIENT_EMAILS="email1@example.com, email2@example.com"
COMPANY_NAME="Your Practice Name"
SERVER_NAME="MP-Server-01"
```

2. Create log directories:
```bash
sudo mkdir -p /var/log/mp_monitor
sudo touch /var/log/mp_monitor/connection.log
sudo touch /var/log/mp_monitor/traffic.pcap
sudo chmod 755 /var/log/mp_monitor
```

## Usage

1. Start monitoring:
```bash
sudo .venv/bin/python mp_connection_monitor.py
```

2. Test email configuration:
```bash
sudo .venv/bin/python mp_connection_monitor.py --test_email
```

## Log Files

- `/var/log/mp_monitor/connection.log`: Connection events and status
- `/var/log/mp_monitor/traffic.pcap`: Network traffic capture
- `/var/log/mp_monitor/monitor.log`: Monitor script activity

## Email Notifications

The script sends alerts for:
- Client disconnections
- MySQL connection issues
- Network anomalies
- VPN connection drops
- DNS configuration changes

## Troubleshooting

- Check MySQL process list for connection issues
- Review network capture files
- Verify email configuration
- Monitor disk space for log files
- Check MacPractice client logs

## License

MIT License
Copyright (c) 2024 Tatsu Ikeda

Permission is hereby granted, free of charge, to any person obtaining a copy of this software.