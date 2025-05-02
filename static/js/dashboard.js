// Variables globales para los gráficos
let charts = {};

// Función para destruir gráficos existentes
function destroyCharts() {
    Object.values(charts).forEach(chart => {
        if (chart instanceof Chart) {
            chart.destroy();
        }
    });
    charts = {};
}

// Configuración común para los gráficos
const commonOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 20,
                usePointStyle: true
            }
        }
    }
};

// Función para inicializar los gráficos
function initializeCharts() {
    // Destruir gráficos existentes si los hay
    destroyCharts();

    // Gráfico de Proyectos (Pie)
    const proyectosCtx = document.getElementById('proyectosChart');
    if (proyectosCtx && window.dashboardData.proyectos) {
        charts.proyectos = new Chart(proyectosCtx, {
            type: 'doughnut',
            data: {
                labels: window.dashboardData.proyectos.labels,
                datasets: [{
                    data: window.dashboardData.proyectos.data,
                    backgroundColor: window.dashboardData.proyectos.colors,
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                cutout: '60%',
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Distribución de Proyectos',
                        padding: {
                            top: 10,
                            bottom: 30
                        }
                    }
                }
            }
        });
    }

    // Gráfico de Prioridades (Bar)
    const prioridadesCtx = document.getElementById('prioridadesChart');
    if (prioridadesCtx && window.dashboardData.prioridades) {
        charts.prioridades = new Chart(prioridadesCtx, {
            type: 'bar',
            data: {
                labels: window.dashboardData.prioridades.labels,
                datasets: [{
                    label: 'Cantidad de Tareas',
                    data: window.dashboardData.prioridades.data,
                    backgroundColor: window.dashboardData.prioridades.colors,
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Tareas por Nivel de Prioridad',
                        padding: {
                            top: 10,
                            bottom: 30
                        }
                    }
                }
            }
        });
    }

    // Gráfico de Progreso (Line)
    const progresoCtx = document.getElementById('progresoChart');
    if (progresoCtx && window.dashboardData.progreso) {
        charts.progreso = new Chart(progresoCtx, {
            type: 'line',
            data: {
                labels: window.dashboardData.progreso.labels,
                datasets: [{
                    label: 'Progreso Mensual (%)',
                    data: window.dashboardData.progreso.data,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Porcentaje de Avance'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Progreso Mensual del Proyecto',
                        padding: {
                            top: 10,
                            bottom: 30
                        }
                    }
                }
            }
        });
    }

    // Gráfico de Asignaciones (Horizontal Bar)
    const asignacionesCtx = document.getElementById('asignacionesChart');
    if (asignacionesCtx && window.dashboardData.asignaciones) {
        charts.asignaciones = new Chart(asignacionesCtx, {
            type: 'bar',
            data: {
                labels: window.dashboardData.asignaciones.labels,
                datasets: [{
                    label: 'Tareas Asignadas',
                    data: window.dashboardData.asignaciones.data,
                    backgroundColor: window.dashboardData.asignaciones.colors,
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Top 5 Miembros con más Tareas',
                        padding: {
                            top: 10,
                            bottom: 30
                        }
                    }
                }
            }
        });
    }
}

// Inicializar los gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    if (window.dashboardData) {
        initializeCharts();
        
        // Manejar el redimensionamiento de la ventana
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function() {
                initializeCharts();
            }, 250);
        });
    }
});
