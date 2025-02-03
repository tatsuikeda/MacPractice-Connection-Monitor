import os
import sys
import time
import signal
import logging
from pathlib import Path
from dotenv import load_dotenv

from .database import monitor_mysql_connections
from .network import NetworkMonitor
from .alerts import AlertManager
from .utils import setup_logging, analyze_logs

class MPConnectionMonitor:
    def __init__(self):
        self.connection_log = "/var/log/mp_monitor/connection.log"
        self.traffic_pcap = "/var/log/mp_monitor/traffic.pcap"
        self.monitor_log = "/var/log/mp_monitor/monitor.log"
        self.running = True

        setup_logging(self.monitor_log)
        self.alert_manager = AlertManager()
        self.network_monitor = NetworkMonitor(self.traffic_pcap)
        
    def start_monitoring(self):
        """Start the monitoring process"""
        self.network_monitor.start_capture()
        logging.info(f"Started monitoring for {os.getenv('COMPANY_NAME')} - {os.getenv('SERVER_NAME')}")
        
        while self.running:
            try:
                if not monitor_mysql_connections(self.connection_log):
                    self.alert_manager.queue_alert("mysql_error", "Failed to monitor MySQL connections")
                
                analyze_logs(self.connection_log, self.alert_manager)
                self.alert_manager.send_queued_alerts()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logging.error(f"Monitoring error: {str(e)}")

    def cleanup(self, signum, frame):
        """Clean up resources on shutdown"""
        logging.info("Stopping monitoring...")
        self.running = False
        self.network_monitor.stop_capture()
        sys.exit(0) 