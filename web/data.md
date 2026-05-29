# Data & Methods

## Two-tier data strategy

NSS gives **district context**; village/block sources give the **Loni Deokar
specifics**. The analysis combines them.

| Tier | Question it answers | Source |
|------|---------------------|--------|
| District (NSS) | What do typical Pune farm households look like? | NSS 77th Round |
| Village / block | What is actually happening in Loni Deokar / Indapur? | 6th MI Census, Agri Census, CGWB, Census 2011 |
| Biophysical | How much water do crops need vs. get? | IMD rainfall, FAO-56 ETc |

## Acquisition status

=== "Processed ✅"

    - **6th Minor Irrigation Census** — filtered to Pune/Indapur/Loni Deokar; 62 wells, 100% groundwater, 23 m water table. `scripts/analyze_mi_census.py`
    - **Village cadastral map** — 1,045 plots digitised from `LONI-DEOKAR.dwg`, reprojected UTM 43N → WGS-84. `scripts/gpkg_to_geojson.py`
    - **FAO-56 crop-water model** — Kc values for nine local crops. `scripts/crop_water_productivity.py`

=== "Pending ⏳"

    - **NSS 77th Round** — downloaded; awaiting Nesstar Explorer export.
    - **Agricultural Census 2015–16** — Pune/Indapur crop-area tables.
    - **CGWB** — Indapur block groundwater category & extraction stage.
    - **IMD rainfall** — for the water-balance model.
    - **Census 2011** — Loni Deokar village directory & demographics.

## Methods

### Irrigation profile
The 6th MI Census ships seven Maharashtra CSVs (~1.3 GB). The large
ground-water scheme files are read in chunks and filtered to Pune/Indapur so
the 933 MB Dug Wells file never loads fully into memory. Per-village irrigation
area and groundwater levels come from the Village Schedule.

### Cadastral map
The CAD-derived GeoPackage was tagged EPSG:4326 but its coordinates are
actually **UTM Zone 43N metres (EPSG:32643)** — a common DWG-export mislabel,
and the reason the data never appeared on a normal map. The converter reads the
GeoPackage WKB blobs directly from SQLite (no GDAL), parses the CompoundCurve /
CircularString / CurvePolygon geometries, reprojects with `pyproj`, and clips
out stray (0,0)-origin vertices.

### Crop water productivity
Reference evapotranspiration (ET₀ ≈ 5.5 mm/day, Indapur semi-arid) is scaled by
crop coefficients (Kc) to crop ET (ETc = ET₀ × Kc), converted to m³/ha
(1 mm/ha = 10 m³), and divided into yield and value to give physical (kg/m³)
and economic (Rs/m³) productivity.

!!! note "Reproducibility"
    All processing scripts live in [`scripts/`](https://github.com/somdeepkundu/nss-loni-devkar-water/tree/main/scripts).
    The raw 1.3 GB census CSVs are gitignored; processed summaries and GeoJSON
    are committed under `data/processed/`.
