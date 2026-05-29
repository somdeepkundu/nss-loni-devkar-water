# Data Sources Strategy — Crop Water Productivity, Loni Devkar

## Target Location
- **Village:** Loni Devkar (also spelled Loni Deokar / Loni Dewakar)
- **Taluka:** Indapur
- **District:** Pune
- **State:** Maharashtra (state code 27)
- **Pincode:** 413132 (PO: Palasdeo)
- **Region:** Desh / Paschim Maharashtra, Pune Division
- **Setting:** Drought-prone eastern Pune district, Bhima river / Ujani dam command area, ~143 km east of Pune city near Baramati–Daund. Sugarcane-dominant despite water scarcity — making crop water productivity a high-impact local problem.

---

## The Two-Tier Strategy

NSS gives us **regional (district) context**; other sources give us **village/block specifics**. We combine them.

| Tier | Question it answers | Sources |
|------|--------------------|---------|
| **District (NSS)** | What do typical Pune farm households look like? Crops, irrigation, water sources, income | NSS 77th Round |
| **Village/Block** | What is actually happening in Loni Devkar / Indapur? | Agri Census, MI Census, CGWB, Census village directory |
| **Biophysical** | How much water do crops need vs. get? | IMD rainfall, CGWB groundwater, ET/climate data |

---

## Tier 1 — District Context (NSS 77th Round)

**What it provides:** Household-level operational holdings, irrigated area, crops, irrigation source/method, farm income — for a *sample* of Pune district rural households.

**Granularity limit:** District + NSS region only. Villages are anonymized FSU codes; **Loni Devkar cannot be named/isolated**. Use as a regional benchmark, not village data.

**Status:** Downloaded (367MB `.Nesstar` file). Needs Nesstar Explorer to export → see [NSS_EXTRACTION_GUIDE.md](NSS_EXTRACTION_GUIDE.md).

**Source:** https://microdata.gov.in/ (NSS 77th Round, Sch 33.1)

---

## Tier 2 — Village / Block-Level Sources

### A. Agriculture Census (agcensus.gov.in)
- **Granularity:** Block/taluka-level tables; village-level operational holdings in some tables
- **Provides:** Number & area of operational holdings by size class, irrigated vs. unirrigated area, cropping pattern, irrigation status
- **Latest:** Agriculture Census 2015–16 (2021–22 in progress)
- **URL:** https://agcensus.gov.in/

### B. 6th Minor Irrigation Census — Village Schedule ⭐
- **Granularity:** VILLAGE-LEVEL (this is the key village source)
- **Provides:** Ground water schemes (dug wells, borewells, tube wells), surface water schemes, lift irrigation, area irrigated by each, scheme status
- **Reference period:** 2017–18
- **URL:** https://aikosh.indiaai.gov.in/ (search "6th Minor Irrigation Census Village Schedule")
- **Also:** https://www.jalshakti-dowr.gov.in/irrigation-census

### C. CGWB — Central Ground Water Board
- **Granularity:** Block/taluka groundwater assessment units; monitoring wells
- **Provides:** Groundwater level (pre/post monsoon), stage of extraction (%), category (safe/semi-critical/over-exploited), water quality
- **Why critical:** Indapur groundwater status directly limits sustainable irrigation
- **URL:** http://cgwb.gov.in/ and India-WRIS https://indiawris.gov.in/

### D. Census of India — Village Directory & PCA
- **Granularity:** VILLAGE-LEVEL
- **Provides:** Loni Devkar population, area, land use, irrigation source availability, amenities
- **Latest available:** Census 2011 (village directory)
- **URL:** https://censusindia.gov.in/

### E. ICRISAT District Level Database
- **Granularity:** District (Pune), long time series
- **Provides:** Apportioned crop area, production, yield, irrigated area by crop, normal rainfall — clean CSVs, easy for Python
- **URL:** https://data.icrisat.org/dld/

---

## Tier 3 — Biophysical / Water Balance

### F. IMD — Rainfall & Climate
- Daily/monthly rainfall for Pune district; gridded 0.25° data
- Needed for effective rainfall in water-balance
- **URL:** https://mausam.imd.gov.in/ , https://www.imdpune.gov.in/

### G. Crop Water Requirement (ET-based)
- **Method:** FAO-56 Penman-Monteith → reference ET (ET0) → crop ET (ETc = ET0 × Kc)
- **Tools:** FAO CROPWAT / CLIMWAT, or compute from IMD climate normals
- **Provides:** Theoretical water need per crop → compare to water applied

### H. Remote Sensing (optional, for actual village ET)
- **Bhuvan/ISRO:** land use, crop area mapping — https://bhuvan.nrsc.gov.in/
- **Satellite ET products** (e.g., WaPOR/MODIS) can give actual ET at field scale for Loni Devkar specifically

---

## Crop Water Productivity — What We Compute

**Core metric:**
```
CWP (physical)  = Crop Yield (kg/ha)  /  Water Used (m3/ha)     [kg/m3]
CWP (economic)  = Crop Value (Rs/ha)  /  Water Used (m3/ha)     [Rs/m3]
```

**Water Used** can be defined three ways (we'll be explicit about which):
1. **Irrigation applied** (from MI Census / NSS) — what farmers pump
2. **ETc — crop evapotranspiration** (FAO-56) — what the crop consumes
3. **Total water input** = effective rainfall + irrigation

**The improvement levers** this analysis will surface:
- Crop choice (sugarcane vs. less thirsty alternatives)
- Irrigation method (flood → drip/sprinkler)
- Deficit irrigation / scheduling
- Groundwater sustainability constraints

---

## Data Acquisition Checklist

- [x] NSS 77th Round downloaded (needs extraction)
- [ ] NSS exported to CSV via Nesstar Explorer
- [ ] Agriculture Census 2015–16 — Pune/Indapur tables
- [ ] 6th MI Census Village Schedule — Indapur villages
- [ ] CGWB groundwater status — Indapur block
- [ ] Census 2011 Village Directory — Loni Devkar
- [ ] ICRISAT district CSV — Pune crop/irrigation series
- [ ] IMD rainfall — Pune district
- [ ] FAO Kc values for local crops (sugarcane, jowar, wheat, onion, etc.)

---

*Last updated: 2026-05-29*
