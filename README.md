# Crop Water Productivity Analysis — Loni Deokar, Indapur, Pune

**Version 1.1.0** — Updated with Ujjaini dam hydrology, waterlogging-risk analysis, and 2025 La Niña crop loss data.

Analyzing and improving **crop water productivity** in Loni Deokar village (Indapur taluka, Pune district, Maharashtra) under **Ujjaini dam water-driven variability**. Loni Deokar is not water-scarce; it is **waterlogging-prone during high-release periods** and requires spatial crop zoning to turn water surplus into productivity. This analysis combines the 6th MI Census, digitised cadastral survey, 2025 La Niña crop-loss observations, and farm-level well-depth data (red-rock indicators).

**Live site:** https://somdeepkundu.github.io/nss-loni-devkar-water/ (MkDocs Material)

*Somdeep Kundu · RuDRA Lab · CTARA · IIT Bombay ·
[somdeep@iitb.ac.in](mailto:somdeep@iitb.ac.in) ·
[somdeepkundu.in](https://somdeepkundu.in) ·
[somdeepkundu.github.io](https://somdeepkundu.github.io)*

## Goal
Improve crop water productivity and reduce waterlogging risk through spatial crop zoning and data-driven hydrology:
- **Hydrology**: Ujjaini dam releases create waterlogging; wells supplement during low-release windows.
- **2025 La Niña**: Maize crop failure due to soil saturation in high-seepage zones; deep wells hit red-rock (iron-oxide) layers.
- **Crop adaptation**: Rice in waterlogged zones (flood-tolerant, ~20 Rs/m³); grapes/onion on elevated, well-drained plots (high value, requires drainage).
- **Water management**: Shift from "save water" (irrelevant) to "manage surplus and variability" (critical).

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

## Key Findings (6th MI Census + 2025 Field Data)

**Irrigation profile** (Loni Deokar within Ujjaini dam command):

| Metric | Loni Deokar | Indapur taluka avg | Interpretation |
|--------|-------------|---------------------|----|
| Irrigation source | **62 wells** | mixed | *Supplementary*; primary is dam seepage |
| Well depths | 23–60 m pre-monsoon | varies | Deep wells hit red-oxide rocks (iron hydroxide) |
| Ujjaini dam proximity | ~5–10 km upstream | — | Seepage feeds upper aquifer during releases |
| Monsoon recharge | ~2 m rise | ~2.1 m | **Dam-driven**, not rainfall-driven alone |
| 2025 La Niña | Maize waterlogging failure | — | Above-normal releases + monsoon = soil saturation |

**Takeaway:** Loni Deokar's primary challenge is **waterlogging under high-release periods**, not groundwater depletion. Crop choice and spatial zoning (rice in seepage zones, grapes on elevated land) are the primary levers. Well depths hitting red rocks indicate deeper aquifer is unsuitable for irrigation. Summary data: [data/processed/loni_devkar_mi_census.json](data/processed/loni_devkar_mi_census.json).

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
`main`. It embeds the interactive Leaflet cadastral map, waterlogging-risk + crop-zone overlays, Chart.js visualisations, and a full **References & Citation** page with version history.

```bash
pip install mkdocs-material
mkdocs serve     # preview at http://127.0.0.1:8001
mkdocs build     # output to site/ (gitignored)
```

> **One-time setup:** in the repo's **Settings → Pages**, set *Source* to
> **GitHub Actions** (instead of "Deploy from a branch"). Until then the old
> root `index.html` is what Pages serves.

**Citation (v1.1.0):** Kundu, S. (2026). *Crop Water Productivity in Loni Deokar
(Indapur, Pune): Waterlogging Risk, Ujjaini Dam Hydrology, and Crop-Choice Adaptation.* RuDRA Lab, CTARA, IIT Bombay. See the
[References page](web/references.md) and [CHANGELOG](CHANGELOG.md) for version history.

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

## Status (v1.1.0)

### Completed
- [x] Repo + structure set up
- [x] NSS 77th Round downloaded; technical PDFs converted to markdown
- [x] CWP + flood-tolerance analysis framework built
- [x] 6th MI Census filtered for Loni Deokar / Indapur (Ujjaini dam command context)
- [x] Irrigation + waterlogging findings published to MkDocs site
- [x] Village cadastral map (1,045 plots, 1,059 labels; UTM 43N → WGS-84)
- [x] 2025 La Niña crop-loss data integrated (maize waterlogging)
- [x] Red-rock (iron-oxide aquifer) well-depth observations added
- [x] Spatial crop zoning (rice/grapes/onion by hydrologic zone) framework
- [x] Version tracking (1.1.0) across all files + CHANGELOG

### Pending
- [ ] Ujjaini dam release schedule (monthly/seasonal data from MWR Dept)
- [ ] Waterlogging-risk zone mapping (topography + seepage patterns)
- [ ] Well-depth survey completion (arsenic/iron/pH profile)
- [ ] NSS 77th Round export & Pune district farm household benchmarking
- [ ] Agricultural Census 2015–16 crop-area breakdown by zone
- [ ] Water-balance model (dam releases + monsoon + ETc + draft)

## Getting Started
```bash
pip install -r requirements.txt
python scripts/crop_water_productivity.py   # see the CWP comparison
python scripts/analyze_mi_census.py         # rebuild the MI Census summary (needs raw CSVs in data/raw/mi_census_6th/)
python scripts/gpkg_to_geojson.py           # rebuild the village map GeoJSON (needs the .gpkg)
```

The live site is in `index.html` (GitHub Pages). The processed analysis output
lives in `data/processed/`; the 1.3 GB raw census CSVs are gitignored.
