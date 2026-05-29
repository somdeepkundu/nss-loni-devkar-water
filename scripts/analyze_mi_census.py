"""
Filter & analyze 6th Minor Irrigation Census for Loni Devkar (Indapur, Pune).

- Extracts the LONI village row + all Indapur taluka villages from the
  Village Schedule.
- Chunk-reads the large GW/SW scheme files (filtered to PUNE/INDAPUR) so the
  933 MB Dug Wells file never loads fully into memory.
- Writes JSON + CSV summaries to data/processed/ for the GitHub Pages
  infographics.
- Corrected interpretation: wells are supplementary in the Ujjaini dam command,
  not primary source.
"""

VERSION = "1.1.0"  # Ujjaini dam context added; waterlogging-focused interpretation

import json
from pathlib import Path

import pandas as pd

RAW = Path("data/raw/mi_census_6th")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

DISTRICT = "PUNE"
TALUKA = "INDAPUR"
VILLAGE = "LONI"  # Loni Devkar is recorded simply as "LONI" in Indapur

SCHEME_FILES = {
    "Dug Wells": "MI6_GW_DGW_MH.csv",
    "Deep Tube Wells": "MI6_GW_DTW_MH.csv",
    "Medium Tube Wells": "MI6_GW_MTW_MH.csv",
    "Shallow Tube Wells": "MI6_GW_STW_MH.csv",
    "Surface Flow": "MI6_SW_SF_MH.csv",
    "Surface Lift": "MI6_SW_SL_MH.csv",
}

CHUNK = 100_000


def filter_village_schedule():
    df = pd.read_csv(RAW / "MHVillageSchedule.csv", low_memory=False)
    indapur = df[
        (df["district_name"] == DISTRICT)
        & (df["block_tehsil_name"].str.contains(TALUKA, case=False, na=False))
    ].copy()
    indapur.to_csv(OUT / "indapur_village_schedule.csv", index=False)
    return indapur


def scan_schemes():
    """Chunk-read each scheme file, keep only PUNE/INDAPUR rows."""
    results = {}
    for label, fname in SCHEME_FILES.items():
        fpath = RAW / fname
        if not fpath.exists():
            results[label] = None
            continue

        kept = []
        for chunk in pd.read_csv(fpath, chunksize=CHUNK, low_memory=False):
            mask = (chunk["district_name"] == DISTRICT) & (
                chunk["block_tehsil_name"].str.contains(TALUKA, case=False, na=False)
            )
            sub = chunk[mask]
            if len(sub):
                kept.append(sub)

        if kept:
            results[label] = pd.concat(kept, ignore_index=True)
        else:
            results[label] = pd.DataFrame()
        print(f"  {label}: {len(results[label])} Indapur scheme rows")
    return results


def summarize(indapur, schemes):
    loni_vs = indapur[indapur["village_name"] == VILLAGE]
    loni = loni_vs.iloc[0] if len(loni_vs) else None

    summary = {
        "location": {
            "district": DISTRICT,
            "taluka": TALUKA,
            "village": "Loni Devkar (LONI)",
            "census": "6th Minor Irrigation Census (ref. 2017-18)",
        },
        "loni_devkar": {},
        "indapur_context": {},
        "scheme_breakdown": {},
    }

    if loni is not None:
        summary["loni_devkar"] = {
            "geographical_area_ha": int(loni["geographical_area"]),
            "cultivable_area_ha": int(loni["cultivable_area"]),
            "net_sown_area_ha": int(loni["net_sown_area"]),
            "net_irrigated_area_ha": int(loni["net_irrigated_area"]),
            "gross_irrigated_total_ha": int(loni["gross_irrigated_area_total"]),
            "irrigated_kharif_ha": int(loni["gross_irrigated_area_kharif_season"]),
            "irrigated_rabi_ha": int(loni["gross_irrigated_area_rabi_season"]),
            "irrigated_perennial_ha": int(loni["gross_irrigated_area_perennial_season"]),
            "gw_level_pre_monsoon_m": float(loni["avg_ground_water_level_pre_monsoon"]),
            "gw_level_post_monsoon_m": float(loni["avg_ground_water_level_post_monsoon"]),
            "irrigation_intensity_pct": round(
                100 * loni["net_irrigated_area"] / loni["net_sown_area"], 1
            )
            if loni["net_sown_area"]
            else None,
        }

    # Indapur taluka aggregates
    summary["indapur_context"] = {
        "villages_count": int(len(indapur)),
        "total_net_sown_ha": int(indapur["net_sown_area"].sum()),
        "total_net_irrigated_ha": int(indapur["net_irrigated_area"].sum()),
        "avg_gw_pre_monsoon_m": round(
            indapur["avg_ground_water_level_pre_monsoon"].mean(), 1
        ),
        "avg_gw_post_monsoon_m": round(
            indapur["avg_ground_water_level_post_monsoon"].mean(), 1
        ),
        "avg_irrigation_intensity_pct": round(
            100
            * indapur["net_irrigated_area"].sum()
            / indapur["net_sown_area"].sum(),
            1,
        ),
    }

    # Scheme breakdown for Loni Devkar specifically
    loni_schemes = {}
    indapur_schemes = {}
    for label, df in schemes.items():
        if df is None or df.empty:
            loni_schemes[label] = 0
            indapur_schemes[label] = 0
            continue
        indapur_schemes[label] = int(len(df))
        loni_df = df[df["village_name"] == VILLAGE]
        loni_schemes[label] = int(len(loni_df))

    summary["scheme_breakdown"] = {
        "loni_devkar": loni_schemes,
        "indapur_taluka": indapur_schemes,
    }

    # Irrigation potential created vs utilized (IPC/IPU) where available
    ipc_ipu = {}
    for label, df in schemes.items():
        if df is None or df.empty:
            continue
        cols = df.columns
        ipc_col = next((c for c in cols if c.lower() == "ipc_total"), None)
        ipu_col = next((c for c in cols if c.lower() == "ipu_total"), None)
        if ipc_col and ipu_col:
            loni_df = df[df["village_name"] == VILLAGE]
            ipc_ipu[label] = {
                "indapur_ipc_ha": round(float(df[ipc_col].sum()), 1),
                "indapur_ipu_ha": round(float(df[ipu_col].sum()), 1),
                "loni_ipc_ha": round(float(loni_df[ipc_col].sum()), 1),
                "loni_ipu_ha": round(float(loni_df[ipu_col].sum()), 1),
            }
    summary["irrigation_potential"] = ipc_ipu

    return summary


def main():
    print("Filtering Village Schedule...")
    indapur = filter_village_schedule()
    print(f"  Indapur villages: {len(indapur)}")

    print("Scanning scheme files (chunked)...")
    schemes = scan_schemes()

    print("Summarizing...")
    summary = summarize(indapur, schemes)

    out_json = OUT / "loni_devkar_mi_census.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Written {out_json}")

    # Save per-village irrigation table for nearby-village comparison
    cols = [
        "village_name",
        "geographical_area",
        "net_sown_area",
        "net_irrigated_area",
        "gross_irrigated_area_total",
        "gross_irrigated_area_perennial_season",
        "avg_ground_water_level_pre_monsoon",
        "avg_ground_water_level_post_monsoon",
    ]
    indapur[cols].to_csv(OUT / "indapur_irrigation_by_village.csv", index=False)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
