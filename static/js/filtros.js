document.addEventListener('DOMContentLoaded', function () {
    const filtroForm = document.getElementById('filtroForm');

    filtroForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(filtroForm);
        const params = new URLSearchParams(formData);

        fetch(`/api/filtrar/?${params}`)
            .then(response => response.json())
            .then(data => {
                actualizarGraficos(data);
                actualizarProyectos(data.proyectos_html);
                actualizarAvancePromedio(data.avance_promedio);
            })
            .catch(error => console.error('Error en el filtro:', error));
    });
});

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
