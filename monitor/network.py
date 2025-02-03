import subprocess
import logging

class NetworkMonitor:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.tcpdump_process = None

    def start_capture(self):
        """Start packet capture on MySQL port"""
        try:
            self.tcpdump_process = subprocess.Popen([
                'tcpdump', '-i', 'any', 'port', '3306',
                '-w', self.pcap_file
            ])
            logging.info("Started network capture")
            return True
        except Exception as e:
            logging.error(f"Failed to start network capture: {e}")
            return False

    def stop_capture(self):
        """Stop packet capture"""
        if self.tcpdump_process:
            self.tcpdump_process.terminate()
            logging.info("Stopped network capture") 