# Data & Methods

**Version: 1.2.0** — Updated with field-relevant crops: sugarcane, maize, pomegranate, banana, elephant grass, mulberry.

## Ujjaini dam command zone context

Loni Deokar is located within the **Ujjaini (Ujni) dam command zone** on the Bhima River (Indapur taluka, Pune). Ujjaini dam was constructed in 1858 and releases water into canals and seepage zones that recharge Loni Deokar's upper aquifer. This makes the village's hydrology **dam-driven**, not rainfall-dependent alone.

**Key facts**:
- Monsoon releases (June–September) create seepage and surface flooding.
- Post-monsoon releases (October–May) sustain well irrigation.
- 2025 La Niña event brought above-normal rainfall + dam releases, causing waterlogging and maize crop failure.

## Two-tier data strategy

NSS gives **district context**; village/block sources + dam data give the **Loni Deokar specifics**. The analysis combines all three.

| Tier | Question it answers | Source |
|------|---------------------|--------|
| District (NSS) | What do typical Pune farm households look like? | NSS 77th Round |
| Village / dam command | What is happening in Loni Deokar / Ujjaini zone? | 6th MI Census, Agri Census, CGWB, Ujjaini dam release schedule |
| Biophysical | Water surplus/deficit, crop suitability, waterlogging risk | Topography, soils, La Niña impacts, well-depth surveys |

## Acquisition status

=== "Processed ✅"

    - **6th Minor Irrigation Census** — filtered to Pune/Indapur/Loni Deokar; 62 wells, surface + groundwater interaction, 23 m water table (pre-monsoon). `scripts/analyze_mi_census.py`
    - **Village cadastral map** — 1,045 plots digitised from `LONI-DEOKAR.dwg`, reprojected UTM 43N → WGS-84. `scripts/gpkg_to_geojson.py`
    - **Crop-zone suitability map** — three hydrologic zones with recommended crops: rice, sugarcane, mulberry, pomegranate, banana, elephant grass.
    - **2025 La Niña crop loss data** — maize waterlogging failure in high-seepage zones; red rocks (iron hydroxide) in deep wells; field-verified crop recommendations.
    - **Flood-tolerance crop framework** — six locally-viable crops ranked by water needs, flood tolerance, and economic productivity.

=== "Pending ⏳"

    - **Ujjaini dam release schedule** — monthly/seasonal water releases (Maharashtra Water Resources Department).
    - **Waterlogging risk zones** — derived from topography, seepage patterns, 2025 damage hotspots.
    - **Well-depth survey** — depths and aquifer characteristics (red rocks, iron/arsenic content) in deep wells.
    - **Agricultural Census 2015–16** — Pune/Indapur crop-area breakdown by zone.
    - **CGWB groundwater quality report** — Indapur block arsenic/iron/pH profile.
    - **IMD rainfall + Ujjaini release data** — water-balance model integrating dam + monsoon dynamics.
    - **Census 2011** — Loni Deokar village demographics & infrastructure.

## Methods

### Irrigation profile (corrected hydrology)

The 6th MI Census was interpreted through a **dam-command lens**, not a groundwater-scarcity lens. The 23 m pre-monsoon water table reflects prior high recharge from Ujjaini releases, not aquifer stress. The 62 wells function as **supplementary irrigation** during low-release windows, not the primary source.

Large ground-water scheme files are read in chunks (chunksize=100,000) and filtered to Pune/Indapur to avoid memory overflow of the 933 MB file.

### 2025 La Niña waterlogging impact

The 2025 monsoon brought above-normal rainfall and Ujjaini releases simultaneously:

- **Maize in flood-prone zones (high seepage areas) suffered anoxic soil conditions** and premature crop failure (death before physiological maturity).
- Farmers observed **red-oxide rock layers** at depths 40–60 m in newly dug wells, indicating iron-rich deeper aquifers and potential arsenic enrichment.
- Lesson: **Crop choice must prioritize flood tolerance in dam-command zones**, not just water productivity.

### Crop adaptation framework

Six field-viable crops ranked by:
1. **Water requirement** (m³/ha for Indapur semi-arid zone).
2. **Flood tolerance** (based on agronomic literature + 2025 field observations).
3. **Economic productivity** (Rs/ha and Rs/m³).
4. **Suitability to hydrologic zones** (seepage/intermediate/elevated).

**Recommended crops** (farmer-validated):
- **Rice** — Zone 1 (high-seepage); flood-excellent, stable market.
- **Mulberry** — Zone 2 (intermediate); flood-tolerant, high income, less water than sugarcane.
- **Sugarcane** — Zone 2 (intermediate, on raised beds); high income but water-intensive, risky in seepage.
- **Banana** — Zone 3 (elevated); premium price, requires perfect drainage.
- **Pomegranate** — Zone 3 (elevated); drought-tolerant, high value.
- **Elephant Grass** — All zones (field margins, erosion control, biogas feedstock).

### Cadastral map & red-rock zones

The CAD-derived GeoPackage (`LONI-DEOKAR.gpkg`) was tagged EPSG:4326 but actually contains UTM Zone 43N metres (EPSG:32643). The converter reads WKB blobs directly from SQLite, parses curved geometries, reprojects to WGS-84, and outputs GeoJSON overlaid with:

- **Waterlogging risk zones** (based on topography and 2025 damage reports).
- **Well-depth zones** (where red rocks appear).
- **Recommended crop zones** (rice, sugarcane, grapes, etc. by suitability).

!!! note "Reproducibility"
    All processing scripts live in [`scripts/`](https://github.com/somdeepkundu/nss-loni-devkar-water/tree/main/scripts).
    Scripts include VERSION tracking for reproducibility.
    Raw 1.3 GB MI Census CSVs are gitignored; processed summaries, GeoJSON, and analysis outputs are committed under `data/processed/`.
