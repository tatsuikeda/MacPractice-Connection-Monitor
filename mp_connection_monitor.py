#!/usr/bin/env python3
import sys
import signal
from dotenv import load_dotenv
from monitor import MPConnectionMonitor

def main():
    # Load environment variables
    load_dotenv()
    
    monitor = MPConnectionMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test_email':
        monitor.alert_manager.send_test_email()
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, monitor.cleanup)
    signal.signal(signal.SIGTERM, monitor.cleanup)
    
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
