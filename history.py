"""
History Module for MCTiers Application
Manages user interaction history
"""

import os
import csv
from datetime import datetime
from typing import List, Optional


class HistoryManager:
    """Manage user interaction history"""
    
    def __init__(self, filename: str = "history.csv"):
        """Initialize history manager"""
        self.filename = filename
        self.history = []
        self.load_from_file()
    
    def add_entry(self, action: str):
        """Add an entry to history"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] {action}"
        self.history.append(entry)
    
    def get_all(self) -> List[str]:
        """Get all history entries"""
        return self.history
    
    def get_last(self, n: int = 10) -> List[str]:
        """Get last n entries"""
        return self.history[-n:]
    
    def clear(self):
        """Clear history"""
        self.history = []
    
    def save_to_file(self):
        """Save history to CSV file"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'action'])
                for entry in self.history:
                    # Parse timestamp and action from entry
                    if entry.startswith('[') and '] ' in entry:
                        timestamp = entry[1:entry.find(']')]
                        action = entry[entry.find('] ') + 2:]
                        writer.writerow([timestamp, action])
            print(f"\nHistory saved to {self.filename}")
        except Exception as e:
            print(f"\nWarning: Could not save history - {e}")
    
    def load_from_file(self):
        """Load history from CSV file"""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        timestamp, action = row[0], row[1]
                        self.history.append(f"[{timestamp}] {action}")
        except Exception as e:
            print(f"Warning: Could not load history - {e}")