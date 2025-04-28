document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const googleSignInBtn = document.getElementById('googleSignInBtn');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    if (googleSignInBtn) {
        googleSignInBtn.addEventListener('click', handleGoogleSignIn);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/login/', {
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
            console.log("Response data:", data.access_token);
            localStorage.setItem('token', data.access_token);
            window.location.href = '/cabinet';
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
        const response = await fetch('http://localhost:8000/register/', {
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
            window.location.href = 'login';
        } else {
            showError(data.detail || 'Ошибка регистрации');
        }
    } catch (error) {
        showError('Ошибка соединения с сервером');
    }
}

async function handleGoogleSignIn(e) {
    e.preventDefault();

    google.accounts.id.initialize({
        client_id: "388636973029-gktni9q43lprm1m1buf2t03pumelderr.apps.googleusercontent.com",
        callback: async (response) => {
            console.log("Google response:", response);

            const id_token = response.credential;

            try {
                const serverResponse = await fetch('http://localhost:8000/user/google', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id_token: id_token
                    })
                });

                const data = await serverResponse.json();

                if (serverResponse.ok) {
                    localStorage.setItem('token', data.access_token);
                    window.location.href = '/cabinet';
                } else {
                    showError(data.detail || 'Ошибка входа через Google');
                }
            } catch (error) {
                showError('Ошибка соединения с сервером');
            }
        }
    });

    google.accounts.id.prompt();  // Показать всплывающее окно выбора аккаунта
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    setTimeout(() => errorDiv.textContent = '', 5000);
}