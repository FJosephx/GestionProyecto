document.addEventListener('DOMContentLoaded', function () {
    const filtroForm = document.getElementById('filtroForm');
    if (!filtroForm) return;

    filtroForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(filtroForm);
        const params = new URLSearchParams(formData);

        fetch(`/api/filtrar/?${params}`)
            .then(response => response.json())
            .then(data => {
                actualizarDashboardData(data);
                initializeCharts();
            })
            .catch(error => console.error('Error en el filtro:', error));
    });
});

function actualizarDashboardData(data) {
    if (!window.dashboardData) return;

    // Actualizar datos de proyectos
    window.dashboardData.proyectos.data = [
        data.proyectos_activos,
        data.proyectos_completados,
        data.proyectos_pendientes
    ];

    // Actualizar datos de tareas
    if (window.dashboardData.tareas) {
        window.dashboardData.tareas.data = [
            data.tareas_completadas,
            data.tareas_en_progreso,
            data.tareas_pendientes
        ];
    }

    // Actualizar progreso si existe
    if (window.dashboardData.progreso && data.progreso_mensual) {
        window.dashboardData.progreso.data = data.progreso_mensual;
    }

    // Actualizar asignaciones si existen
    if (window.dashboardData.asignaciones && data.asignaciones_data) {
        window.dashboardData.asignaciones.labels = data.asignaciones_labels;
        window.dashboardData.asignaciones.data = data.asignaciones_data;
    }
}

function actualizarGraficos(data) {
    tareasChart.data.datasets[0].data = [data.tareas_completadas, data.tareas_pendientes];
    tareasChart.update();

    proyectosChart.data.datasets[0].data = [data.proyectos_activos, data.proyectos_finalizados];
    proyectosChart.update();
}

function actualizarProyectos(html) {
    const container = document.getElementById('proyectosContainer');
    container.innerHTML = html;
}

function actualizarAvancePromedio(valor) {
    const avanceElement = document.getElementById('avancePromedioGeneral');
    if (avanceElement) {
        avanceElement.textContent = valor + '%';
    }
}
