import os
import csv
from datetime import datetime
from typing import Dict, Any, Optional, List

def save_data_to_csv(data: List[Dict[str, Any]], filename: str) -> None:
    if not data:
        print("No data to save.")
        return

    # Generate directory name based on today's date
    date_str = datetime.today().strftime('%Y-%m-%d')
    dir_name = f"./data/{date_str}"

    dir_name = f"./data"

    os.makedirs(dir_name, exist_ok=True)  # Create the directory if it doesn't exist

    # Define file path
    file_path = os.path.join(dir_name, f"{filename}.csv")

    # Write data to CSV
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {file_path}")