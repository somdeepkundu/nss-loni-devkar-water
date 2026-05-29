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

## Scripts
- `scripts/crop_water_productivity.py` — CWP framework (FAO-56 ETc, crop ranking)
- `scripts/analyze_mi_census.py` — filters the 6th MI Census to Pune/Indapur/Loni Devkar and summarizes irrigation + groundwater (memory-safe chunked reads)
- `scripts/explore_mi_census.py` — inspects MI Census CSV structure without loading full files
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
- [ ] Export NSS data → load Pune district records
- [ ] Acquire remaining village sources (Agri Census, CGWB, Census 2011, IMD)
- [ ] Nearby-village water-table comparison (143 Indapur villages)
- [ ] Water-balance model (rainfall + ETc + groundwater draft)

## Getting Started
```bash
pip install -r requirements.txt
python scripts/crop_water_productivity.py   # see the CWP comparison
python scripts/analyze_mi_census.py         # rebuild the MI Census summary (needs raw CSVs in data/raw/mi_census_6th/)
```

The live site is in `index.html` (GitHub Pages). The processed analysis output
lives in `data/processed/`; the 1.3 GB raw census CSVs are gitignored.
