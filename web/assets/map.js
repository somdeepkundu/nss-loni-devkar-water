// Loni Deokar crop-zone map — Leaflet over OpenStreetMap / satellite.
// Shows hydrologic zones with recommended crops.
// GeoJSON digitised from LONI-DEOKAR.dwg, reprojected UTM 43N -> WGS-84.

document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('map');
    if (!el || typeof L === 'undefined') return;

    const root = window.location.pathname.replace(/[^/]*$/, '');

    const map = L.map('map').setView([18.2014, 74.9126], 14);

    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19, attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const sat = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { maxZoom: 19, attribution: 'Tiles &copy; Esri' }
    );

    // Crop zone colors by suitability
    const zoneColors = {
        1: '#2E7D32', // Green: Rice (flood-tolerant)
        2: '#F57C00', // Orange: Sugarcane/Mulberry (intermediate)
        3: '#C62828'  // Red: Banana/Pomegranate (elevated, premium)
    };

    const zoneStyle = function(feature) {
        const zoneId = feature.properties.zone_id;
        return {
            color: zoneColors[zoneId] || '#666',
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.5,
            fillColor: zoneColors[zoneId]
        };
    };

    const zonePopup = function(feature) {
        const p = feature.properties;
        return `<strong>${p.name}</strong><br>
            <strong>Primary:</strong> ${p.primary_crop}<br>
            <strong>Secondary:</strong> ${p.secondary_crop}<br>
            <strong>Water:</strong> ${p.water_req}<br>
            <strong>Income:</strong> ${p.income}<br>
            <strong>Flood Tolerance:</strong> ${p.flood_tolerance}<br>
            <em style="font-size: 0.85em;">${p.description}</em>`;
    };

    const zoneLayer = L.geoJSON(null, {
        style: zoneStyle,
        onEachFeature: function(feature, layer) {
            layer.bindPopup(zonePopup(feature));
        }
    });

    const plotLayer = L.geoJSON(null, {
        style: { color: '#00838F', weight: 0.5, opacity: 0.4 }
    });

    const labelLayer = L.layerGroup();

    // Load crop zones
    fetch(root + 'geo/loni_crop_zones.geojson')
        .then(r => r.json())
        .then(gj => {
            zoneLayer.addData(gj).addTo(map);
            try { map.fitBounds(zoneLayer.getBounds(), { padding: [40, 40] }); } catch (e) {}
        })
        .catch(e => console.error('crop zones load failed', e));

    // Load plot boundaries (optional, visible but subtle)
    fetch(root + 'geo/loni_plots.geojson')
        .then(r => r.json())
        .then(gj => {
            plotLayer.addData(gj).addTo(map);
        })
        .catch(e => console.error('plots load failed', e));

    // Load survey labels (optional, hidden by default)
    fetch(root + 'geo/loni_labels.geojson')
        .then(r => r.json())
        .then(gj => {
            gj.features.forEach(f => {
                const txt = f.properties && f.properties.label ? f.properties.label : '';
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
        {
            'Crop zones': zoneLayer,
            'Plot boundaries': plotLayer,
            'Survey numbers': labelLayer
        },
        { collapsed: false }
    ).addTo(map);
});
