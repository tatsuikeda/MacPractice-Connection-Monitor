import re
import logging
from pathlib import Path

def setup_logging(log_file):
    """Configure logging with file and console output"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def analyze_logs(connection_log, alert_manager):
    """Analyze logs for patterns and queue alerts"""
    patterns = {
        'connection_drop': r'Lost connection|Connection closed',
        'timeout': r'Connection timed out|Read timeout',
        'high_latency': r'slow query|Query execution time',
        'max_connections': r'Too many connections|Connection limit reached'
    }
    
    try:
        with open(connection_log, 'r') as f:
            logs = f.readlines()
            
        for line in logs[-100:]:  # Check last 100 lines
            for issue, pattern in patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    alert_manager.queue_alert(issue, line.strip())
    except Exception as e:
        logging.error(f"Log analysis error: {str(e)}") 