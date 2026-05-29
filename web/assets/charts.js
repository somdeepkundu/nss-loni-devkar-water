// Chart.js visualisations for the MkDocs site.
// Guards on element presence so it is safe on every page.

const cropData = [
    { crop: "Grapes", water: 14025, kg_m3: 1.78, rs_m3: 80.21 },
    { crop: "Onion", water: 8662, kg_m3: 2.89, rs_m3: 43.29 },
    { crop: "Soybean", water: 6325, kg_m3: 0.35, rs_m3: 14.61 },
    { crop: "Maize", water: 7260, kg_m3: 0.69, rs_m3: 13.77 },
    { crop: "Sugarcane", water: 25094, kg_m3: 3.19, rs_m3: 9.88 },
    { crop: "Jowar", water: 6600, kg_m3: 0.38, rs_m3: 9.47 },
    { crop: "Bajra", water: 5225, kg_m3: 0.38, rs_m3: 9.19 },
    { crop: "Wheat", water: 7590, kg_m3: 0.46, rs_m3: 11.07 },
    { crop: "Tur", water: 9680, kg_m3: 0.12, rs_m3: 8.06 }
].sort((a, b) => b.rs_m3 - a.rs_m3);

function cwpChart() {
    const el = document.getElementById('cwpChart');
    if (!el || typeof Chart === 'undefined') return;
    new Chart(el.getContext('2d'), {
        type: 'bar',
        data: {
            labels: cropData.map(d => d.crop),
            datasets: [{
                label: 'Economic CWP (Rs/m³)',
                data: cropData.map(d => d.rs_m3),
                backgroundColor: cropData.map(d => d.rs_m3 > 40 ? '#26A69A' : d.rs_m3 > 15 ? '#FFB74D' : '#EF5350'),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Income per m³ of water — ranked', font: { size: 14, weight: 'bold' } }
            },
            scales: { x: { beginAtZero: true, ticks: { callback: v => v + ' Rs/m³' } } }
        }
    });
}

function schemeChart() {
    const el = document.getElementById('schemeChart');
    if (!el || typeof Chart === 'undefined') return;
    const labels = ['Dug Wells', 'Deep Tube Wells', 'Medium Tube Wells', 'Shallow Tube Wells', 'Surface Flow', 'Surface Lift'];
    const loni = [61, 1, 0, 0, 0, 0];
    new Chart(el.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Schemes in Loni Deokar',
                data: loni,
                backgroundColor: loni.map((v, i) => i === 0 ? '#00838F' : (v > 0 ? '#26A69A' : '#CFD8DC')),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Loni Deokar relies almost entirely on dug wells', font: { size: 14, weight: 'bold' } }
            },
            scales: { x: { beginAtZero: true, title: { display: true, text: 'Number of schemes' } } }
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    cwpChart();
    schemeChart();
});
