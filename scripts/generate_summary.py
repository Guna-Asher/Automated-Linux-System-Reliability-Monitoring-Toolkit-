#!/usr/bin/env python3
"""
Standalone summary generator.
"""
import sys
sys.path.insert(0, '.')  
from scripts.main_monitor import generate_summary

if __name__ == '__main__':
    generate_summary()
    print("Summary generated in reports/daily_summary.txt")

