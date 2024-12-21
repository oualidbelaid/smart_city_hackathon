document.addEventListener('DOMContentLoaded', function() {
    const filterInput = document.getElementById('filter-input');
    const transportItems = document.querySelectorAll('.transport-item');

    filterInput.addEventListener('input', function() {
        const filterValue = filterInput.value.toLowerCase();

        transportItems.forEach(item => {
            const type = item.dataset.type.toLowerCase();
            const destination = item.dataset.destination.toLowerCase();
            const schedule = item.dataset.schedule.toLowerCase();
            const text = item.textContent.toLowerCase();

            if (type.includes(filterValue) || destination.includes(filterValue) || schedule.includes(filterValue) || text.includes(filterValue)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});