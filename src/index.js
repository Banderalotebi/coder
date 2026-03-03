import Chart from 'chart.js/auto';
import axios from 'axios';

const ctx = document.getElementById('perfChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],            // will be filled with timestamps / epochs
    datasets: [{
      label: 'Accuracy (%)',
      data: [],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
      fill: false,
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true, max: 100 }
    }
  }
});

// Fetch performance data from the backend API
function loadPerformance() {
  axios.get('/api/model/performance')
    .then(res => {
      const { timestamps, accuracy } = res.data;
      chart.data.labels = timestamps;
      chart.data.datasets[0].data = accuracy;
      chart.update();
    })
    .catch(err => console.error('Failed to load performance data', err));
}

// Initial load + poll every 5 seconds
loadPerformance();
setInterval(loadPerformance, 5000);

// initial load + poll every 5 seconds
loadPerformance();
setInterval(loadPerformance, 5000);