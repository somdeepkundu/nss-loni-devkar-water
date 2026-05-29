# NSS Nesstar Data Extraction Guide

The NSS 77th Round data is locked in a proprietary `.Nesstar` file (367 MB) that
only **Nesstar Explorer** can open. This guide walks through exporting it to a
format pandas can read.

## File locations
- Data file: `data/raw/Round77sch331Data/NSS77_33pt1study.Nesstar`
- Installer:  `data/raw/Round77sch331Data/NesstarExplorerInstaller.exe`

## Why this is needed
We tested direct parsing (ZIP, SPSS, Stata, GZIP, zlib) — none work. The format
is custom-encoded with a `NESSTART` header. Nesstar Explorer is the only reader.

---

## Step 1 — Install Nesstar Explorer
1. Run `NesstarExplorerInstaller.exe` (in the data folder)
2. Accept defaults, finish install
3. Launch **Nesstar Explorer**

## Step 2 — Open the study
1. File → Open  →  select `NSS77_33pt1study.Nesstar`
2. Wait for it to load (large file, may take a minute)
3. You'll see the study tree with **data files / "cubes"**. NSS 77th Sch 33.1
   typically has multiple levels (blocks), e.g.:
   - Level 1–2: Household identification & general particulars
   - Level 3+: Land holdings, crops, irrigation
   - Livestock, income, expenditure blocks

## Step 3 — Export each data block
For each data file in the tree:
1. Right-click → **Export** (or File → Export Data)
2. Choose format — preference order:
   - **Stata (.dta)** — best: keeps variable names + value labels
   - **SPSS (.sav)** — also good for labels
   - **CSV / tab-delimited** — simplest, but labels separate
3. Save into: `data/raw/nss_export/`
4. Name clearly: `nss77_L01_hh_id.dta`, `nss77_L03_land.dta`, etc.

> Tip: Stata format is ideal — pandas reads it with `pd.read_stata()` and you
> keep the coded value labels (crop codes, irrigation codes, etc.).

## Step 4 — Note the data dictionary
While in Explorer, also export or screenshot the **variable descriptions** for
the blocks that contain:
- State / district / NSS region codes
- Operational holding area
- Irrigated area
- Crop code
- Irrigation source / method
- Multiplier / weight (for population estimates)

These map cryptic column names (e.g., `b3q5`) to meanings.

---

## Step 5 — Tell me when done
Once exported to `data/raw/nss_export/`, let me know and I'll:
1. Load the blocks with pandas
2. Filter to **Maharashtra (state 27) → Pune district**
3. Merge household + land + irrigation blocks on common IDs
4. Apply survey weights for correct district estimates
5. Compute district-level irrigation & cropping benchmarks

---

## Alternative if Nesstar Explorer won't run
- Some researchers use the **GNU R `nesstar` reader** — unreliable for MoSPI files.
- Better fallback: **MoSPI eSankhyiki / data portal** sometimes offers the same
  round as fixed-width ASCII + layout file. If Explorer fails, we pivot there.

---

*Last updated: 2026-05-29*
