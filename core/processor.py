import json
import re
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
from .config import settings

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ensure_output_directory()

    def ensure_output_directory(self):
        """Ensure the output directory exists."""
        if not os.path.exists(settings.OUTPUT_DIR):
            os.makedirs(settings.OUTPUT_DIR)
            self.logger.info(f"✅ Created output directory: {settings.OUTPUT_DIR}")

    def extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from a response text."""
        if not response_text.strip():
            return None

        pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        match = re.search(pattern, response_text, re.DOTALL)

        cleaned_json = match.group(1) if match else response_text.strip()

        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError:
            self.logger.error(f"⚠️ Failed to decode response:\n{cleaned_json[:300]}")
            return None

    def save_data(self, data: Dict[str, Any], prefix: str = "data") -> str:
        """Save data to a file with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.json"
        filepath = os.path.join(settings.OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Saved data: {filepath}")
        return filepath

    def update_master_file(self, data: List[Dict[str, Any]]):
        """Update the master file with all data."""
        filepath = os.path.join(settings.OUTPUT_DIR, settings.MASTER_FILE)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"✅ Updated master file with {len(data)} records")

    def load_master_file(self) -> List[Dict[str, Any]]:
        """Load data from the master file."""
        filepath = os.path.join(settings.OUTPUT_DIR, settings.MASTER_FILE)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                self.logger.warning("⚠️ Existing master file is invalid, starting fresh")
        return []

    def create_backup(self, data: List[Dict[str, Any]]):
        """Create a timestamped backup of the data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.json"
        filepath = os.path.join(settings.OUTPUT_DIR, backup_file)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"✅ Created backup: {backup_file}") 