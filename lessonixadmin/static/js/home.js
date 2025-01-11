document.getElementById("currentDate").textContent = new Date().toLocaleDateString("en-US", {
    month: "2-digit",
    day: "2-digit",
    year: "numeric",
  });
  
// charts.js
const ctx = document.getElementById('attendanceChart').getContext('2d');
const attendanceChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'нд'],
        datasets: [{
            label: 'Відвідуваність',
            data: [240, 200, 260, 240, 120, 40, 20],
            backgroundColor: 'rgba(211, 211, 211, 0.8)',
            borderColor: '#000000',
            borderWidth: 2,
            borderRadius: 5,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                enabled: false
            },
            legend: {
                display: false,
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    font: {
                        size: 14,
                        weight: 600,
                    }
                }
            },
            y: {
                beginAtZero: true,
                max: 300,
                ticks: {
                    stepSize: 40,
                    font: {
                        size: 14,
                        weight: 600,
                    },
                    callback: function(value, index, ticks) {
                        if (value === 300) {
                            return '';
                        }
                        return value;
                    }
                },
                grid: {
                    display: false,
                    drawBorder: false,
                },
            },
        },
    }
});