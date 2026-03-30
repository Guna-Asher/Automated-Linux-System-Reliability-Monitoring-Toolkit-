#!/usr/bin/env python3
"""
Common utilities for all monitoring scripts.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import psutil  # External dependency

def get_timestamp():
    """Return ISO timestamp string."""
    return datetime.now().isoformat()

def load_config(config_path='config/thresholds.json'):
    """Load thresholds from JSON."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_path} not found. Using defaults.", file=sys.stderr)
        return {
            "cpu_threshold": 70,
            "memory_threshold": 80,
            "disk_threshold": 80,
            "failed_login_attempts_threshold": 5
        }

def log_json(log_file, data):
    """Append structured log entry to JSONL file."""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    log_path = logs_dir / log_file
    
    entry = {
        "timestamp": get_timestamp(),
        **data
    }
    
    with open(log_path, 'a') as f:
        f.write(json.dumps(entry) + '\\n')

def alert_terminal(metric_name, value, threshold, status='ALERT'):
    """Print terminal alert."""
    print(f"🚨 {status} 🚨 {metric_name}: {value}% > threshold {threshold}% at {get_timestamp()}")
    
    # Simulate email (placeholder)
    print(f"[EMAIL SIMULATION] Alert: {metric_name} violation!")

