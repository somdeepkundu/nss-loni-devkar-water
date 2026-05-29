"""
Crop Water Productivity (CWP) analysis framework for Loni Devkar, Indapur, Pune.

Implements the standard definitions used in agricultural water management:

    CWP_physical = Yield (kg/ha)        / Water (m3/ha)   -> kg/m3
    CWP_economic = Crop value (Rs/ha)   / Water (m3/ha)   -> Rs/m3

"Water" can be (be explicit which one you report):
    1. Irrigation applied   (from MI Census / NSS)
    2. ETc  = ET0 * Kc      (crop consumptive use, FAO-56)
    3. Total = effective rainfall + irrigation

This module provides:
  - FAO-56 crop coefficients (Kc) for crops common in Indapur
  - Seasonal crop water requirement (ETc) estimation
  - CWP calculators
  - A comparison table to rank crops by water productivity
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Crop coefficients (Kc) and typical season length for crops grown in
# Indapur taluka (drought-prone eastern Pune, Bhima/Ujani command).
# Kc values are FAO-56 mid-season; season_days = total growing period.
# These are planning defaults — refine with local agri-dept data.
# ---------------------------------------------------------------------------
@dataclass
class Crop:
    name: str
    kc_mid: float          # FAO-56 mid-season crop coefficient
    season_days: int       # total growing period (days)
    typical_yield_t_ha: float   # typical local yield (tonnes/ha)
    price_rs_per_kg: float      # farm-gate price (Rs/kg)
    note: str = ""


# Indapur-relevant crops. Sugarcane is the dominant (and thirstiest) crop.
CROPS = {
    "sugarcane": Crop("Sugarcane", kc_mid=1.25, season_days=365,
                      typical_yield_t_ha=80.0, price_rs_per_kg=3.1,
                      note="Dominant cash crop; very high water use, ~12-month crop"),
    "jowar": Crop("Jowar (sorghum)", kc_mid=1.00, season_days=120,
                  typical_yield_t_ha=2.5, price_rs_per_kg=25.0,
                  note="Traditional rabi staple; drought-tolerant"),
    "bajra": Crop("Bajra (pearl millet)", kc_mid=1.00, season_days=95,
                  typical_yield_t_ha=2.0, price_rs_per_kg=24.0,
                  note="Low water need; kharif"),
    "wheat": Crop("Wheat", kc_mid=1.15, season_days=120,
                  typical_yield_t_ha=3.5, price_rs_per_kg=24.0,
                  note="Rabi, irrigated"),
    "maize": Crop("Maize", kc_mid=1.20, season_days=110,
                  typical_yield_t_ha=5.0, price_rs_per_kg=20.0,
                  note="Kharif/rabi fodder & grain"),
    "onion": Crop("Onion", kc_mid=1.05, season_days=150,
                  typical_yield_t_ha=25.0, price_rs_per_kg=15.0,
                  note="High-value; major in Pune district"),
    "soybean": Crop("Soybean", kc_mid=1.15, season_days=100,
                    typical_yield_t_ha=2.2, price_rs_per_kg=42.0,
                    note="Kharif oilseed"),
    "tur": Crop("Tur (pigeon pea)", kc_mid=1.10, season_days=160,
                typical_yield_t_ha=1.2, price_rs_per_kg=65.0,
                note="Pulse; drought-hardy"),
    "grapes": Crop("Grapes", kc_mid=0.85, season_days=300,
                   typical_yield_t_ha=25.0, price_rs_per_kg=45.0,
                   note="High-value horticulture; drip-irrigated"),
}


def crop_etc_mm(crop: Crop, et0_mm_per_day: float) -> float:
    """
    Seasonal crop evapotranspiration (mm) using simplified FAO-56:
        ETc_season ~= ET0_daily * Kc_mid * season_days

    NOTE: This uses Kc_mid across the season as a planning approximation.
    For precision, split into initial/dev/mid/late stages with stage Kc.

    et0_mm_per_day: reference ET (Penman-Monteith). Indapur ~5-6 mm/day avg.
    """
    return et0_mm_per_day * crop.kc_mid * crop.season_days


def mm_to_m3_per_ha(depth_mm: float) -> float:
    """1 mm of water over 1 ha = 10 m3.  (1 ha = 10,000 m2; 1mm = 0.001 m)"""
    return depth_mm * 10.0


def cwp_physical(yield_t_ha: float, water_m3_ha: float) -> float:
    """Physical crop water productivity in kg/m3."""
    if water_m3_ha <= 0:
        return float("nan")
    return (yield_t_ha * 1000.0) / water_m3_ha


def cwp_economic(yield_t_ha: float, price_rs_kg: float, water_m3_ha: float) -> float:
    """Economic crop water productivity in Rs/m3."""
    if water_m3_ha <= 0:
        return float("nan")
    value_rs_ha = yield_t_ha * 1000.0 * price_rs_kg
    return value_rs_ha / water_m3_ha


def build_comparison(et0_mm_per_day: float = 5.5,
                     effective_rain_mm: float = 0.0) -> list:
    """
    Build a CWP comparison across crops using ETc as the water basis.

    et0_mm_per_day: average reference ET for Indapur (default 5.5).
    effective_rain_mm: seasonal effective rainfall to subtract from ETc to get
        net irrigation requirement (default 0 = report gross ETc).
    Returns list of dicts, ranked by economic CWP (Rs/m3) descending.
    """
    rows = []
    for key, crop in CROPS.items():
        etc_mm = crop_etc_mm(crop, et0_mm_per_day)
        net_irr_mm = max(etc_mm - effective_rain_mm, 0.0)
        water_m3 = mm_to_m3_per_ha(etc_mm)            # consumptive basis
        irr_m3 = mm_to_m3_per_ha(net_irr_mm)          # net irrigation basis

        rows.append({
            "crop": crop.name,
            "season_days": crop.season_days,
            "kc_mid": crop.kc_mid,
            "ETc_mm": round(etc_mm, 0),
            "ETc_m3_ha": round(water_m3, 0),
            "net_irr_m3_ha": round(irr_m3, 0),
            "yield_t_ha": crop.typical_yield_t_ha,
            "price_rs_kg": crop.price_rs_per_kg,
            "CWP_kg_per_m3": round(cwp_physical(crop.typical_yield_t_ha, water_m3), 3),
            "CWP_rs_per_m3": round(cwp_economic(crop.typical_yield_t_ha,
                                                crop.price_rs_per_kg, water_m3), 2),
            "note": crop.note,
        })

    rows.sort(key=lambda r: r["CWP_rs_per_m3"], reverse=True)
    return rows


def print_comparison(et0_mm_per_day: float = 5.5):
    rows = build_comparison(et0_mm_per_day)
    print("\n" + "=" * 100)
    print(f"CROP WATER PRODUCTIVITY COMPARISON - Indapur (ET0={et0_mm_per_day} mm/day)")
    print("Water basis = seasonal ETc (consumptive use). Planning estimates only.")
    print("=" * 100)
    hdr = f"{'Crop':<18}{'Season':>7}{'ETc(mm)':>9}{'ETc m3/ha':>11}{'Yield t/ha':>11}{'kg/m3':>8}{'Rs/m3':>9}"
    print(hdr)
    print("-" * 100)
    for r in rows:
        print(f"{r['crop']:<18}{r['season_days']:>7}{r['ETc_mm']:>9.0f}"
              f"{r['ETc_m3_ha']:>11.0f}{r['yield_t_ha']:>11.1f}"
              f"{r['CWP_kg_per_m3']:>8.3f}{r['CWP_rs_per_m3']:>9.2f}")
    print("-" * 100)
    print("\nReading this table:")
    print("  - kg/m3  = physical water productivity (food per drop)")
    print("  - Rs/m3  = economic water productivity (income per drop)")
    print("  - Sugarcane usually shows LOW Rs/m3 despite high revenue - it drinks")
    print("    enormous water. Crops near the TOP earn more income per m3 of water.")
    print("\nNOTE: replace default yields/prices/ET0 with Loni Devkar actuals once")
    print("      NSS, MI-Census and IMD data are loaded (see docs/DATA_SOURCES.md).")


if __name__ == "__main__":
    # Indapur reference ET ~5.5 mm/day (semi-arid). Refine with IMD data.
    print_comparison(et0_mm_per_day=5.5)
