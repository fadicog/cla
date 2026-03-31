// Advanced Charts Initialization
// This script creates all Chart.js visualizations for the Advanced Reports section

// Data embedded from advanced_charts_data.json
const advancedChartsData = {
  "funnel": [
    {"stage": "S00", "label": "Request Created", "count": 500, "drop_off_pct": 0},
    {"stage": "S08", "label": "Request Opened", "count": 478, "drop_off_pct": 4.4},
    {"stage": "S20", "label": "Consent Screen", "count": 435, "drop_off_pct": 9.0},
    {"stage": "S21", "label": "Reviewing Docs", "count": 405, "drop_off_pct": 6.9},
    {"stage": "S30", "label": "Docs Collected", "count": 368, "drop_off_pct": 9.1},
    {"stage": "S31", "label": "Verification Complete", "count": 352, "drop_off_pct": 4.3},
    {"stage": "S40", "label": "Success", "count": 328, "drop_off_pct": 6.8}
  ],
  "sp_performance": [
    {"sp": "Botim", "notification": 55.0, "qr": 100.0, "redirect": 100.0},
    {"sp": "Etisalat Retail", "notification": 63.6, "qr": 66.7, "redirect": 75.0},
    {"sp": "InsureOne (Premier Insurance Brokers L.L.C-O.P.C)", "notification": 31.6, "qr": 33.3, "redirect": 66.7},
    {"sp": "ADNIC", "notification": 78.6, "qr": 71.4, "redirect": 80.0},
    {"sp": "National Bonds Corporation Sole Proprietorship P.S.C.", "notification": 40.0, "qr": 62.5, "redirect": 100.0},
    {"sp": "ADCB", "notification": 56.2, "qr": 75.0, "redirect": 60.0},
    {"sp": "Lulu", "notification": 80.0, "qr": 55.6, "redirect": 100.0},
    {"sp": "FAB Retail Banking", "notification": 85.7, "qr": 66.7, "redirect": 85.7},
    {"sp": "Beyon Money", "notification": 40.0, "qr": 83.3, "redirect": 100.0},
    {"sp": "Arab Bank", "notification": 55.0, "qr": 100.0, "redirect": 100.0}
  ],
  "error_distribution": [
    {"label": "Technical Error", "count": 24},
    {"label": "Expired", "count": 47},
    {"label": "User Aborted", "count": 89},
    {"label": "Not Eligible", "count": 12}
  ],
  "step_latency": [
    {"transition": "Review Docs", "avg_seconds": 7.9},
    {"transition": "Collecting Docs", "avg_seconds": 2.0},
    {"transition": "Verification", "avg_seconds": 6.89},
    {"transition": "Final Submit", "avg_seconds": 3.16}
  ],
  "platform_channel": [
    {"platform": "ios", "notification": 61.7, "qr": 62.3, "redirect": 87.3},
    {"platform": "android", "notification": 58.1, "qr": 67.8, "redirect": 75.7}
  ],
  "doc_complexity": [
    {"label": "1 doc", "success_rate": 59.1, "count": 186},
    {"label": "2 docs", "success_rate": 71.6, "count": 257},
    {"label": "3 docs", "success_rate": 59.6, "count": 57},
    {"label": "4+ docs", "success_rate": 0, "count": 0}
  ],
  "weekly_trend": [
    {"date": "2025-11-01", "success_rate": 71.4},
    {"date": "2025-11-02", "success_rate": 55.6},
    {"date": "2025-11-03", "success_rate": 71.4},
    {"date": "2025-11-04", "success_rate": 66.7},
    {"date": "2025-11-05", "success_rate": 71.4},
    {"date": "2025-11-06", "success_rate": 58.3},
    {"date": "2025-11-07", "success_rate": 66.7},
    {"date": "2025-11-08", "success_rate": 56.2},
    {"date": "2025-11-09", "success_rate": 68.8},
    {"date": "2025-11-10", "success_rate": 63.3},
    {"date": "2025-11-11", "success_rate": 57.1},
    {"date": "2025-11-12", "success_rate": 80.0},
    {"date": "2025-11-13", "success_rate": 71.4},
    {"date": "2025-11-14", "success_rate": 83.3},
    {"date": "2025-11-15", "success_rate": 70.6},
    {"date": "2025-11-16", "success_rate": 84.6},
    {"date": "2025-11-17", "success_rate": 61.9},
    {"date": "2025-11-18", "success_rate": 69.2},
    {"date": "2025-11-19", "success_rate": 60.9},
    {"date": "2025-11-20", "success_rate": 80.0},
    {"date": "2025-11-21", "success_rate": 58.8},
    {"date": "2025-11-22", "success_rate": 65.2},
    {"date": "2025-11-23", "success_rate": 66.7},
    {"date": "2025-11-24", "success_rate": 41.2},
    {"date": "2025-11-25", "success_rate": 73.9},
    {"date": "2025-11-26", "success_rate": 58.8},
    {"date": "2025-11-27", "success_rate": 66.7},
    {"date": "2025-11-28", "success_rate": 47.4}
  ],
  "path_analysis": [
    {"path": "S00 > S01 > S02 > S03 > S08...", "outcome": "Success", "count": 121, "percentage": 24.2},
    {"path": "S00 > S01 > S02 > S03 > S08...", "outcome": "Success", "count": 51, "percentage": 10.2},
    {"path": "S00 > S04 > S05 > S08 > S10...", "outcome": "Success", "count": 49, "percentage": 9.8},
    {"path": "S00 > S06 > S07 > S08 > S10...", "outcome": "Success", "count": 41, "percentage": 8.2},
    {"path": "S00 > S01 > S02 > S03 > S08...", "outcome": "Aborted", "count": 37, "percentage": 7.4}
  ],
  "bottleneck": [
    {"stage": "Opening", "count": 22},
    {"stage": "Doc Availability Check", "count": 43},
    {"stage": "Consent Screen", "count": 67},
    {"stage": "Collection & Verification", "count": 40}
  ]
};

// Initialize all charts when DOM is ready
function initAdvancedCharts() {
    // 1. FUNNEL CHART (Horizontal Bar)
    const funnelCtx = document.getElementById('funnelChart');
    if (funnelCtx) {
        new Chart(funnelCtx, {
            type: 'bar',
            data: {
                labels: advancedChartsData.funnel.map(d => d.label),
                datasets: [{
                    label: 'Requests',
                    data: advancedChartsData.funnel.map(d => d.count),
                    backgroundColor: [
                        '#4CAF50',
                        '#66BB6A',
                        '#81C784',
                        '#FFA726',
                        '#FF7043',
                        '#EF5350',
                        '#2196F3'
                    ],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const idx = context.dataIndex;
                                const count = context.parsed.x;
                                const dropOff = advancedChartsData.funnel[idx].drop_off_pct;
                                return [
                                    `Requests: ${count}`,
                                    `Drop-off: ${dropOff}%`
                                ];
                            }
                        }
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'end',
                        formatter: (value, ctx) => {
                            const dropOff = advancedChartsData.funnel[ctx.dataIndex].drop_off_pct;
                            return `${value} (${dropOff}% drop)`;
                        },
                        color: '#333',
                        font: {weight: 'bold', size: 11}
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {display: true, text: 'Number of Requests'}
                    }
                }
            }
        });
    }

    // 2. SP PERFORMANCE BY CHANNEL (Grouped Bar)
    const spPerfCtx = document.getElementById('spPerformanceChart');
    if (spPerfCtx) {
        const spLabels = advancedChartsData.sp_performance.map(d => {
            // Shorten long SP names
            const sp = d.sp;
            return sp.length > 30 ? sp.substring(0, 27) + '...' : sp;
        });

        new Chart(spPerfCtx, {
            type: 'bar',
            data: {
                labels: spLabels,
                datasets: [
                    {
                        label: 'Notification',
                        data: advancedChartsData.sp_performance.map(d => d.notification),
                        backgroundColor: '#e91e63'
                    },
                    {
                        label: 'QR',
                        data: advancedChartsData.sp_performance.map(d => d.qr),
                        backgroundColor: '#009688'
                    },
                    {
                        label: 'Redirect',
                        data: advancedChartsData.sp_performance.map(d => d.redirect),
                        backgroundColor: '#3f51b5'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {position: 'top'},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {display: true, text: 'Success Rate (%)'}
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }

    // 3. ERROR DISTRIBUTION (Doughnut)
    const errorCtx = document.getElementById('errorDistChart');
    if (errorCtx) {
        new Chart(errorCtx, {
            type: 'doughnut',
            data: {
                labels: advancedChartsData.error_distribution.map(d => d.label),
                datasets: [{
                    data: advancedChartsData.error_distribution.map(d => d.count),
                    backgroundColor: ['#f44336', '#ff9800', '#ff5722', '#ffc107'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {position: 'right'},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // 4. STEP LATENCY (Bar Chart)
    const latencyCtx = document.getElementById('latencyChart');
    if (latencyCtx) {
        new Chart(latencyCtx, {
            type: 'bar',
            data: {
                labels: advancedChartsData.step_latency.map(d => d.transition),
                datasets: [{
                    label: 'Average Latency (seconds)',
                    data: advancedChartsData.step_latency.map(d => d.avg_seconds),
                    backgroundColor: '#ff9800',
                    borderColor: '#f57c00',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y}s average`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {display: true, text: 'Seconds'}
                    }
                }
            }
        });
    }

    // 5. PLATFORM x CHANNEL MATRIX (Grouped Bar)
    const platformChannelCtx = document.getElementById('platformChannelChart');
    if (platformChannelCtx) {
        new Chart(platformChannelCtx, {
            type: 'bar',
            data: {
                labels: ['Notification', 'QR', 'Redirect'],
                datasets: [
                    {
                        label: 'iOS',
                        data: [
                            advancedChartsData.platform_channel[0].notification,
                            advancedChartsData.platform_channel[0].qr,
                            advancedChartsData.platform_channel[0].redirect
                        ],
                        backgroundColor: '#42a5f5'
                    },
                    {
                        label: 'Android',
                        data: [
                            advancedChartsData.platform_channel[1].notification,
                            advancedChartsData.platform_channel[1].qr,
                            advancedChartsData.platform_channel[1].redirect
                        ],
                        backgroundColor: '#66bb6a'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {position: 'top'},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {display: true, text: 'Success Rate (%)'}
                    }
                }
            }
        });
    }

    // 6. DOCUMENT COMPLEXITY (Bar Chart)
    const docComplexityCtx = document.getElementById('docComplexityChart');
    if (docComplexityCtx) {
        const filteredDocs = advancedChartsData.doc_complexity.filter(d => d.count > 0);
        new Chart(docComplexityCtx, {
            type: 'bar',
            data: {
                labels: filteredDocs.map(d => d.label),
                datasets: [{
                    label: 'Success Rate (%)',
                    data: filteredDocs.map(d => d.success_rate),
                    backgroundColor: ['#4caf50', '#8bc34a', '#cddc39'],
                    borderColor: '#388e3c',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const idx = context.dataIndex;
                                const count = filteredDocs[idx].count;
                                return [
                                    `Success Rate: ${context.parsed.y}%`,
                                    `Requests: ${count}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {display: true, text: 'Success Rate (%)'}
                    }
                }
            }
        });
    }

    // 7. WEEKLY TREND (Line Chart)
    const weeklyTrendCtx = document.getElementById('weeklyTrendChart');
    if (weeklyTrendCtx) {
        const dates = advancedChartsData.weekly_trend.map(d => {
            const date = new Date(d.date);
            return `${date.getMonth() + 1}/${date.getDate()}`;
        });

        new Chart(weeklyTrendCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Success Rate',
                    data: advancedChartsData.weekly_trend.map(d => d.success_rate),
                    borderColor: '#2196f3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return advancedChartsData.weekly_trend[context[0].dataIndex].date;
                            },
                            label: function(context) {
                                return `Success Rate: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {display: true, text: 'Success Rate (%)'}
                    },
                    x: {
                        title: {display: true, text: 'Date (Nov 2025)'},
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }

    // 8. PATH ANALYSIS (Horizontal Bar)
    const pathAnalysisCtx = document.getElementById('pathAnalysisChart');
    if (pathAnalysisCtx) {
        const colors = advancedChartsData.path_analysis.map(d =>
            d.outcome === 'Success' ? '#4caf50' : '#f44336'
        );

        new Chart(pathAnalysisCtx, {
            type: 'bar',
            data: {
                labels: advancedChartsData.path_analysis.map((d, i) => `Path ${i + 1}`),
                datasets: [{
                    label: 'Request Count',
                    data: advancedChartsData.path_analysis.map(d => d.count),
                    backgroundColor: colors,
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                const idx = context[0].dataIndex;
                                return advancedChartsData.path_analysis[idx].path;
                            },
                            label: function(context) {
                                const idx = context.dataIndex;
                                const data = advancedChartsData.path_analysis[idx];
                                return [
                                    `Outcome: ${data.outcome}`,
                                    `Count: ${data.count} (${data.percentage}%)`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {display: true, text: 'Number of Requests'}
                    }
                }
            }
        });
    }

    // 9. BOTTLENECK WATERFALL (Bar Chart)
    const bottleneckCtx = document.getElementById('bottleneckChart');
    if (bottleneckCtx) {
        new Chart(bottleneckCtx, {
            type: 'bar',
            data: {
                labels: advancedChartsData.bottleneck.map(d => d.stage),
                datasets: [{
                    label: 'Failure Count',
                    data: advancedChartsData.bottleneck.map(d => d.count),
                    backgroundColor: ['#ff9800', '#f44336', '#d32f2f', '#b71c1c'],
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {display: false},
                    title: {display: false},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = 172; // Total failures
                                const pct = ((context.parsed.y / total) * 100).toFixed(1);
                                return `${context.parsed.y} failures (${pct}% of all failures)`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {display: true, text: 'Number of Failures'}
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
}

// Call initialization when section becomes visible or page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdvancedCharts);
} else {
    initAdvancedCharts();
}
