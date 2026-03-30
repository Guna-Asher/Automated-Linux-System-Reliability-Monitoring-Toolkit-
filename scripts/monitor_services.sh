#!/bin/bash
# Service monitoring and auto-restart for nginx, docker, ssh.

set -euo pipefail

LOGS_DIR="logs"
mkdir -p "$LOGS_DIR"

log_event() {
    local service="$1"
    local status="$2"
    local timestamp=$(date -Iseconds)
    echo "{\"timestamp\":\"$timestamp\",\"service\":\"$service\",\"status\":\"$status\"}" >> "$LOGS_DIR/service_status.json"
}

services=("nginx" "docker" "ssh")

for service in "${services[@]}"; do
    if systemctl is-active --quiet "$service"; then
        log_event "$service" "running"
        echo "Service $service: OK"
    else
        echo "🚨 ALERT: Service $service stopped!"
        log_event "$service" "stopped"
        
        # Attempt restart
        if systemctl restart "$service"; then
            log_event "$service" "restarted_success"
            echo "Restarted $service successfully."
        else
            log_event "$service" "restart_failed"
            echo "Failed to restart $service."
        fi
    fi
done

