"""
Explore 6th Minor Irrigation Census CSV structure (Maharashtra).
Reads headers + sample rows without loading the full (huge) files.
Writes a structure report to docs/mi_census_structure.txt
"""

import pandas as pd
from pathlib import Path
import io

DATA_DIR = Path("data/raw/mi_census_6th")

FILES = {
    "MHVillageSchedule.csv": "Village Schedule (master village list)",
    "MI6_GW_DGW_MH.csv": "Ground Water - Dug Wells",
    "MI6_GW_DTW_MH.csv": "Ground Water - Deep Tube Wells",
    "MI6_GW_MTW_MH.csv": "Ground Water - Medium Tube Wells",
    "MI6_GW_STW_MH.csv": "Ground Water - Shallow Tube Wells",
    "MI6_SW_SF_MH.csv": "Surface Water - Surface Flow",
    "MI6_SW_SL_MH.csv": "Surface Water - Surface Lift",
}


def explore():
    out = io.StringIO()
    out.write("=" * 80 + "\n")
    out.write("6th MINOR IRRIGATION CENSUS - MAHARASHTRA - STRUCTURE REPORT\n")
    out.write("=" * 80 + "\n\n")

    for fname, desc in FILES.items():
        fpath = DATA_DIR / fname
        out.write("-" * 80 + "\n")
        out.write(f"FILE: {fname}\n")
        out.write(f"DESC: {desc}\n")
        if not fpath.exists():
            out.write("  [NOT FOUND]\n\n")
            continue

        size_mb = fpath.stat().st_size / (1024 * 1024)
        out.write(f"SIZE: {size_mb:.1f} MB\n")

        # Read just first 5 rows to get structure
        try:
            df = pd.read_csv(fpath, nrows=5, low_memory=False)
        except Exception as e:
            # Try different encoding / separator
            try:
                df = pd.read_csv(fpath, nrows=5, encoding="latin1", low_memory=False)
            except Exception as e2:
                out.write(f"  [ERROR reading: {e2}]\n\n")
                continue

        out.write(f"COLUMNS ({len(df.columns)}): {list(df.columns)}\n")
        out.write("\nSAMPLE ROWS (first 3):\n")
        out.write(df.head(3).to_string())
        out.write("\n")

        # Identify location-related columns
        loc_cols = [c for c in df.columns if any(
            kw in str(c).lower() for kw in
            ["state", "dist", "village", "block", "taluk", "tehsil",
             "name", "code", "lgd"]
        )]
        out.write(f"\nLOCATION COLUMNS: {loc_cols}\n\n")

    report = out.getvalue()

    # Write report with UTF-8
    docs = Path("docs")
    docs.mkdir(exist_ok=True)
    report_path = docs / "mi_census_structure.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"Report written to {report_path}")

    # Also print a safe ASCII version
    print(report.encode("ascii", "replace").decode("ascii"))


if __name__ == "__main__":
    explore()
