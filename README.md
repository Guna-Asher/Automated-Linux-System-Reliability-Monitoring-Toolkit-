# Automated Linux System Reliability Monitoring Toolkit

## Overview
Resume-level SRE project demonstrating monitoring, alerting, logging, automation. Monitors CPU/Memory/Disk/Services/Auth logs on Ubuntu Linux.

## Architecture
```
linux-reliability-monitor/
├── scripts/          # Monitoring modules
│   ├── common.py
│   ├── monitor_cpu.py
│   ├── monitor_memory.py
│   ├── monitor_disk.py
│   ├── monitor_auth_logs.py
│   ├── monitor_services.sh
│   ├── main_monitor.py
│   └── generate_summary.py
├── config/
│   └── thresholds.json
├── logs/             # JSONL logs (auto-created)
├── reports/          # Summary txt (auto-created)
└── README.md
```

## Prerequisites (Ubuntu)
```
sudo apt update
sudo apt install nginx docker.io openssh-server  # Test services
pip3 install psutil
chmod +x scripts/*.sh
```

## Quick Start
```bash
cd linux-reliability-monitor
python3 scripts/main_monitor.py
```

## Cron Scheduling (every 5 min)
```bash
crontab -e
# Add:
*/5 * * * * cd /path/to/linux-reliability-monitor && /usr/bin/python3 scripts/main_monitor.py >> /path/to/logs/cron.log 2>&1
```

## Modules
- **CPU/Memory/Disk**: psutil metrics vs thresholds.
- **Services**: Bash systemctl check/restart nginx/docker/ssh.
- **Auth Logs**: Tail /var/log/auth.log for failed logins.

## Outputs
- Terminal 🚨 ALERTs
- JSONL logs: `logs/system_metrics.json`, `logs/security_events.json`, `logs/service_status.json`
- Report: `reports/daily_summary.txt`

## Testing (Ubuntu)
1. Run `python3 scripts/main_monitor.py`
2. Simulate high CPU: `stress --cpu 8 --timeout 60s &`
3. Check logs/alerts.
4. Stop service: `sudo systemctl stop nginx`; rerun.
5. Failed logins: Attempt SSH fails.

## Sample Output
```
🚀 Starting Linux Reliability Monitoring...
🚨 ALERT 🚨 CPU Usage: 85.2% > threshold 70% at 2024-01-01T12:00:00
✅ Monitoring cycle complete.
```

## Troubleshooting
- Run on Ubuntu (systemctl, auth.log paths).
- psutil: `pip3 install psutil`
- Permissions: sudo for services/disk if needed.

## Future Improvements
- Real email (smtplib)
- Prometheus exporter
- Web dashboard (Flask)
- Docker containerization

Project complete per success criteria!

