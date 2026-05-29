"""
Load and explore NSS 77th Round state-level data
"""

import pandas as pd
import sys

def explore_excel_file(file_path):
    """Load and explore Excel file structure"""
    try:
        # Load the file to see sheet names
        excel_file = pd.ExcelFile(file_path)
        print("\n" + "="*70)
        print("EXCEL FILE STRUCTURE")
        print("="*70)
        print(f"File: {file_path}")
        print(f"\nSheet names ({len(excel_file.sheet_names)} sheets):")
        for i, sheet in enumerate(excel_file.sheet_names, 1):
            print(f"  {i}. {sheet}")

        # Load first sheet to understand structure
        df = pd.read_excel(file_path, sheet_name=0)
        print("\n" + "="*70)
        print(f"FIRST SHEET: '{excel_file.sheet_names[0]}'")
        print("="*70)
        print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"\nColumns:\n{list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head(10).to_string())

        # Check for Pune or Maharashtra
        if 'State' in df.columns or 'STATE' in df.columns:
            state_col = [c for c in df.columns if 'state' in c.lower()][0]
            print(f"\n{state_col} values (sample):")
            print(df[state_col].unique()[:10])

        if 'District' in df.columns or 'DISTRICT' in df.columns:
            dist_col = [c for c in df.columns if 'district' in c.lower()][0]
            print(f"\n{dist_col} values (sample):")
            print(df[dist_col].unique()[:10])

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    file_path = "C:\\Users\\Somdeep Kundu\\Downloads\\State_77.xlsx"
    explore_excel_file(file_path)
