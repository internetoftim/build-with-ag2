#!/bin/bash

echo "===== System Information ====="
echo "Date and Time: $(date)"
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo "CPU: $(grep 'model name' /proc/cpuinfo | head -1 | cut -d ':' -f2 | xargs)"
echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "Disk Usage: $(df -h | grep '/$' | awk '{print $5}')"

echo "\n===== Network Information ====="
echo "IP Address: $(hostname -I 2>/dev/null || echo 'Not available')"

echo "\n===== Current Directory ====="
pwd
ls -la | head -10
