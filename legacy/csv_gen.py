import csv
from pathlib import Path
from datetime import datetime, timezone
import random

# Требование: CSV
# 1) Время и даты: timestamp
# 2) Логические блоки: ИСТИНА / ЛОЖЬ
# 3) Числа: числовой формат
# 4) Строки: текст

HEADERS = ["timestamp", "flag", "value", "text"]

def generate_row(i: int):
    ts = int(datetime.now(timezone.utc).timestamp()) - random.randint(0, 86400)
    flag = "ИСТИНА" if random.random() > 0.5 else "ЛОЖЬ"
    value = round(random.uniform(-1000, 1000), 3)  # число
    text = f"row_{i}"
    return [ts, flag, value, text]

def generate_csv(path: Path, rows: int = 20):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(HEADERS)
        for i in range(rows):
            w.writerow(generate_row(i))
