#!/usr/bin/env python3
"""
Main orchestrator: Runs all monitoring modules.
"""
import sys
import subprocess
from pathlib import Path
sys.path.insert(0, '.')  

from scripts.common import load_config, log_json, get_timestamp

# Import individual monitors
from scripts.monitor_cpu import monitor_cpu
from scripts.monitor_memory import monitor_memory
from scripts.monitor_disk import monitor_disk
from scripts.monitor_auth_logs import monitor_auth_logs

def run_service_monitor():
    """Run bash service monitor."""
    bash_script = Path('scripts/monitor_services.sh')
    if bash_script.exists():
        subprocess.run(['bash', str(bash_script)], check=True)
    else:
        print("Warning: monitor_services.sh not found", file=sys.stderr)

def generate_summary():
    """Generate simple daily summary."""
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    summary_path = reports_dir / 'daily_summary.txt'
    timestamp = get_timestamp()
    
    summary = f"Monitoring Summary at {timestamp}\\n"
    summary += "=" * 50 + "\\n\\n"
    
    # Placeholder: count alerts from logs
    logs_dir = Path('logs')
    if logs_dir.exists():
        for log_file in logs_dir.glob('*.json'):
            alert_count = sum(1 for line in log_file.open() if 'ALERT' in line)
            summary += f"{log_file.name}: {alert_count} alerts\\n"
    
    with open(summary_path, 'w') as f:
        f.write(summary)

def main():
    print("🚀 Starting Linux Reliability Monitoring...")
    
    # Run monitors
    monitor_cpu()
    monitor_memory()
    monitor_disk()
    monitor_auth_logs()
    run_service_monitor()
    
    # Generate summary
    generate_summary()
    
    print("✅ Monitoring cycle complete.")

if __name__ == '__main__':
    main()

