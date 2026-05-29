# Crop Water Productivity Analysis — Loni Devkar, Indapur, Pune

Analyzing and improving **crop water productivity** in Loni Devkar village
(Indapur taluka, Pune district, Maharashtra) using NSS and complementary
village/block-level agricultural & water datasets.

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

## Scripts
- `scripts/crop_water_productivity.py` — CWP framework (FAO-56 ETc, crop ranking)
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
- [ ] Export NSS data → load Pune district records
- [ ] Acquire village/block sources (Agri Census, MI Census, CGWB)
- [ ] Compute Loni Devkar / Indapur water productivity & alternatives

## Getting Started
```bash
pip install -r requirements.txt
python scripts/crop_water_productivity.py   # see the CWP comparison
```
