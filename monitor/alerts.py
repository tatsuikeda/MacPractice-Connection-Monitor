import os
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import deque

class AlertManager:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.recipient_emails = [email.strip() for email in os.getenv('RECIPIENT_EMAILS').split(',')]
        self.company_name = os.getenv('COMPANY_NAME')
        self.server_name = os.getenv('SERVER_NAME')
        self.alert_queue = deque()

    def queue_alert(self, issue_type, details):
        """Add alert to queue"""
        alert = {
            'timestamp': datetime.now(),
            'type': issue_type,
            'details': details
        }
        self.alert_queue.append(alert)
        logging.info(f"Queued alert: {issue_type}")

    def send_queued_alerts(self):
        """Process and send all queued alerts"""
        while self.alert_queue:
            alert = self.alert_queue.popleft()
            subject = f"[{self.company_name}] MacPractice Server {self.server_name} - {alert['type'].replace('_', ' ').title()}"
            body = self._format_alert_body(alert)
            self.send_email(subject, body)

    def send_email(self, subject, body):
        """Send email using configured SMTP settings"""
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

    def _format_alert_body(self, alert):
        """Format alert body with standard template"""
        return f"""
Time: {alert['timestamp']}
Server: {self.server_name}
Company: {self.company_name}
Issue Type: {alert['type']}
Details: {alert['details']}

Additional Info:
- Check /var/log/mp_monitor/connection.log for full connection logs
- Network capture available in /var/log/mp_monitor/traffic.pcap
"""

    def send_test_email(self):
        """Send test email to verify configuration"""
        subject = f"[{self.company_name}] Test Email - MacPractice Connection Monitor"
        body = f"""
This is a test email from the MacPractice Connection Monitor.
Server: {self.server_name}
Company: {self.company_name}
Time: {datetime.now()}

If you received this email, your email configuration is working correctly.
"""
        self.send_email(subject, body)
        logging.info("Test email sent") 