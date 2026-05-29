"""
Load and standardize village-level data sources for Loni Devkar, Indapur, Pune.

As you download each source (MI Census, Agri Census, CGWB, etc.), this script
will help load, filter to Indapur/Loni Devkar, and prepare for CWP analysis.
"""

import pandas as pd
from pathlib import Path


class VillageDataLoader:
    """Load and standardize village-level agricultural & water data."""

    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)

    def load_mi_census(self, filename="mi_census_6th_indapur_villages.csv"):
        """
        Load 6th Minor Irrigation Census village schedule.

        Expected columns (may vary by download format):
          - village_name, taluka, district, state (or similar)
          - dug_wells, tube_wells, bore_wells, lift_schemes, canal_irrigation
          - area_irrigated (hectares), scheme_status
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] MI Census not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] MI Census: {df.shape[0]} rows, {df.shape[1]} cols")

        # Filter to Loni Devkar if village column present
        if "village_name" in df.columns or "village" in df.columns:
            vcol = [c for c in df.columns if "village" in c.lower()][0]
            loni_rows = df[df[vcol].str.contains("Loni|loni", na=False)]
            if len(loni_rows) > 0:
                print(f"  -> Found {len(loni_rows)} row(s) for Loni Devkar")
                return loni_rows
        return df

    def load_agri_census(self, filename="agri_census_2015_16_indapur.csv"):
        """
        Load Agricultural Census 2015-16 (Indapur).

        Expected columns (varies by table):
          - holding_size_class, irrigated_area, rain_fed_area
          - crop_name, area_ha, number_of_holdings
          - irrigation_source (well, tube_well, canal, tank, etc.)
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] Agri Census not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] Agri Census: {df.shape[0]} rows, {df.shape[1]} cols")
        return df

    def load_cgwb_status(self, filename="cgwb_gw_status_indapur.csv"):
        """
        Load CGWB groundwater status (Indapur block).

        Expected columns:
          - block, tahsil (or taluka)
          - pre_monsoon_gwl_mbgl, post_monsoon_gwl_mbgl (meters below GL)
          - stage_of_extraction (%), category (Safe/Semi-critical/Over-exploited)
          - year
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] CGWB status not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] CGWB: {df.shape[0]} rows, {df.shape[1]} cols")
        return df

    def load_census_village(self, filename="census_2011_loni_devkar.csv"):
        """
        Load Census 2011 Village Directory for Loni Devkar.

        Expected columns:
          - village_code, village_name, taluka, district
          - population, households, area_sq_km
          - irrigated_area, cultivated_area
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] Census village not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] Census 2011: {df.shape[0]} rows, {df.shape[1]} cols")
        return df

    def load_icrisat_crops(self, filename="icrisat_pune_district_crops.csv"):
        """
        Load ICRISAT district-level crop data (Pune).

        Expected columns:
          - year, crop, area_ha, production_tonnes, yield_kg_ha
          - irrigated_area_ha (if available)
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] ICRISAT crops not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] ICRISAT: {df.shape[0]} rows, {df.shape[1]} cols")
        return df

    def load_imd_rainfall(self, filename="imd_rainfall_indapur.csv"):
        """
        Load IMD rainfall data (Indapur or nearby station).

        Expected columns:
          - year, month, rainfall_mm (or date, rainfall)
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"[SKIP] IMD rainfall not found: {filename}")
            return None

        df = pd.read_csv(filepath)
        print(f"[LOAD] IMD rainfall: {df.shape[0]} rows, {df.shape[1]} cols")
        return df

    def load_all(self):
        """Load all available sources. Returns dict of DataFrames."""
        sources = {
            "mi_census": self.load_mi_census(),
            "agri_census": self.load_agri_census(),
            "cgwb": self.load_cgwb_status(),
            "census_village": self.load_census_village(),
            "icrisat": self.load_icrisat_crops(),
            "imd_rainfall": self.load_imd_rainfall(),
        }
        # Filter out None values
        return {k: v for k, v in sources.items() if v is not None}


def print_status():
    """Check which data files are present in data/raw/."""
    print("\n" + "=" * 70)
    print("DATA ACQUISITION STATUS")
    print("=" * 70)

    expected_files = {
        "mi_census_6th_indapur_villages.csv": "6th MI Census (village)",
        "agri_census_2015_16_indapur.csv": "Agricultural Census 2015-16",
        "cgwb_gw_status_indapur.csv": "CGWB groundwater status",
        "census_2011_loni_devkar.csv": "Census 2011 village directory",
        "icrisat_pune_district_crops.csv": "ICRISAT Pune crops (1990–2020)",
        "imd_rainfall_indapur.csv": "IMD rainfall (Indapur)",
    }

    raw_dir = Path("data/raw")
    present = []
    missing = []

    for filename, description in expected_files.items():
        if (raw_dir / filename).exists():
            present.append(description)
            print(f"[OK] {description}")
        else:
            missing.append(description)
            print(f"[ ] {description}")

    print("\n" + "-" * 70)
    print(f"Present: {len(present)}/{len(expected_files)}")
    print(f"Missing: {len(missing)}/{len(expected_files)}")
    print("\nNext: download missing files from docs/DATA_ACQUISITION_GUIDE.md")
    print("=" * 70)

    return present, missing


if __name__ == "__main__":
    # Check what's available
    print_status()

    # Try loading whatever is present
    loader = VillageDataLoader()
    data = loader.load_all()

    if data:
        print(f"\nLoaded {len(data)} data source(s):")
        for name, df in data.items():
            if df is not None:
                print(f"  - {name}: {df.shape}")
    else:
        print("\nNo data files found yet. Start downloading from DATA_ACQUISITION_GUIDE.md")
