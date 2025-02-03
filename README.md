# MacPractice Connection Monitor

Created by Tatsu Ikeda, 2025

## Description

This Python script monitors MacPractice server and client connections by tracking MySQL connections, network traffic, and VPN connectivity. It provides real-time monitoring and email notifications for connection issues.

## Quick Start

```bash
# Clone repository
git clone https://github.com/tatsuikeda/mp_connection_monitor.git
cd ~/projects/mp_connection_monitor

# Run setup script as root
sudo python3 setup_mp_monitor.py
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

1. Copy `.env.example` to `.env` and configure:

### Email Settings
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD="your_app_password"
RECIPIENT_EMAILS="email1@example.com, email2@example.com"
```

### Server Identification
```
COMPANY_NAME="BNS"
SERVER_NAME="MP-Server-01"
```

### Database Settings
```
MYSQL_USER="_macpractice"
MYSQL_PASSWORD="your_mysql_password"
MYSQL_HOST="localhost"
MYSQL_DATABASE="macpractice"
```

2. Set appropriate permissions:
```bash
sudo chmod 600 /usr/local/mp_connection_monitor/.env
```

## MySQL Setup

Create the monitoring user and grant permissions:
```sql
CREATE USER '_macpractice'@'localhost' IDENTIFIED BY 'your_mysql_password';
GRANT SELECT ON macpractice.* TO '_macpractice'@'localhost';
FLUSH PRIVILEGES;
```

## Usage

1. Start monitoring:
```bash
sudo /usr/local/mp_connection_monitor/.venv/bin/python /usr/local/mp_connection_monitor/mp_connection_monitor.py
```

2. Test email configuration:
```bash
sudo /usr/local/mp_connection_monitor/.venv/bin/python /usr/local/mp_connection_monitor/mp_connection_monitor.py --test_email
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