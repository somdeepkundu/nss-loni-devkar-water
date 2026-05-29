// Crop water productivity data
const cropData = [
    { crop: "Grapes", water: 14025, yield: 25, price: 45, kg_m3: 1.78, rs_m3: 80.21 },
    { crop: "Onion", water: 8662, yield: 25, price: 15, kg_m3: 2.89, rs_m3: 43.29 },
    { crop: "Soybean", water: 6325, yield: 2.2, price: 42, kg_m3: 0.35, rs_m3: 14.61 },
    { crop: "Maize", water: 7260, yield: 5, price: 20, kg_m3: 0.69, rs_m3: 13.77 },
    { crop: "Wheat", water: 7590, yield: 3.5, price: 24, kg_m3: 0.46, rs_m3: 11.07 },
    { crop: "Sugarcane", water: 25094, yield: 80, price: 3.1, kg_m3: 3.19, rs_m3: 9.88 },
    { crop: "Jowar", water: 6600, yield: 2.5, price: 25, kg_m3: 0.38, rs_m3: 9.47 },
    { crop: "Bajra", water: 5225, yield: 2, price: 24, kg_m3: 0.38, rs_m3: 9.19 },
    { crop: "Tur", water: 9680, yield: 1.2, price: 65, kg_m3: 0.12, rs_m3: 8.06 }
];

// Sort by economic CWP (Rs/m³) in descending order
cropData.sort((a, b) => b.rs_m3 - a.rs_m3);

// Create Economic CWP Chart
function createCWPChart() {
    const ctx = document.getElementById('cwpChart').getContext('2d');

    const crops = cropData.map(d => d.crop);
    const economics = cropData.map(d => d.rs_m3);
    const physical = cropData.map(d => d.kg_m3);

    // Color coding: high (green), medium (yellow), low (red)
    const colors = cropData.map(d => {
        if (d.rs_m3 > 40) return '#66BB6A';
        if (d.rs_m3 > 15) return '#FFA726';
        return '#EF5350';
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: crops,
            datasets: [
                {
                    label: 'Economic CWP (Rs/m³)',
                    data: economics,
                    backgroundColor: colors,
                    borderColor: '#333',
                    borderWidth: 1,
                    borderRadius: 4
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Income per m³ of Water — Ranked',
                    font: { size: 14, weight: 'bold' }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + ' Rs/m³';
                        }
                    }
                }
            }
        }
    });
}

// Initialize chart when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    createCWPChart();

    // Add smooth scroll to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    console.log('Dashboard loaded. Crop data:', cropData.length, 'crops loaded.');
});

// Export data for analysis (when real data arrives)
window.cwpData = {
    crops: cropData,
    summary: {
        best: cropData[0],
        worst: cropData[cropData.length - 1],
        average_rs_m3: (cropData.reduce((sum, d) => sum + d.rs_m3, 0) / cropData.length).toFixed(2)
    }
};

console.log('CWP Analysis Dashboard Ready. Data available at window.cwpData');
