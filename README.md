# Crop Water Productivity Analysis — Loni Devkar, Indapur, Pune

Analyzing and improving **crop water productivity** in Loni Devkar village
(Indapur taluka, Pune district, Maharashtra) using NSS and complementary
village/block-level agricultural & water datasets.

**Live site:** https://somdeepkundu.github.io/nss-loni-devkar-water/ (MkDocs Material)

*Somdeep Kundu · RuDRA Lab · CTARA · IIT Bombay ·
[somdeep@iitb.ac.in](mailto:somdeep@iitb.ac.in) ·
[somdeepkundu.in](https://somdeepkundu.in) ·
[somdeepkundu.github.io](https://somdeepkundu.github.io)*

## Goal
Improve crop water productivity (yield and income per m³ of water) through
data-driven insights on:
- Current crop choices and water use (sugarcane-dominant, drought-prone area)
- Irrigation practices and groundwater sustainability
- Water availability vs. crop demand (ETc-based)
- Higher-value, lower-water crop alternatives

## Location
Loni Devkar (Indapur taluka, Pune, pin 413132) — eastern Pune district in the
Bhima/Ujani command, semi-arid and groundwater-stressed. See
[docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for the full context.

## Data Strategy (two-tier)
| Tier | Provides | Source |
|------|----------|--------|
| District | Farm household crops/irrigation benchmarks | NSS 77th Round |
| Village/Block | Loni Devkar / Indapur specifics | Agri Census, 6th MI Census (village schedule), CGWB, Census 2011 |
| Biophysical | Crop water need vs. supply | IMD rainfall, FAO-56 ETc |

Full mapping: **[docs/DATA_SOURCES.md](docs/DATA_SOURCES.md)**

## Key Findings (6th Minor Irrigation Census, ref. 2017–18)
Loni Devkar's irrigation profile, extracted from the village schedule and the
groundwater/surface-water scheme files:

| Metric | Loni Devkar | Indapur taluka avg |
|--------|-------------|--------------------|
| Irrigation source | **100% groundwater** | mixed |
| Minor irrigation schemes | 61 dug wells + 1 deep tube well | — |
| Surface water schemes | **none** | 4,269 |
| Water table (pre-monsoon) | **23 m** | 17.4 m |
| Monsoon recharge | ~2 m (23 → 21 m) | ~2.1 m |
| Net irrigated area | 60 ha (100% of net sown) | — |

**Takeaway:** Loni Devkar draws *all* of its irrigation from a deeper,
slower-recharging aquifer than its neighbours, with no canal or surface-water
fallback. That makes crop choice (shifting away from water-guzzling sugarcane)
the village's primary lever against groundwater depletion. Summary data:
[data/processed/loni_devkar_mi_census.json](data/processed/loni_devkar_mi_census.json).

## Project Structure
```
├── data/
│   ├── raw/           # NSS .Nesstar + downloaded datasets
│   └── processed/     # Cleaned, analysis-ready data
├── notebooks/         # Jupyter exploration
├── scripts/           # Fetch / parse / analysis scripts
├── analysis/          # Outputs and insights
└── docs/              # NSS documentation (md) + strategy guides
```

## Website (MkDocs Material)
The public site is built with **MkDocs Material** from `web/` (`docs_dir: web`)
and deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to
`main`. It embeds the interactive Leaflet map, the Chart.js visualisations, and
a full **References & Citation** page.

```bash
pip install mkdocs-material
mkdocs serve     # preview at http://127.0.0.1:8000
mkdocs build     # output to site/ (gitignored)
```

> **One-time setup:** in the repo's **Settings → Pages**, set *Source* to
> **GitHub Actions** (instead of "Deploy from a branch"). Until then the old
> root `index.html` is what Pages serves.

**Citation:** Kundu, S. (2026). *Crop Water Productivity in Loni Deokar
(Indapur, Pune).* RuDRA Lab, CTARA, IIT Bombay. See the
[References page](web/references.md) for BibTeX.

## Village Map (cadastral)
The site now embeds an interactive Leaflet map of Loni Deokar's survey plots.
The source `LONI-DEOKAR.gpkg` (exported from a CAD `.dwg`) was tagged EPSG:4326
but its coordinates are actually **UTM Zone 43N metres (EPSG:32643)** — that
mislabel is why the data never showed up on a normal map. `scripts/gpkg_to_geojson.py`
reads the GeoPackage WKB blobs directly via SQLite, parses the CompoundCurve /
CircularString / CurvePolygon geometries, reprojects to WGS-84 with pyproj,
clips out the stray (0,0)-origin junk, and writes web-ready GeoJSON to
`data/processed/geo/` (1,045 plot boundaries + 1,059 survey-number labels).

## Scripts
- `scripts/crop_water_productivity.py` — CWP framework (FAO-56 ETc, crop ranking)
- `scripts/analyze_mi_census.py` — filters the 6th MI Census to Pune/Indapur/Loni Devkar and summarizes irrigation + groundwater (memory-safe chunked reads)
- `scripts/explore_mi_census.py` — inspects MI Census CSV structure without loading full files
- `scripts/gpkg_to_geojson.py` — converts the Loni Deokar CAD GeoPackage to reprojected GeoJSON for the web map (no GDAL needed; uses pyproj + a hand-rolled WKB parser)
- `scripts/parse_nss_metadata.py` — NSS DDI/XML metadata parser
- `scripts/explore_state_data.py` — Excel/data explorer
- `scripts/pdf_to_markdown.py` — converts NSS PDFs to markdown docs

## Key Docs
- [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) — master data strategy
- [docs/NSS_EXTRACTION_GUIDE.md](docs/NSS_EXTRACTION_GUIDE.md) — how to export the .Nesstar data
- [docs/README.md](docs/README.md) — NSS technical documentation index

## Status
- [x] Repo + structure set up
- [x] NSS 77th Round downloaded (.Nesstar, needs Explorer export)
- [x] NSS technical PDFs converted to markdown
- [x] CWP analysis framework built and tested
- [x] 6th MI Census acquired, filtered, and analyzed for Loni Devkar / Indapur
- [x] Irrigation findings published to the GitHub Pages site
- [x] Village cadastral map (CAD → reprojected GeoJSON → interactive Leaflet map)
- [ ] Export NSS data → load Pune district records
- [ ] Acquire remaining village sources (Agri Census, CGWB, Census 2011, IMD)
- [ ] Nearby-village water-table comparison (143 Indapur villages)
- [ ] Water-balance model (rainfall + ETc + groundwater draft)

## Getting Started
```bash
pip install -r requirements.txt
python scripts/crop_water_productivity.py   # see the CWP comparison
python scripts/analyze_mi_census.py         # rebuild the MI Census summary (needs raw CSVs in data/raw/mi_census_6th/)
python scripts/gpkg_to_geojson.py           # rebuild the village map GeoJSON (needs the .gpkg)
```

The live site is in `index.html` (GitHub Pages). The processed analysis output
lives in `data/processed/`; the 1.3 GB raw census CSVs are gitignored.
