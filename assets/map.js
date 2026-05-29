// Loni Deokar cadastral map — Leaflet over OpenStreetMap.
// Data: data/processed/geo/*.geojson (digitised from LONI-DEOKAR.dwg,
// reprojected UTM 43N -> WGS-84 by scripts/gpkg_to_geojson.py).

document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('map');
    if (!el || typeof L === 'undefined') return;

    const map = L.map('map').setView([18.2014, 74.9126], 14);

    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const sat = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { maxZoom: 19, attribution: 'Tiles &copy; Esri' }
    );

    const plotLayer = L.geoJSON(null, {
        style: { color: '#1E88E5', weight: 1, opacity: 0.8 }
    });

    const labelLayer = L.layerGroup();

    fetch('data/processed/geo/loni_plots.geojson')
        .then(r => r.json())
        .then(gj => {
            plotLayer.addData(gj);
            plotLayer.addTo(map);
            try { map.fitBounds(plotLayer.getBounds(), { padding: [20, 20] }); } catch (e) {}
        })
        .catch(e => console.error('plots load failed', e));

    fetch('data/processed/geo/loni_labels.geojson')
        .then(r => r.json())
        .then(gj => {
            gj.features.forEach(f => {
                const txt = (f.properties && f.properties.label) ? f.properties.label : '';
                if (!txt) return;
                const [lon, lat] = f.geometry.coordinates;
                L.marker([lat, lon], {
                    icon: L.divIcon({
                        className: 'plot-label',
                        html: txt,
                        iconSize: null
                    })
                }).addTo(labelLayer);
            });
        })
        .catch(e => console.error('labels load failed', e));

    L.control.layers(
        { 'Street (OSM)': osm, 'Satellite': sat },
        { 'Plot boundaries': plotLayer, 'Survey numbers': labelLayer }
    ).addTo(map);
});
