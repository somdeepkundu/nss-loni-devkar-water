# Village-Level Data Acquisition — Loni Devkar, Indapur, Pune

Actionable guide to download and organize all village/block-level agricultural &
water data for Loni Devkar (Indapur taluka, Pune district).

**Target location codes:**
- State: Maharashtra (27)
- District: Pune (27-03)
- Taluka: Indapur
- Village: Loni Devkar (Loni Deokar / Loni Devkar)
- Pincode: 413132

---

## Source 1: 6th Minor Irrigation Census — Village Schedule ⭐ **HIGHEST PRIORITY**

**Why:** VILLAGE-LEVEL irrigation data — wells, borewells, surface schemes, area irrigated.
This is the most granular village-specific source available.

### Download Steps

1. **Primary source:** https://aikosh.indiaai.gov.in/
   - Search: "6th Minor Irrigation Census Village Schedule"
   - Look for: Ground Water Schemes + Surface Water Schemes tables
   - Filter: Maharashtra → Pune district → Indapur taluka → Loni Devkar

2. **Backup source:** https://www.jalshakti-dowr.gov.in/irrigation-census
   - Ministry of Jal Shakti official portal
   - Downloadable state-level / district-level MI Census data

3. **What to download:**
   - Village schedule data (CSV/Excel) for Loni Devkar, or
   - Indapur taluka aggregate with village breakdown
   - Scheme details: type (dug well, borewell, lift, canal), area irrigated, status

4. **Save to:** `data/raw/mi_census_6th_indapur_villages.csv` (or .xlsx)

---

## Source 2: Agricultural Census 2015-16

**Why:** Operational holdings, irrigated vs. rain-fed area, cropping pattern.

### Download Steps

1. **Official source:** https://agcensus.gov.in/
   - Navigate: Reports → State reports → Maharashtra
   - Find: Pune district / Indapur taluka tables
   - Tables of interest:
     - Number & area of operational holdings by size class
     - Irrigated area by source (well, tube well, canal, tank, etc.)
     - Crops cultivated: area, number of holdings

2. **Data format:** PDF tables or downloadable Excel/CSV
   - Agri Census often publishes in PDF; extract tables to CSV if needed
   - Or check https://data.gov.in for Agri Census datasets

3. **Fallback — Indian Statistics:** https://www.indianstatistics.org/
   - Curated Agri Census data, cleaner CSVs
   - Filter: Maharashtra → Pune → Indapur

4. **Save to:** `data/raw/agri_census_2015_16_indapur.csv`

---

## Source 3: CGWB — Central Ground Water Board

**Why:** Groundwater level (pre/post monsoon), stage of extraction (%), category
(safe/semi-critical/over-exploited), water quality.

### Download Steps

1. **Primary:** https://indiawris.gov.in/ (India-WRIS portal)
   - Search: Indapur block / Pune district groundwater assessment units
   - Data: Pre-monsoon & post-monsoon GWL, annual trends
   - Download: CSV if available, or screenshot/compile from web interface

2. **CGWB direct:** http://cgwb.gov.in/
   - Publications → State groundwater situation
   - Look for Maharashtra groundwater assessment reports

3. **What to extract:**
   - GW level (m bGL — meters below ground level), pre and post monsoon
   - Stage of extraction (%) — how much is being used of available GW
   - Category — Safe / Semi-critical / Over-exploited
   - Water quality parameters (if available)

4. **Save to:** `data/raw/cgwb_gw_status_indapur.csv`

---

## Source 4: Census of India — Village Directory & PCA

**Why:** Loni Devkar village-level basics: population, area, land use, water availability.

### Download Steps

1. **Census 2011 Village Directory:**
   - https://censusindia.gov.in/
   - Navigate: Data Tables → District Census Handbook → Pune
   - Village-wise primary census abstract (PCA)
   - Search/filter: Loni Devkar

2. **What to capture:**
   - Population, households, area of village
   - Land use: cultivated area, forest, water bodies, barren
   - Irrigation source availability (wells, tube wells, canals)
   - Amenities (road, electricity, water, health center)

3. **Data format:** PDF village abstracts or downloadable tables
   - Manual extraction to CSV if needed

4. **Save to:** `data/raw/census_2011_loni_devkar.csv` or `.txt`

---

## Source 5: ICRISAT District-Level Agricultural Data

**Why:** Long time-series (30+ years) of crop area, production, yield, irrigated
area by crop. District-level; can use as Pune benchmark.

### Download Steps

1. **Source:** https://data.icrisat.org/dld/
   - Download: "District Level Data" for Maharashtra, Pune
   - Includes: crop-wise area, production, yield, irrigation

2. **What to download:**
   - Crop-wise area, production (tonnes), yield (kg/ha)
   - Irrigated area by crop
   - Years: as many years as available (typically 1990s–2020s)
   - Focus crops: sugarcane, jowar, wheat, maize, onion, pulse, soybean

3. **Format:** CSV — ready for Python/pandas

4. **Save to:** `data/raw/icrisat_pune_district_crops.csv`

---

## Source 6: IMD — Rainfall & Climate (Monthly/Daily)

**Why:** Effective rainfall needed for water-balance & crop water requirement
calculations.

### Download Steps

1. **IMD Portal:** https://mausam.imd.gov.in/
   - Historical rainfall data download
   - Search: Pune district / nearest weather station to Indapur

2. **Pune IMD:** https://www.imdpune.gov.in/
   - Regional Pune office; may have Indapur-specific or nearest-station data

3. **What to get:**
   - **Monthly rainfall** (mm): full calendar year, 20+ years if available
   - **Daily rainfall** (optional but better): for detailed water-balance
   - Location: Indapur or nearest representative station

4. **Data format:** Excel or CSV; may require manual copy-paste from web tables

5. **Save to:** `data/raw/imd_rainfall_indapur.csv`

---

## Source 7: Maharashtra State Agriculture Department

**Why:** Local/state-level crop advisories, water allocation, groundwater
updates, crop varieties tested locally.

### Download Steps

1. **Department of Agriculture:** https://krishi.maharashtra.gov.in/
   - Publications → Crop statistics, water management, advisories
   - May have Pune district / taluka-specific data

2. **Directorate of Economics & Statistics:** https://des.maharashtra.gov.in/
   - Agricultural statistics, production data, district tables

3. **What to look for:**
   - Recent crop production statistics (Pune, Indapur)
   - Water allocation / irrigation releases
   - Groundwater status reports
   - Crop variety recommendations for drought-prone areas

4. **Save to:** `data/raw/maha_agri_stats_pune.pdf` or extracted `.csv`

---

## Download Checklist

Track your progress here. Once each source is downloaded, place in `data/raw/` with
the suggested filename.

- [ ] 6th MI Census (village schedule) → `data/raw/mi_census_6th_indapur_villages.csv`
- [ ] Agricultural Census 2015-16 → `data/raw/agri_census_2015_16_indapur.csv`
- [ ] CGWB groundwater status → `data/raw/cgwb_gw_status_indapur.csv`
- [ ] Census 2011 Village Directory → `data/raw/census_2011_loni_devkar.csv`
- [ ] ICRISAT Pune district → `data/raw/icrisat_pune_district_crops.csv`
- [ ] IMD rainfall → `data/raw/imd_rainfall_indapur.csv`
- [ ] Maha Agri Dept stats → `data/raw/maha_agri_stats_pune.pdf`

---

## Once Downloaded

Let me know what you've acquired and in what format. I will:
1. Load each source with pandas
2. Clean & standardize column names
3. Filter/aggregate to Indapur / Loni Devkar level
4. Merge into analysis-ready tables for CWP calculation

---

*Last updated: 2026-05-29*
