#!/usr/bin/env python3
"""
Authentication log monitoring (/var/log/auth.log).
"""
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, '.')  

from scripts.common import load_config, log_json, alert_terminal, get_timestamp

def tail_auth_log(lines=100):
    """Tail last lines of auth.log and count failed logins."""
    try:
        cmd = ["tail", "-n", str(lines), "/var/log/auth.log"]
        output = subprocess.check_output(cmd, text=True)
        failed_count = output.count('Failed password')
        return failed_count
    except subprocess.CalledProcessError:
        print("Warning: Cannot read /var/log/auth.log", file=sys.stderr)
        return 0

def monitor_auth_logs():
    config = load_config()
    failed_attempts = tail_auth_log()
    
    threshold = config['failed_login_attempts_threshold']
    alert_status = 'ALERT' if failed_attempts > threshold else 'OK'
    
    log_data = {
        'metric_name': 'auth_failed_logins',
        'metric_value': failed_attempts,
        'threshold_value': threshold,
        'alert_status': alert_status
    }
    log_json('security_events.json', log_data)
    
    if alert_status == 'ALERT':
        alert_terminal('Failed SSH Logins', failed_attempts, threshold)

if __name__ == '__main__':
    monitor_auth_logs()

