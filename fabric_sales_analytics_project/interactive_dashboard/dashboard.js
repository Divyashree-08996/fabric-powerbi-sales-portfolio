// Power BI Interactive Sales Dashboard Engine
// End-to-End Microsoft Fabric Lakehouse & Power BI Simulator

const SALES_DATABASE = {
  years: ["2025", "2024", "2023"],
  quarters: ["Q1", "Q2", "Q3", "Q4"],
  regions: {
    "NA": { name: "North America", vp: "David Vance", channels: ["Direct Enterprise Sales", "Digital Cloud Marketplace"] },
    "EMEA": { name: "Europe, Middle East, Africa", vp: "Klaus Richter", channels: ["EMEA Strategic Partners", "UK & Northern Europe Field", "France & Southern Europe"] },
    "APAC": { name: "Asia Pacific", vp: "Mei Lin", channels: ["APAC Enterprise Alliance", "Australia & Oceania Hub"] }
  },
  categories: ["Hardware", "Software Licenses", "Cloud Services", "Professional Services"],
  
  // Baseline data generator points
  monthlyData: [
    { year: 2025, month: "Jan", sales: 3950000, budget: 3800000, pySales: 3200000, region: "NA", cat: "Hardware" },
    { year: 2025, month: "Feb", sales: 4120000, budget: 3900000, pySales: 3350000, region: "EMEA", cat: "Software Licenses" },
    { year: 2025, month: "Mar", sales: 4480000, budget: 4200000, pySales: 3600000, region: "APAC", cat: "Cloud Services" },
    { year: 2025, month: "Apr", sales: 4310000, budget: 4100000, pySales: 3500000, region: "NA", cat: "Professional Services" },
    { year: 2025, month: "May", sales: 4620000, budget: 4350000, pySales: 3750000, region: "EMEA", cat: "Hardware" },
    { year: 2025, month: "Jun", sales: 4890000, budget: 4500000, pySales: 3900000, region: "APAC", cat: "Software Licenses" },
    { year: 2025, month: "Jul", sales: 4420000, budget: 4300000, pySales: 3650000, region: "NA", cat: "Cloud Services" },
    { year: 2025, month: "Aug", sales: 4580000, budget: 4400000, pySales: 3700000, region: "EMEA", cat: "Professional Services" },
    { year: 2025, month: "Sep", sales: 4750000, budget: 4600000, pySales: 3950000, region: "APAC", cat: "Hardware" },
    { year: 2025, month: "Oct", sales: 4950000, budget: 4700000, pySales: 4100000, region: "NA", cat: "Software Licenses" },
    { year: 2025, month: "Nov", sales: 5120000, budget: 4800000, pySales: 4250000, region: "EMEA", cat: "Cloud Services" },
    { year: 2025, month: "Dec", sales: 5690000, budget: 5200000, pySales: 4600000, region: "APAC", cat: "Professional Services" }
  ],

  topCustomers: [
    { id: "CUST-0001", name: "Apex Global Solutions", region: "NA", country: "USA", sales: 4850000, marginPct: 54.2, orders: 420 },
    { id: "CUST-0002", name: "Quantum Logistics GmbH", region: "EMEA", country: "Germany", sales: 4120000, marginPct: 51.8, orders: 385 },
    { id: "CUST-0003", name: "Nexus Healthcare Corp", region: "NA", country: "USA", sales: 3980000, marginPct: 56.4, orders: 340 },
    { id: "CUST-0006", name: "Tokyo Telecom Nippon", region: "APAC", country: "Japan", sales: 3620000, marginPct: 49.3, orders: 310 },
    { id: "CUST-0005", name: "Helvetia Alpine Tech", region: "EMEA", country: "Switzerland", sales: 3450000, marginPct: 53.1, orders: 295 },
    { id: "CUST-0007", name: "Sydney Harbour Financial", region: "APAC", country: "Australia", sales: 3180000, marginPct: 52.0, orders: 270 },
    { id: "CUST-0004", name: "Vortex Retail UK", region: "EMEA", country: "UK", sales: 2950000, marginPct: 48.7, orders: 260 },
    { id: "CUST-0009", name: "CyberShield Security Ltd", region: "EMEA", country: "UK", sales: 2740000, marginPct: 62.1, orders: 245 },
    { id: "CUST-0008", name: "Ontario Cloud Systems", region: "NA", country: "Canada", sales: 2590000, marginPct: 50.4, orders: 230 },
    { id: "CUST-0010", name: "Kyoto Robotics Mfg", region: "APAC", country: "Japan", sales: 2410000, marginPct: 47.9, orders: 215 }
  ],

  categoryBreakdown: {
    "Hardware": { sales: 54726265, cost: 28457650, share: 41.5, margin: 48.0 },
    "Professional Services": { sales: 41019843, cost: 18458920, share: 31.1, margin: 55.0 },
    "Software Licenses": { sales: 24809812, cost: 8931530, share: 18.8, margin: 64.0 },
    "Cloud Services": { sales: 11332833, cost: 4441890, share: 8.6, margin: 60.8 }
  },

  regionBreakdown: {
    "NA": { sales: 46592683, target: 44000000, rep: "David Vance", share: 35.3 },
    "EMEA": { sales: 45980405, target: 43500000, rep: "Klaus Richter", share: 34.9 },
    "APAC": { sales: 39315666, target: 37500000, rep: "Mei Lin", share: 29.8 }
  }
};

let currentFilters = {
  year: "2025",
  region: "all",
  category: "all",
  priceAdjust: 0,
  costAdjust: 0
};

let chartMonthly = null;
let chartCategory = null;
let chartRegion = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  renderDashboard();
});

function setupEventListeners() {
  // Slicers
  document.getElementById("slicer-year")?.addEventListener("change", (e) => {
    currentFilters.year = e.target.value;
    renderDashboard();
  });

  document.getElementById("slicer-region")?.addEventListener("change", (e) => {
    currentFilters.region = e.target.value;
    renderDashboard();
  });

  document.getElementById("slicer-category")?.addEventListener("change", (e) => {
    currentFilters.category = e.target.value;
    renderDashboard();
  });

  // What-If Sliders
  document.getElementById("slider-price")?.addEventListener("input", (e) => {
    currentFilters.priceAdjust = parseFloat(e.target.value);
    document.getElementById("val-price").textContent = `${currentFilters.priceAdjust > 0 ? '+' : ''}${currentFilters.priceAdjust}%`;
    updateWhatIfSimulations();
  });

  document.getElementById("slider-cost")?.addEventListener("input", (e) => {
    currentFilters.costAdjust = parseFloat(e.target.value);
    document.getElementById("val-cost").textContent = `${currentFilters.costAdjust > 0 ? '+' : ''}${currentFilters.costAdjust}%`;
    updateWhatIfSimulations();
  });

  // Reset Filters Button
  document.getElementById("btn-reset-filters")?.addEventListener("click", () => {
    currentFilters = { year: "2025", region: "all", category: "all", priceAdjust: 0, costAdjust: 0 };
    document.getElementById("slicer-year").value = "2025";
    document.getElementById("slicer-region").value = "all";
    document.getElementById("slicer-category").value = "all";
    if (document.getElementById("slider-price")) {
      document.getElementById("slider-price").value = "0";
      document.getElementById("val-price").textContent = "0%";
    }
    if (document.getElementById("slider-cost")) {
      document.getElementById("slider-cost").value = "0";
      document.getElementById("val-cost").textContent = "0%";
    }
    renderDashboard();
  });

  // Tab Switching
  document.querySelectorAll(".pbi-tab").forEach(tab => {
    tab.addEventListener("click", (e) => {
      document.querySelectorAll(".pbi-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const targetTab = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach(c => c.style.display = "none");
      document.getElementById(`tab-${targetTab}`).style.display = "block";
    });
  });

  // Theme Toggle
  document.getElementById("btn-theme-toggle")?.addEventListener("click", () => {
    const isDark = document.body.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.body.removeAttribute("data-theme");
      document.getElementById("btn-theme-toggle").textContent = "🌙 Dark Mode";
    } else {
      document.body.setAttribute("data-theme", "dark");
      document.getElementById("btn-theme-toggle").textContent = "☀️ Light Mode";
    }
    renderDashboard();
  });

  // Export CSV
  document.getElementById("btn-export-csv")?.addEventListener("click", exportSalesDataCSV);
}

function calculateCurrentMetrics() {
  let scale = 1.0;
  if (currentFilters.year === "2024") scale = 0.835;
  if (currentFilters.year === "2023") scale = 0.706;

  let regionFilterMultiplier = 1.0;
  if (currentFilters.region === "NA") regionFilterMultiplier = 0.353;
  if (currentFilters.region === "EMEA") regionFilterMultiplier = 0.349;
  if (currentFilters.region === "APAC") regionFilterMultiplier = 0.298;

  let catFilterMultiplier = 1.0;
  if (currentFilters.category === "Hardware") catFilterMultiplier = 0.415;
  if (currentFilters.category === "Professional Services") catFilterMultiplier = 0.311;
  if (currentFilters.category === "Software Licenses") catFilterMultiplier = 0.188;
  if (currentFilters.category === "Cloud Services") catFilterMultiplier = 0.086;

  const totalSalesBase = 51882134 * scale * regionFilterMultiplier * catFilterMultiplier;
  const totalCostBase = 24488390 * scale * regionFilterMultiplier * catFilterMultiplier;
  const budgetBase = 49000000 * scale * regionFilterMultiplier * catFilterMultiplier;
  const pySalesBase = 43336404 * (scale === 1.0 ? 1.0 : scale * 0.85) * regionFilterMultiplier * catFilterMultiplier;

  const totalOrders = Math.round(13929 * scale * regionFilterMultiplier * catFilterMultiplier);
  const unitsSold = Math.round(58200 * scale * regionFilterMultiplier * catFilterMultiplier);

  const grossProfit = totalSalesBase - totalCostBase;
  const marginPct = (grossProfit / totalSalesBase) * 100;
  const aov = totalSalesBase / (totalOrders || 1);
  const budgetVariance = totalSalesBase - budgetBase;
  const budgetAchievedPct = (totalSalesBase / budgetBase) * 100;
  const yoyGrowthPct = ((totalSalesBase - pySalesBase) / pySalesBase) * 100;

  return {
    sales: totalSalesBase,
    cost: totalCostBase,
    profit: grossProfit,
    marginPct: marginPct,
    orders: totalOrders,
    units: unitsSold,
    aov: aov,
    budget: budgetBase,
    budgetVariance: budgetVariance,
    budgetAchievedPct: budgetAchievedPct,
    yoyGrowthPct: yoyGrowthPct,
    scale: scale,
    regionMult: regionFilterMultiplier,
    catMult: catFilterMultiplier
  };
}

function formatUSD(val) {
  if (Math.abs(val) >= 1e6) {
    return '$' + (val / 1e6).toFixed(2) + 'M';
  } else if (Math.abs(val) >= 1e3) {
    return '$' + (val / 1e3).toFixed(1) + 'K';
  }
  return '$' + Math.round(val).toLocaleString();
}

function renderDashboard() {
  const m = calculateCurrentMetrics();

  // Render KPI Cards
  document.getElementById("kpi-sales").textContent = formatUSD(m.sales);
  document.getElementById("kpi-profit").textContent = formatUSD(m.profit);
  document.getElementById("kpi-margin").textContent = m.marginPct.toFixed(1) + '%';
  document.getElementById("kpi-orders").textContent = m.orders.toLocaleString();
  document.getElementById("kpi-aov").textContent = '$' + Math.round(m.aov).toLocaleString();
  document.getElementById("kpi-budget-attain").textContent = m.budgetAchievedPct.toFixed(1) + '%';

  const badgeYoy = document.getElementById("badge-yoy");
  if (badgeYoy) {
    badgeYoy.className = m.yoyGrowthPct >= 0 ? "badge-growth-pos" : "badge-growth-neg";
    badgeYoy.textContent = `${m.yoyGrowthPct >= 0 ? '▲ +' : '▼ '}${m.yoyGrowthPct.toFixed(1)}% YoY`;
  }

  const badgeTarget = document.getElementById("badge-target");
  if (badgeTarget) {
    const isExceeded = m.budgetAchievedPct >= 100;
    badgeTarget.className = isExceeded ? "badge-growth-pos" : "badge-growth-neg";
    badgeTarget.textContent = `${isExceeded ? '🟢' : '🔴'} ${formatUSD(m.budgetVariance)} vs Target`;
  }

  // Render Charts
  renderMonthlyTrendChart(m);
  renderCategoryBreakdownChart(m);
  renderRegionDoughnutChart(m);
  renderCustomerTable(m);
  updateWhatIfSimulations();
}

function renderMonthlyTrendChart(m) {
  const ctx = document.getElementById("chart-monthly-trend")?.getContext("2d");
  if (!ctx) return;

  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const salesData = SALES_DATABASE.monthlyData.map(d => d.sales * m.scale * m.regionMult * m.catMult);
  const budgetData = SALES_DATABASE.monthlyData.map(d => d.budget * m.scale * m.regionMult * m.catMult);
  const pyData = SALES_DATABASE.monthlyData.map(d => d.pySales * m.scale * m.regionMult * m.catMult);

  if (chartMonthly) chartMonthly.destroy();

  chartMonthly = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: months,
      datasets: [
        {
          label: 'Net Sales ($)',
          data: salesData,
          backgroundColor: '#118dff',
          borderRadius: 4,
          order: 2
        },
        {
          label: 'Budget Target ($)',
          data: budgetData,
          type: 'line',
          borderColor: '#f2c811',
          borderWidth: 3,
          pointBackgroundColor: '#f2c811',
          pointRadius: 4,
          tension: 0.2,
          order: 1
        },
        {
          label: 'Prior Year (PY)',
          data: pyData,
          type: 'line',
          borderColor: '#a19f9d',
          borderWidth: 2,
          borderDash: [5, 5],
          pointRadius: 0,
          tension: 0.2,
          order: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${formatUSD(ctx.raw)}`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: (val) => formatUSD(val), font: { size: 10 } }
        },
        x: { ticks: { font: { size: 11 } } }
      }
    }
  });
}

function renderCategoryBreakdownChart(m) {
  const ctx = document.getElementById("chart-category-bar")?.getContext("2d");
  if (!ctx) return;

  const cats = Object.keys(SALES_DATABASE.categoryBreakdown);
  const catSales = cats.map(c => SALES_DATABASE.categoryBreakdown[c].sales * m.scale * m.regionMult * (currentFilters.category === "all" || currentFilters.category === c ? 1 : 0.05));
  const catMargins = cats.map(c => SALES_DATABASE.categoryBreakdown[c].margin);

  if (chartCategory) chartCategory.destroy();

  chartCategory = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: cats,
      datasets: [{
        label: 'Net Sales ($)',
        data: catSales,
        backgroundColor: ['#0078d4', '#118dff', '#4ade80', '#f2c811'],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Sales: ${formatUSD(ctx.raw)} (Margin: ${catMargins[ctx.dataIndex]}%)`
          }
        }
      },
      scales: {
        x: { ticks: { callback: (val) => formatUSD(val), font: { size: 10 } } },
        y: { ticks: { font: { size: 11 } } }
      }
    }
  });
}

function renderRegionDoughnutChart(m) {
  const ctx = document.getElementById("chart-region-doughnut")?.getContext("2d");
  if (!ctx) return;

  const regions = ["NA", "EMEA", "APAC"];
  const regionNames = ["North America", "EMEA", "Asia Pacific"];
  const regionSales = regions.map(r => SALES_DATABASE.regionBreakdown[r].sales * m.scale * m.catMult * (currentFilters.region === "all" || currentFilters.region === r ? 1 : 0.1));

  if (chartRegion) chartRegion.destroy();

  chartRegion = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: regionNames,
      datasets: [{
        data: regionSales,
        backgroundColor: ['#0078d4', '#107c41', '#f2c811'],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.label}: ${formatUSD(ctx.raw)} (${((ctx.raw / (regionSales.reduce((a,b)=>a+b,0)))*100).toFixed(1)}%)`
          }
        }
      },
      cutout: '68%'
    }
  });
}

function renderCustomerTable(m) {
  const tbody = document.getElementById("table-customer-body");
  if (!tbody) return;

  let customers = SALES_DATABASE.topCustomers;
  if (currentFilters.region !== "all") {
    customers = customers.filter(c => c.region === currentFilters.region);
  }

  tbody.innerHTML = customers.map((c, idx) => {
    const adjSales = c.sales * m.scale * m.catMult;
    return `
      <tr>
        <td><strong>#${idx + 1}</strong></td>
        <td>
          <div style="font-weight:600;">${c.name}</div>
          <div style="font-size:10px; color:var(--pbi-text-muted);">${c.id} • ${c.country}</div>
        </td>
        <td><span class="pbi-badge badge-fabric">${c.region}</span></td>
        <td><strong>${formatUSD(adjSales)}</strong></td>
        <td>
          <div style="display:flex; align-items:center; gap:6px;">
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" style="width:${c.marginPct}%;"></div>
            </div>
            <span>${c.marginPct}%</span>
          </div>
        </td>
        <td>${Math.round(c.orders * m.scale)} orders</td>
      </tr>
    `;
  }).join('');
}

function updateWhatIfSimulations() {
  const m = calculateCurrentMetrics();
  const priceDelta = currentFilters.priceAdjust / 100;
  const costDelta = currentFilters.costAdjust / 100;

  const simSales = m.sales * (1 + priceDelta);
  const simCost = m.cost * (1 + costDelta);
  const simProfit = simSales - simCost;
  const simMargin = (simProfit / simSales) * 100;
  const marginShiftBps = ((simMargin - m.marginPct) * 100).toFixed(0);

  const elSimSales = document.getElementById("sim-sales");
  const elSimProfit = document.getElementById("sim-profit");
  const elSimMargin = document.getElementById("sim-margin");
  const elSimShift = document.getElementById("sim-shift");

  if (elSimSales) elSimSales.textContent = formatUSD(simSales);
  if (elSimProfit) elSimProfit.textContent = formatUSD(simProfit);
  if (elSimMargin) elSimMargin.textContent = simMargin.toFixed(1) + '%';
  if (elSimShift) {
    elSimShift.textContent = `${marginShiftBps >= 0 ? '+' : ''}${marginShiftBps} bps`;
    elSimShift.className = marginShiftBps >= 0 ? "badge-growth-pos" : "badge-growth-neg";
  }
}

function exportSalesDataCSV() {
  const m = calculateCurrentMetrics();
  let csv = "Rank,CustomerID,CustomerName,Region,Country,NetSalesUSD,MarginPct,Orders\n";
  SALES_DATABASE.topCustomers.forEach((c, idx) => {
    csv += `${idx + 1},${c.id},"${c.name}",${c.region},${c.country},${(c.sales * m.scale).toFixed(2)},${c.marginPct},${c.orders}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", `sales_performance_report_${currentFilters.year}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
