#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
import logging
from collections import deque
import re
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import signal
import mysql.connector
from scapy.all import sniff

# Load environment variables from .env
load_dotenv()

class MPConnectionMonitor:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.recipient_emails = [email.strip() for email in os.getenv('RECIPIENT_EMAILS').split(',')]
        self.company_name = os.getenv('COMPANY_NAME')
        self.server_name = os.getenv('SERVER_NAME')
        self.running = True
        self.connection_log = "/var/log/mp_monitor/connection.log"
        self.traffic_pcap = "/var/log/mp_monitor/traffic.pcap"
        self.monitor_log = "/var/log/mp_monitor/monitor.log"
        self.alert_queue = deque()
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.monitor_log),
                logging.StreamHandler()
            ]
        )
        
    def start_monitoring(self):
        # Start packet capture in background
        self.tcpdump_process = subprocess.Popen([
            'tcpdump', '-i', 'any', 'port', '3306',
            '-w', self.traffic_pcap
        ])
        
        logging.info(f"Started monitoring for {self.company_name} - {self.server_name}")
        
        while self.running:
            try:
                self.monitor_connections()
                self.analyze_logs()
                self.send_queued_alerts()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logging.error(f"Monitoring error: {str(e)}")

    def monitor_connections(self):
        try:
            # Monitor MySQL connections
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("SHOW PROCESSLIST")
            processes = cursor.fetchall()
            
            with open(self.connection_log, 'a') as f:
                f.write(f"\n--- Connection Check: {datetime.now()} ---\n")
                for process in processes:
                    f.write(f"ID: {process[0]}, User: {process[1]}, Host: {process[2]}, DB: {process[3]}, Command: {process[4]}, Time: {process[5]}, State: {process[6]}\n")
            
            cursor.close()
            db.close()
            
        except Exception as e:
            logging.error(f"MySQL connection error: {str(e)}")
            self.queue_alert("mysql_error", str(e))

    def analyze_logs(self):
        patterns = {
            'connection_drop': r'Lost connection|Connection closed',
            'timeout': r'Connection timed out|Read timeout',
            'high_latency': r'slow query|Query execution time',
            'max_connections': r'Too many connections|Connection limit reached'
        }
        
        try:
            with open(self.connection_log, 'r') as f:
                logs = f.readlines()
                
            for line in logs[-100:]:  # Check last 100 lines
                for issue, pattern in patterns.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        self.queue_alert(issue, line.strip())
        except Exception as e:
            logging.error(f"Log analysis error: {str(e)}")

    def queue_alert(self, issue_type, details):
        alert = {
            'timestamp': datetime.now(),
            'type': issue_type,
            'details': details
        }
        self.alert_queue.append(alert)
        logging.info(f"Queued alert: {issue_type}")

    def send_queued_alerts(self):
        while self.alert_queue:
            alert = self.alert_queue.popleft()
            subject = f"[{self.company_name}] MacPractice Server {self.server_name} - {alert['type'].replace('_', ' ').title()}"
            body = f"""
Time: {alert['timestamp']}
Server: {self.server_name}
Company: {self.company_name}
Issue Type: {alert['type']}
Details: {alert['details']}

Additional Info:
- Check /var/log/mp_monitor/connection.log for full connection logs
- Network capture available in /var/log/mp_monitor/traffic.pcap
"""
            self.send_email(subject, body)

    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                
                for recipient in self.recipient_emails:
                    msg['To'] = recipient
                    server.send_message(msg)
                    logging.info(f"Alert email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")

    def cleanup(self, signum, frame):
        logging.info("Stopping monitoring...")
        self.running = False
        if hasattr(self, 'tcpdump_process'):
            self.tcpdump_process.terminate()
        sys.exit(0)

def test_email_config(monitor):
    subject = f"[{monitor.company_name}] Test Email - MacPractice Connection Monitor"
    body = f"""
This is a test email from the MacPractice Connection Monitor.
Server: {monitor.server_name}
Company: {monitor.company_name}
Time: {datetime.now()}

If you received this email, your email configuration is working correctly.
"""
    monitor.send_email(subject, body)
    logging.info("Test email sent")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

def main():
    monitor = MPConnectionMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test_email':
        test_email_config(monitor)
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, monitor.cleanup)
    signal.signal(signal.SIGTERM, monitor.cleanup)
    
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
