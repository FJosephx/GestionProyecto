// Declaramos globalmente
var tareasChart, proyectosChart;

document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de Tareas
    var tareasCtx = document.getElementById('tareasChart');
    if (tareasCtx) {
        tareasChart = new Chart(tareasCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Completadas', 'Pendientes'],
                datasets: [{
                    data: window.chartDataTareas,
                    backgroundColor: ['#198754', '#ffc107'],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1000,
                    easing: 'easeOutBounce'
                }
            }
        });
    }

    // Gráfico de Proyectos
    var proyectosCtx = document.getElementById('proyectosChart');
    if (proyectosCtx) {
        proyectosChart = new Chart(proyectosCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Activos', 'Finalizados'],
                datasets: [{
                    label: 'Cantidad',
                    data: window.chartDataProyectos,
                    backgroundColor: ['#0d6efd', '#198754'],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuart'
                }
            }
        });
    }
});
