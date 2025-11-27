# src/utils.py
from datetime import datetime

def parse_datetime(s: str):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")
