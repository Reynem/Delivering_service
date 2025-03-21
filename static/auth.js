
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`http://localhost:8000/user/login/${encodeURIComponent(email)}/${encodeURIComponent(password)}`);
        const data = await response.json();

        if (response.status === 200) {
            window.location.href = 'index.html';
        } else {
            showError(data.detail || 'Ошибка входа');
        }
    } catch (error) {
        showError('Ошибка соединения с сервером');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/user/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = 'login.html';
        } else {
            showError(data.detail || 'Ошибка регистрации');
        }
    } catch (error) {
        showError('Ошибка соединения с сервером');
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    setTimeout(() => errorDiv.textContent = '', 5000);
}