# Automated Linux System Reliability Monitoring Toolkit [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![Bash](https://img.shields.io/badge/Bash-Scripting-green)](https://www.gnu.org/software/bash/) [![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)](https://ubuntu.com/) [![SRE](https://img.shields.io/badge/SRE-Portfolio-red)](https://sre.google/sre-book/table-of-contents/)

## Project Overview

Production-grade monitoring agent designed to maintain system reliability Service Level Objectives (SLOs) on Ubuntu Linux servers. This toolkit provides comprehensive observability through real-time resource utilization tracking (CPU, memory, disk), critical service health monitoring (nginx, Docker, SSH), and security event detection from authentication logs.

Key capabilities include:
- **Proactive alerting** on threshold breaches to enable rapid incident response.
- **Automated self-healing** for degraded services via systemctl integration.
- **Structured JSONL logging** for downstream analysis (ELK, Prometheus).
- **Daily reliability reports** aggregating alert metrics.
- **Cron-scheduled execution** for continuous monitoring with minimal toil.

Built as an enterprise-ready internal tool demonstrating SRE best practices: error budgets via configurable thresholds, golden signals monitoring, and automation to reduce MTTR.

## Architecture Diagram

```
Automated Linux Reliability Monitoring Toolkit
├── config/
│   └── thresholds.json          # SLO thresholds (CPU:70%, Mem:80%, Disk:80%, Auth:5)
├── scripts/                     # Modular observers
│   ├── common.py               # Logging, alerting utils (JSONL, terminal 🚨)
│   ├── monitor_cpu.py          # psutil.cpu_percent()
│   ├── monitor_memory.py       # psutil.virtual_memory()
│   ├── monitor_disk.py         # psutil.disk_usage(/, /home)
│   ├── monitor_auth_logs.py    # tail /var/log/auth.log (Failed password)
│   ├── monitor_services.sh     # systemctl nginx/docker/ssh (check/restart)
│   ├── main_monitor.py         # Orchestrator + cron entrypoint
│   └── generate_summary.py     # Daily alert aggregation
├── logs/ (auto-created)         # JSONL: system_metrics.json, security_events.json, service_status.json
├── reports/ (auto-created)      # daily_summary.txt
└── README.md
```
*Data flows: Metrics → JSONL logs → Alerts → Reports. Observability pipeline ready for Prometheus pushgateway.*

## Features

- **Resource Monitoring**: Tracks CPU, memory, and disk I/O against SLO thresholds, logging golden signals.
- **Service Reliability**: Automated health checks and restarts for nginx, Docker, SSH to achieve 99.9% uptime SLO.
- **Security Observability**: Real-time failed login detection from `/var/log/auth.log` for threat hunting.
- **Incident Alerting**: Terminal notifications with simulated email dispatch on breaches.
- **Structured Logging**: JSONL format for easy parsing, querying, and integration with log aggregators.
- **Reporting**: Automated daily summaries of alert counts for post-incident reviews.
- **Configurability**: JSON thresholds for environment-specific SLOs.
- **Low-Toil Automation**: Cron-compatible, zero-infra deployment.

## Technology Stack

| Category          | Technologies                          |
|-------------------|---------------------------------------|
| Language          | Python 3.8+, Bash                     |
| Libraries         | psutil (system metrics), json, pathlib|
| Scheduling        | cron, systemctl                      |
| Logging           | JSONL (line-delimited JSON)           |
| OS                | Ubuntu Linux (systemd-based)          |
| SRE Patterns      | Self-healing, observability, SLOs     |

## Project Folder Structure

```
linux-reliability-monitor/
├── config/thresholds.json
├── scripts/
│   ├── __init__.py
│   ├── common.py
│   ├── monitor_cpu.py
│   ├── monitor_memory.py
│   ├── monitor_disk.py
│   ├── monitor_auth_logs.py
│   ├── monitor_services.sh
│   ├── main_monitor.py
│   └── generate_summary.py
├── logs/             # Auto-generated JSONL files
└── reports/          # Auto-generated summaries
```

## Monitoring Capabilities

- **CPU**: `psutil.cpu_percent(interval=1)` vs 70% threshold.
- **Memory**: `psutil.virtual_memory().percent` vs 80% threshold.
- **Disk**: `psutil.disk_usage('/')` and `/home` vs 80% used.
- **Authentication Logs**: `tail -n 100 /var/log/auth.log | grep 'Failed password'` count vs 5 attempts.
- **Services**: `systemctl is-active` for nginx, docker, ssh; auto-restart on failure.

All metrics logged with status (OK/ALERT).

## Alerting Strategy

1. **Threshold Evaluation**: On every cycle, compare metric vs config threshold.
2. **Notification**: 
   - Terminal: `🚨 ALERT 🚨 <metric>: <value>% > threshold <thresh>%`
   - Log: JSONL entry with `alert_status: "ALERT"`.
   - Email Simulation: Printed placeholder for smtplib integration.
3. **Self-Healing**: Service failures trigger `systemctl restart` with status logging.
4. **Escalation Readiness**: Logs structured for PagerDuty/Alertmanager.

## Logging Format Description

Structured JSONL (one JSON object per line) for machine readability:

**system_metrics.json**:
```json
{"timestamp":"2024-10-01T12:00:00","metric_name":"cpu_usage","metric_value":85.2,"threshold_value":70,"alert_status":"ALERT"}
```

**security_events.json**:
```json
{"timestamp":"2024-10-01T12:00:00","metric_name":"auth_failed_logins","metric_value":7,"threshold_value":5,"alert_status":"ALERT"}
```

**service_status.json**:
```json
{"timestamp":"2024-10-01T12:00:00","service":"nginx","status":"restarted_success"}
```

## Cron Automation Setup Instructions

1. Edit crontab: `crontab -e`
2. Add (runs every 5 minutes):
   ```
   */5 * * * * cd /Users/gunar/Desktop/Linux Reliability Monitoring Toolkit/linux-reliability-monitor && /usr/bin/python3 scripts/main_monitor.py >> logs/cron.log 2>&1
   ```
3. Verify: `crontab -l`

## Example Output

```
🚀 Starting Linux Reliability Monitoring...
🚨 ALERT 🚨 CPU Usage: 85.2% > threshold 70% at 2024-10-01T12:00:00
[EMAIL SIMULATION] Alert: CPU Usage violation!
✅ Monitoring cycle complete.
```

## How to Run Locally

### Prerequisites (Ubuntu)
```bash
sudo apt update && sudo apt install -y nginx docker.io openssh-server stress
pip3 install psutil
chmod +x linux-reliability-monitor/scripts/*.sh
cd linux-reliability-monitor
```

### Step-by-Step
1. `python3 scripts/main_monitor.py`  # Single cycle
2. Simulate incidents:
   - High CPU: `stress --cpu 8 --timeout 60s &`
   - Stop service: `sudo systemctl stop nginx`
   - Failed logins: SSH brute-force sim
3. Check `logs/*.json` and `reports/daily_summary.txt`

## Sample Alerts Section

**High Resource Alert**:
```
🚨 ALERT 🚨 Memory Usage: 82.1% > threshold 80% at 2024-10-01T12:05:00
```

**Service Failure**:
```
🚨 ALERT: Service nginx stopped!
Restarted nginx successfully.
{"timestamp":"...","service":"nginx","status":"restarted_success"}
```

**Security**:
```
🚨 ALERT 🚨 Failed SSH Logins: 7 > threshold 5
```

## Reliability Engineering Concepts Demonstrated

- **SLO Definition**: Configurable thresholds define acceptable error budgets.
- **Observability**: Metrics (psutil), logs (JSONL), traces (service restarts).
- **Error Budgets**: Alert only on SLO violations, allow bursts below threshold.
- **Toil Reduction**: Automated checks/reports eliminate manual `top`/`systemctl` usage.
- **Self-Healing**: Idempotent restarts reduce MTTR from hours to seconds.
- **Incident Response**: Structured logs enable quick root cause analysis.

## Future Improvements

- **Prometheus Integration**: Add `/metrics` exporter endpoint in `main_monitor.py`.
- **Grafana Dashboards**: Pre-built panels for golden signals.
- **Alertmanager**: Replace email sim with webhook.
- **Containerization**: Dockerfile for Kubernetes CronJob.
- **Distributed Tracing**: OpenTelemetry for multi-host fleets.

[Deploy Demo](https://github.com/Guna-Asher/linux-reliability-monitor) | [Live Logs](logs/) | Fork & Star 

