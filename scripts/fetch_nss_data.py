"""
Fetch NSS (National Sample Survey) data for Pune district, Loni Dewakar region
Focus: Agricultural practices, water usage, crop patterns (NSS 77th Round 2019-20)
"""

import os
import requests
import pandas as pd
from pathlib import Path

# NSS Data Sources
NSS_SOURCES = {
    "77th_round": {
        "year": "2019-20",
        "description": "NSS 77th Round - Consumer Expenditure Survey",
        "url": "https://nss.mospi.gov.in/",
    }
}

PUNE_DISTRICT_CODE = "27"  # Maharashtra state=27, Pune district
LONI_DEWAKAR_CODES = {
    "taluka": "Shirur",  # Approximate taluka for Loni Dewakar
    "village": "Loni Dewakar"
}

class NSSDataFetcher:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_nss_metadata(self):
        """Fetch available NSS datasets for Pune"""
        print("NSS Data Sources for Pune District (77th Round 2019-20)")
        print("-" * 60)
        for key, info in NSS_SOURCES.items():
            print(f"Round: {key}")
            print(f"  Year: {info['year']}")
            print(f"  Description: {info['description']}")
            print(f"  Source: {info['url']}")

        return NSS_SOURCES

    def create_sample_structure(self):
        """Create sample CSV structure for NSS agricultural data"""
        # Create a template structure for NSS agricultural data
        sample_data = {
            "household_id": [f"HH_{i}" for i in range(1, 11)],
            "district": ["Pune"] * 10,
            "taluka": [LONI_DEWAKAR_CODES["taluka"]] * 10,
            "village": [LONI_DEWAKAR_CODES["village"]] * 10,
            "household_size": [4, 5, 3, 6, 4, 5, 7, 4, 3, 5],
            "agriculture_main_activity": ["Yes"] * 10,
            "primary_crop": ["Sugar cane", "Jowar", "Maize", "Sugar cane", "Vegetables",
                           "Jowar", "Sugar cane", "Maize", "Groundnut", "Sugar cane"],
            "irrigated_area_ha": [1.5, 0.5, 1.0, 2.0, 0.3, 0.8, 1.8, 0.6, 0.9, 1.2],
            "total_cultivated_area_ha": [2.0, 1.2, 1.5, 2.5, 0.5, 1.0, 2.2, 1.0, 1.2, 1.5],
            "annual_water_usage_m3": [15000, 5000, 8000, 20000, 2000, 7000, 18000, 6000, 7000, 12000],
            "irrigation_source": ["Well", "Borewell", "Canal", "Well", "Canal",
                                "Borewell", "Well", "Canal", "Borewell", "Well"],
        }

        df = pd.DataFrame(sample_data)
        output_path = self.output_dir / "nss_77_pune_agriculture_sample.csv"
        df.to_csv(output_path, index=False)
        print(f"\n[OK] Sample NSS data structure created: {output_path}")
        return df

    def fetch_real_data(self):
        """
        Instructions to fetch actual NSS data
        """
        print("\nTo fetch actual NSS data:")
        print("-" * 60)
        print("1. Visit: https://nss.mospi.gov.in/nss_documents.html")
        print("2. Download NSS 77th Round (2019-20) data files")
        print("3. Filter for Pune district (District Code: 27)")
        print("4. Extract relevant agricultural variables")
        print("\nKey variables for water productivity analysis:")
        print("  - Area under irrigation")
        print("  - Primary crop cultivated")
        print("  - Irrigation method")
        print("  - Water source (well, borewell, canal, etc.)")
        print("  - Household income from agriculture")

if __name__ == "__main__":
    fetcher = NSSDataFetcher()

    # Show available sources
    fetcher.fetch_nss_metadata()

    # Create sample data structure
    sample_df = fetcher.create_sample_structure()
    print(f"\nSample data shape: {sample_df.shape}")
    print("\nFirst few rows:")
    print(sample_df.head())

    # Instructions for real data
    fetcher.fetch_real_data()
