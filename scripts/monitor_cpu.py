#!/usr/bin/env python3
"""
CPU monitoring module.
"""
import sys
sys.path.insert(0, '.')  # Allow importing common

from scripts.common import load_config, log_json, alert_terminal, get_timestamp
import psutil

def monitor_cpu():
    config = load_config()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    threshold = config['cpu_threshold']
    alert_status = 'ALERT' if cpu_percent > threshold else 'OK'
    
    log_data = {
        'metric_name': 'cpu_usage',
        'metric_value': cpu_percent,
        'threshold_value': threshold,
        'alert_status': alert_status
    }
    log_json('system_metrics.json', log_data)
    
    if alert_status == 'ALERT':
        alert_terminal('CPU Usage', cpu_percent, threshold)

if __name__ == '__main__':
    monitor_cpu()

