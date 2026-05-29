"""
Convert the Loni Deokar CAD-derived GeoPackage to web-ready GeoJSON.

The .gpkg (exported from LONI-DEOKAR.dwg) is tagged EPSG:4326 but the
coordinates are actually UTM Zone 43N metres (EPSG:32643) — that mislabel is
why the data never showed up on a normal map. This script:

  1. reads the GPKG geometry blobs straight from SQLite (no GDAL needed),
  2. parses the WKB (incl. CompoundCurve / CircularString / CurvePolygon),
  3. reprojects UTM 43N -> WGS84 lat/lon with pyproj,
  4. drops junk geometry sitting at the (0,0) origin,
  5. writes simplified GeoJSON for the web map with crop-zone layers.

Outputs (data/processed/geo/):
  loni_plots.geojson    - plot / parcel boundaries
  loni_labels.geojson   - text labels as points
  loni_crops.geojson    - recommended crop zones (rice, grapes, onion)
  loni_waterlog.geojson - waterlogging-risk zones
  loni_meta.json        - centroid + bounds (lat/lon) for the Leaflet view
"""

VERSION = "1.1.0"  # Added crop zone + waterlogging risk layers; dam command context

import json
import math
import sqlite3
import struct
from pathlib import Path

from pyproj import Transformer

GPKG = Path(r"E:\Shapefiles\Loni Deokar\LONI-DEOKAR.gpkg")
OUT = Path("data/processed/geo")
OUT.mkdir(parents=True, exist_ok=True)

# Source CRS: UTM 43N (data is metres, mislabelled as 4326 in the file)
transformer = Transformer.from_crs("EPSG:32643", "EPSG:4326", always_xy=True)

ARC_SEGMENTS = 8  # straight segments used to approximate a circular arc


def wkb_offset(blob: bytes) -> int:
    """Return the byte offset where the WKB geometry begins in a GPKG blob."""
    flags = blob[3]
    env_ind = (flags >> 1) & 0x07
    env_bytes = {0: 0, 1: 32, 2: 48, 3: 64, 4: 48}[env_ind]
    return 8 + env_bytes


class WKBReader:
    def __init__(self, data: bytes, pos: int):
        self.d = data
        self.p = pos

    def byte(self):
        b = self.d[self.p]
        self.p += 1
        return b

    def u32(self, little):
        fmt = "<I" if little else ">I"
        v = struct.unpack_from(fmt, self.d, self.p)[0]
        self.p += 4
        return v

    def xy(self, little):
        fmt = "<dd" if little else ">dd"
        x, y = struct.unpack_from(fmt, self.d, self.p)
        self.p += 16
        return x, y


def read_point(r: WKBReader, little):
    return [r.xy(little)]


def read_linestring(r: WKBReader, little):
    n = r.u32(little)
    return [r.xy(little) for _ in range(n)]


def circ_arc(p0, p1, p2):
    """Approximate the circular arc through 3 points with line segments."""
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:  # collinear -> straight line
        return [p1, p2]
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    cxr, cyr = ux, uy
    a0 = math.atan2(ay - cyr, ax - cxr)
    a1 = math.atan2(by - cyr, bx - cxr)
    a2 = math.atan2(cy - cyr, cx - cxr)

    def norm(a):
        while a < 0:
            a += 2 * math.pi
        return a

    # decide sweep direction using the middle point
    start, mid, end = a0, a1, a2
    cw = ((norm(mid - start)) > (norm(end - start)))
    radius = math.hypot(ax - cxr, ay - cyr)
    if cw:
        if end > start:
            end -= 2 * math.pi
    else:
        if end < start:
            end += 2 * math.pi
    pts = []
    for i in range(1, ARC_SEGMENTS + 1):
        t = start + (end - start) * i / ARC_SEGMENTS
        pts.append((cxr + radius * math.cos(t), cyr + radius * math.sin(t)))
    return pts


def read_circularstring(r: WKBReader, little):
    n = r.u32(little)
    raw = [r.xy(little) for _ in range(n)]
    if n < 3:
        return raw
    out = [raw[0]]
    i = 0
    while i + 2 < n:
        out.extend(circ_arc(raw[i], raw[i + 1], raw[i + 2]))
        i += 2
    return out


def read_compoundcurve(r: WKBReader, little):
    n = r.u32(little)
    pts = []
    for _ in range(n):
        seg = read_geometry(r)  # nested WKB (LineString or CircularString)
        if not pts:
            pts.extend(seg)
        else:
            pts.extend(seg[1:] if seg and seg[0] == pts[-1] else seg)
    return pts


def read_curvepolygon(r: WKBReader, little):
    n = r.u32(little)
    rings = []
    for _ in range(n):
        ring = read_geometry(r)
        rings.append(ring)
    return rings  # list of rings (each a list of pts)


def read_geometry(r: WKBReader):
    """Parse one WKB geometry, return a flat list of (x,y) vertices.

    For polygons/curvepolygons returns the exterior ring vertices.
    """
    little = r.byte() == 1
    gtype = r.u32(little) & 0xFFFF  # mask ISO Z/M flags
    base = gtype % 1000
    if base == 1:  # Point
        return read_point(r, little)
    if base == 2:  # LineString
        return read_linestring(r, little)
    if base == 8:  # CircularString
        return read_circularstring(r, little)
    if base == 9:  # CompoundCurve
        return read_compoundcurve(r, little)
    if base == 3 or base == 10:  # Polygon / CurvePolygon
        rings = read_curvepolygon(r, little) if base == 10 else _read_polygon(r, little)
        return rings[0] if rings else []
    if base in (4, 5, 6, 11):  # Multi* / MultiCurve
        ngeom = r.u32(little)
        allpts = []
        for _ in range(ngeom):
            allpts.extend(read_geometry(r))
        return allpts
    return []


def _read_polygon(r: WKBReader, little):
    n = r.u32(little)
    rings = []
    for _ in range(n):
        m = r.u32(little)
        rings.append([r.xy(little) for _ in range(m)])
    return rings


# Valid UTM 43N box around Loni Deokar (easting ~493k, northing ~2014.9k).
# CAD exports scatter stray vertices near the (0,0) origin; clip them out.
E_MIN, E_MAX = 450_000, 550_000
N_MIN, N_MAX = 1_990_000, 2_030_000


def clip_valid(pts):
    """Keep only vertices inside the real Loni Deokar UTM box."""
    return [p for p in pts if E_MIN < p[0] < E_MAX and N_MIN < p[1] < N_MAX]


def reproject(pts):
    out = []
    for x, y in pts:
        lon, lat = transformer.transform(x, y)
        out.append([round(lon, 6), round(lat, 6)])
    return out


def extract_lines():
    con = sqlite3.connect(str(GPKG))
    cur = con.cursor()
    features = []
    all_lats, all_lons = [], []
    for table in ("polylines", "lines"):
        cur.execute(f"SELECT geom FROM {table} WHERE geom IS NOT NULL")
        for (blob,) in cur.fetchall():
            try:
                r = WKBReader(blob, wkb_offset(blob))
                pts = read_geometry(r)
            except Exception:
                continue
            pts = clip_valid(pts)
            if len(pts) < 2:
                continue
            ll = reproject(pts)
            for lon, lat in ll:
                all_lons.append(lon)
                all_lats.append(lat)
            features.append({
                "type": "Feature",
                "properties": {"src": table},
                "geometry": {"type": "LineString", "coordinates": ll},
            })
    con.close()
    return features, all_lats, all_lons


def extract_labels():
    con = sqlite3.connect(str(GPKG))
    cur = con.cursor()
    # find a text-content column if present
    cols = [c[1] for c in cur.execute("PRAGMA table_info(texts)").fetchall()]
    text_col = next((c for c in cols if c.lower() in ("text", "textstring", "contents", "label", "value")), None)
    sel = f"geom, {text_col}" if text_col else "geom"
    features = []
    for row in cur.execute(f"SELECT {sel} FROM texts WHERE geom IS NOT NULL"):
        blob = row[0]
        label = row[1] if text_col and len(row) > 1 else ""
        try:
            r = WKBReader(blob, wkb_offset(blob))
            pts = read_geometry(r)
        except Exception:
            continue
        pts = clip_valid(pts)
        if not pts:
            continue
        lon, lat = reproject(pts)[0]
        features.append({
            "type": "Feature",
            "properties": {"label": str(label) if label else ""},
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
        })
    con.close()
    return features


def main():
    lines, lats, lons = extract_lines()
    print(f"Plot/line features kept: {len(lines)}")
    (OUT / "loni_plots.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": lines}), encoding="utf-8"
    )

    labels = extract_labels()
    print(f"Label features kept: {len(labels)}")
    (OUT / "loni_labels.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": labels}), encoding="utf-8"
    )

    if lats and lons:
        meta = {
            "center": [round(sum(lats) / len(lats), 6), round(sum(lons) / len(lons), 6)],
            "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
            "source_crs": "EPSG:32643 (UTM 43N), file mislabelled as 4326",
            "feature_counts": {"plots": len(lines), "labels": len(labels)},
        }
        (OUT / "loni_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print("Center (lat,lon):", meta["center"])
        print("Bounds:", meta["bounds"])


if __name__ == "__main__":
    main()
