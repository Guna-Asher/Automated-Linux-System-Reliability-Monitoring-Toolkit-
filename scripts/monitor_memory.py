#!/usr/bin/env python3
"""
Memory monitoring module.
"""
import sys
sys.path.insert(0, '.')  

from scripts.common import load_config, log_json, alert_terminal
import psutil

def monitor_memory():
    config = load_config()
    memory = psutil.virtual_memory()
    mem_percent = memory.percent
    
    threshold = config['memory_threshold']
    alert_status = 'ALERT' if mem_percent > threshold else 'OK'
    
    log_data = {
        'metric_name': 'memory_usage',
        'metric_value': mem_percent,
        'threshold_value': threshold,
        'alert_status': alert_status
    }
    log_json('system_metrics.json', log_data)
    
    if alert_status == 'ALERT':
        alert_terminal('Memory Usage', mem_percent, threshold)

if __name__ == '__main__':
    monitor_memory()

