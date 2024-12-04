document.querySelectorAll('.profile-container').forEach(container => {
    container.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        window.location.href = url;
    });
});