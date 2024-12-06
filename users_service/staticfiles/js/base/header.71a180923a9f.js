document.getElementById('logout-button').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/v1/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'include'
        });

        if (response.ok) {
            window.location.href = '/login/';
        } else {
            console.error('Ошибка выхода');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
});

document.getElementById('user-list-button').addEventListener('click', async () => {
    window.location.href = ('/users/');
});

document.getElementById('my-profile-button').addEventListener('click', function () {
    const url = this.getAttribute('data-url');
    window.location.href = url;
});

function getCSRFToken() {
    const name = 'csrftoken';
    const value = document.cookie.split(';').find(row => row.startsWith(name)).split('=')[1];
    return value;
}