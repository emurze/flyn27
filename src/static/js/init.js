document.addEventListener('DOMContentLoaded', function () {
    const table = document.getElementById('entriesTable');
    if (table && window.jQuery && $.fn.dataTable) {
        $(table).DataTable();
    }
});