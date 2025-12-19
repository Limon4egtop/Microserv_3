import argparse
from pathlib import Path
from legacy.csv_gen import generate_csv
from legacy.csv_view import view_csv
from legacy.xlsx_export import csv_to_xlsx

def main():
    p = argparse.ArgumentParser(prog="legacy", description="Pascal-Legacy replacement utility")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Generate CSV with typed columns")
    g.add_argument("--rows", type=int, default=20)
    g.add_argument("--out", type=str, default="./data/sample.csv")

    v = sub.add_parser("view", help="Render CSV as table (console)")
    v.add_argument("--csv", type=str, required=True)

    x = sub.add_parser("to-xlsx", help="Convert CSV to XLSX with timestamp substitution")
    x.add_argument("--csv", type=str, required=True)
    x.add_argument("--out", type=str, default="./data/sample.xlsx")

    args = p.parse_args()
    if args.cmd == "generate":
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        generate_csv(out, rows=args.rows)
        print(f"CSV written: {out}")
    elif args.cmd == "view":
        view_csv(Path(args.csv))
    elif args.cmd == "to-xlsx":
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        csv_to_xlsx(Path(args.csv), out)
        print(f"XLSX written: {out}")
