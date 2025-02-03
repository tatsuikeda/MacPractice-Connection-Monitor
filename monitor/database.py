import os
import logging
from datetime import datetime
import mysql.connector

def get_db_connection():
    """Create a new database connection using environment variables"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

def monitor_mysql_connections(connection_log):
    """Monitor MySQL processes and log connections"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SHOW PROCESSLIST")
        processes = cursor.fetchall()
        
        with open(connection_log, 'a') as f:
            f.write(f"\n--- Connection Check: {datetime.now()} ---\n")
            for process in processes:
                f.write(f"ID: {process[0]}, User: {process[1]}, Host: {process[2]}, "
                       f"DB: {process[3]}, Command: {process[4]}, Time: {process[5]}, "
                       f"State: {process[6]}\n")
        
        cursor.close()
        db.close()
        return True
        
    except Exception as e:
        logging.error(f"MySQL connection error: {str(e)}")
        return False 