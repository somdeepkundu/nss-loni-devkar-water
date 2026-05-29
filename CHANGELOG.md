# Changelog

All notable changes to this project are documented here.

## [1.1.0] — 2026-05-29

### Changed
- **Hydrology premise corrected**: Loni Deokar's primary constraint is **waterlogging from Ujjaini dam releases**, not groundwater depletion. The 2025 La Niña event caused maize crop failure due to overwatering, not deficit.
- **Analysis reframed**: shifted focus from "crop choice to save groundwater" to "crop choice to manage waterlogging risk and dam-driven variability."
- **Map visualization redesigned**: now shows waterlogging-risk zones, crop-zone recommendations, and well-depth characteristics (deep wells hitting red iron-oxide rocks).
- **Data context expanded**: added Ujjaini dam release patterns, La Niña 2025 impacts, and groundwater quality indicators.

### Added
- `CHANGELOG.md` — version history.
- Version tracking across all source files (`VERSION = 1.1.0` in scripts, mkdocs config).
- New map layers: waterlogging zones, recommended crop zones, well depth zones.
- La Niña 2025 impact analysis in analysis.md.
- Red-rock (deep aquifer iron oxide) characteristics in data.md.

### Fixed
- Incorrect narrative about groundwater stress (was based on deeper water table, but misses surface water availability).

## [1.0.0] — 2026-05-28

### Added
- Initial MkDocs Material site with cadastral map, CWP analysis, and citations.
- 6th Minor Irrigation Census filtering and analysis.
- Leaflet interactive map (1,045 plots, 1,059 survey labels).
- Chart.js visualizations (irrigation scheme distribution, CWP ranking).
- Full citation infrastructure (RuDRA Lab, CTARA, IIT Bombay).
- GitHub Actions CI/CD for Pages deployment.
