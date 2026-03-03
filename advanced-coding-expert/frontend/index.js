import Chart from 'chart.js/auto';
import axios from 'axios';

// ---------- Chart setup ----------
const ctx = document.getElementById('perfChart').getContext('2d');

const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],               // timestamps will be filled dynamically
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
      y: {beginAtZero: true, max: 100}
    }
  }
});

// ---------- Poll the backend ----------
function refreshMetrics() {
  axios.get('/api/model/performance')
    .then(res => {
      const { timestamps, accuracy } = res.data;
      chart.data.labels = timestamps;
      chart.data.datasets[0].data = accuracy;
      chart.update();
    })
    .catch(err => console.error('⚠️ Could not fetch metrics', err));
}

// first load + repeat every 5 seconds
refreshMetrics();
setInterval(refreshMetrics, 5000);