function confirmDelete(event, url) {
    event.preventDefault();
    const form = document.getElementById('deleteForm');
    form.action = url;
    const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    modal.show();
}
