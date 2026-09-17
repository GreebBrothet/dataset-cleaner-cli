import json
import argparse
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class DatasetReport(BaseModel):
    total_rows: int
    total_columns: int
    missing_values_count: int
    duplicate_rows_count: int
    columns: List[str]

class QuickDatasetLint:
    """Utility for rapid dataset quality and structural integrity checks."""
    
    def __init__(self, filepath: str = ""):
        self.filepath = filepath
        self.data: List[Dict[str, Any]] = []

    def load_json(self) -> None:
        """Loads JSON data from specified path."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def analyze(self) -> DatasetReport:
        if not self.data:
            raise ValueError("Dataset is empty or was not loaded properly.")

        columns = list(self.data[0].keys())
        total_rows = len(self.data)
        
        missing_count = 0
        seen = set()
        duplicates = 0

        for row in self.data:
            row_str = json.dumps(row, sort_keys=True)
            if row_str in seen:
                duplicates += 1
            else:
                seen.add(row_str)

            for val in row.values():
                if val is None or val == "":
                    missing_count += 1

        return DatasetReport(
            total_rows=total_rows,
            total_columns=len(columns),
            missing_values_count=missing_count,
            duplicate_rows_count=duplicates,
            columns=columns
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Dataset Linter & Sanitizer")
    parser.add_argument("--file", type=str, help="Path to target JSON dataset", required=False)
    args = parser.parse_args()

    sample_data = [
        {"id": 1, "prompt": "Explain gradient descent", "response": "Gradient descent is an optimization algorithm..."},
        {"id": 2, "prompt": "", "response": "Missing prompt sample"},
        {"id": 1, "prompt": "Explain gradient descent", "response": "Gradient descent is an optimization algorithm..."},
    ]
    
    print("=== AI Dataset Quality Audit ===")
    linter = QuickDatasetLint()
    linter.data = sample_data
    report = linter.analyze()
    print(report.model_dump_json(indent=2))
