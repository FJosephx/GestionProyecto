// Desvanecer automáticamente mensajes flash
document.addEventListener('DOMContentLoaded', function () {
    const alertList = document.querySelectorAll('.alert');
    alertList.forEach(function (alert) {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => {
                let alertInstance = new bootstrap.Alert(alert);
                alertInstance.close();
            }, 500);
        }, 3000);
    });

    // Inicializar Flatpickr en inputs con clase datepicker
    flatpickr(".datepicker", {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "d/m/Y",
        allowInput: true,
        locale: "es"
    });
});
