#!/usr/bin/env python3
"""
Disk usage monitoring for / and /home.
"""
import sys
sys.path.insert(0, '.')  

from scripts.common import load_config, log_json, alert_terminal
import psutil

def monitor_disk():
    config = load_config()
    threshold = config['disk_threshold']
    
    for mountpoint in ['/', '/home']:
        try:
            usage = psutil.disk_usage(mountpoint)
            disk_percent = (usage.used / usage.total) * 100
            
            alert_status = 'ALERT' if disk_percent > threshold else 'OK'
            
            log_data = {
                'metric_name': f'disk_usage_{mountpoint}',
                'metric_value': disk_percent,
                'threshold_value': threshold,
                'alert_status': alert_status,
                'mountpoint': mountpoint
            }
            log_json('system_metrics.json', log_data)
            
            if alert_status == 'ALERT':
                alert_terminal(f'Disk Usage {mountpoint}', disk_percent, threshold)
        except PermissionError:
            print(f"Warning: Cannot access {mountpoint}", file=sys.stderr)

if __name__ == '__main__':
    monitor_disk()

