document.addEventListener("DOMContentLoaded", function() {
  // Chart.js defaults for dark theme
  Chart.defaults.color = "#A8B0C5";
  Chart.defaults.borderColor = "rgba(255,255,255,0.06)";
  Chart.defaults.font.family = "'Inter', sans-serif";

  // Helper: parse JSON data attribute
  function getData(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    try {
      return {
        labels: JSON.parse(el.dataset.labels || "[]"),
        values: JSON.parse(el.dataset.values || "[]")
      };
    } catch(e) { return null; }
  }

  // ── Monthly Upload Line Chart ──
  const uploadData = getData("monthlyUploadChart");
  if (uploadData && uploadData.labels.length) {
    new Chart(document.getElementById("monthlyUploadChart"), {
      type: "line",
      data: {
        labels: uploadData.labels,
        datasets: [{
          label: "Contracts",
          data: uploadData.values,
          borderColor: "#7C5CFC",
          backgroundColor: "rgba(124,92,252,0.1)",
          borderWidth: 2,
          pointBackgroundColor: "#7C5CFC",
          pointBorderColor: "#1A2138",
          pointBorderWidth: 2,
          pointRadius: 4,
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: "rgba(255,255,255,0.04)" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // ── Risk Distribution Doughnut ──
  const riskData = getData("riskDistributionChart");
  if (riskData && riskData.labels.length) {
    new Chart(document.getElementById("riskDistributionChart"), {
      type: "doughnut",
      data: {
        labels: riskData.labels,
        datasets: [{
          data: riskData.values,
          backgroundColor: ["#EF4444", "#F59E0B", "#22C55E"],
          borderColor: "#1A2138",
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { padding: 12, usePointStyle: true, font: { size: 11 } }
          }
        },
        cutout: "65%"
      }
    });
  } else {
    // Show empty state
    const canvas = document.getElementById("riskDistributionChart");
    if (canvas) {
      canvas.parentElement.innerHTML = `
        <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:200px;background:rgba(11,17,32,0.6);border-radius:16px;">
          <i class="bi bi-shield-check" style="font-size:36px;color:var(--success);"></i>
          <h5 style="color:var(--text-secondary);font-size:14px;margin-top:8px;">No risks detected</h5>
        </div>`;
    }
  }

  // ── Clause Distribution Doughnut ──
  const clauseData = getData("clauseDistributionChart");
  if (clauseData && clauseData.labels.length) {
    const colors = ["#7C5CFC", "#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A78BFA", "#60A5FA", "#34D399"];
    new Chart(document.getElementById("clauseDistributionChart"), {
      type: "doughnut",
      data: {
        labels: clauseData.labels,
        datasets: [{
          data: clauseData.values,
          backgroundColor: colors.slice(0, clauseData.labels.length),
          borderColor: "#1A2138",
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { padding: 10, usePointStyle: true, font: { size: 10 } }
          }
        },
        cutout: "60%"
      }
    });
  } else {
    const canvas = document.getElementById("clauseDistributionChart");
    if (canvas) {
      canvas.parentElement.innerHTML = `
        <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:200px;background:rgba(11,17,32,0.6);border-radius:16px;">
          <i class="bi bi-file-earmark-x" style="font-size:36px;color:var(--text-muted);"></i>
          <h5 style="color:var(--text-secondary);font-size:14px;margin-top:8px;">No clauses yet</h5>
        </div>`;
    }
  }
});