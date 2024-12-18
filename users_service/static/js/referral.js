document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('referral-code');
    const applyButton = document.getElementById('apply-button');
    const validationMessage = document.getElementById('validation-message');

    inputField.addEventListener('input', function() {
        if (inputField.value.length === 6) {
            const referralCode = inputField.value.trim();
            fetch(`/api/v1/users/validate-referral/${referralCode}`)
                .then(response => {
                    if (response.status === 200) {
                        response.json().then(data => {
                            validationMessage.textContent = data.detail;
                            validationMessage.style.color = 'green';
                            applyButton.disabled = false;
                        });
                    } else {
                        response.json().then(data => {
                            validationMessage.textContent = data.detail;
                            validationMessage.style.color = 'red';
                            applyButton.disabled = true;
                        });
                    }
                });
        } else {
            applyButton.disabled = true;
            validationMessage.textContent = '';
        }
    });

    applyButton.addEventListener('click', function() {
        console.log('Response status:');
        const referralCode = inputField.value.trim();

        fetch('/api/v1/users/apply_referral/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ referral_code: referralCode })
        })
        .then(response => {
            console.log('Response status:', response.status); // Логирование статуса ответа
            if (response.status === 200) {
                response.json().then(data => {
                    validationMessage.textContent = "Реферальный код успешно применён!";
                    validationMessage.style.color = 'green';
                });
            } else {
                response.json().then(data => {
                    validationMessage.textContent = "Не удалось применить реферальный код.";
                    validationMessage.style.color = 'red';
                });
            }
        });
    });
});
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

function getCSRFToken() {
    const name = 'csrftoken';
    const value = document.cookie.split(';').find(row => row.startsWith(name)).split('=')[1];
    return value;
}