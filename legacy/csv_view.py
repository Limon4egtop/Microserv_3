from pathlib import Path
import csv
from rich.console import Console
from rich.table import Table

def view_csv(path: Path):
    console = Console()
    with path.open("r", encoding="utf-8") as f:
        r = csv.reader(f)
        headers = next(r)
        table = Table(title=str(path))
        for h in headers:
            table.add_column(h, overflow="fold")
        for row in r:
            table.add_row(*[str(x) for x in row])
    console.print(table)
