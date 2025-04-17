async function connectTelegram() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/user/telegram/request-link', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при запросе временного токена');
        }

        const data = await response.json();
        alert(`Отправьте боту команду:\n/start ${data.temp_token}`);
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось получить временный токен для Telegram');
    }
}

// Загрузка данных пользователя
async function loadUserData() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        const userResponse = await fetch('http://localhost:8000/users/me/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!userResponse.ok) throw new Error('Ошибка загрузки данных пользователя');

        const userData = await userResponse.json();

        // Заполнение основных данных
        document.getElementById('userEmail').textContent = userData.email;
        document.getElementById('userName').textContent = userData.name || 'Не указано';
        document.getElementById('userPhone').textContent = userData.phone || 'Не указан';
        document.getElementById('userAddress').textContent = userData.address || 'Не указан';

        // Загрузка статуса Telegram
        const telegramResponse = await fetch('http://localhost:8000/users/me/telegram', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const telegramChatIdSpan = document.getElementById('telegramChatId');
        const connectTelegramButton = document.querySelector('.security-section button');

        if (telegramResponse.ok) {
            const telegramData = await telegramResponse.json();
            if (telegramData.telegram_id) { // Проверяем, что telegram_id не null и не undefined
                telegramChatIdSpan.textContent = telegramData.telegram_id;
                connectTelegramButton.style.display = 'none'; // Скрываем кнопку
            } else {
                telegramChatIdSpan.textContent = 'Не привязан';
                connectTelegramButton.style.display = 'block'; // Показываем кнопку
            }
        } else {
            console.error('Ошибка загрузки статуса Telegram');
            telegramChatIdSpan.textContent = 'Ошибка загрузки';
            connectTelegramButton.style.display = 'block'; // Показываем кнопку на случай ошибки
        }

    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить данные профиля');
        logout();
    }
}

// Выход из системы
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

// Показать форму редактирования
function showEditForm() {
    document.getElementById('editForm').style.display = 'block';
    document.getElementById('editName').value = document.getElementById('userName').textContent;
    document.getElementById('editPhone').value = document.getElementById('userPhone').textContent;
    document.getElementById('editAddress').value = document.getElementById('userAddress').textContent;
}

// Скрыть форму редактирования
function hideEditForm() {
    document.getElementById('editForm').style.display = 'none';
}

// Отправка изменений
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const updateData = {
        name: document.getElementById('editName').value,
        phone: document.getElementById('editPhone').value,
        address: document.getElementById('editAddress').value
    };

    try {
        const response = await fetch('http://localhost:8000/user/profile', {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updateData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка обновления');
        }

        // Обновление интерфейса
        document.getElementById('userName').textContent = updateData.name || 'Не указано';
        document.getElementById('userPhone').textContent = updateData.phone || 'Не указан';
        document.getElementById('userAddress').textContent = updateData.address || 'Не указан';

        hideEditForm();
        alert('Данные успешно обновлены!');

    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при обновлении: ' + error.message);
    }
});

// Инициализация
document.addEventListener('DOMContentLoaded', loadUserData);
document.getElementById('logoutButton').addEventListener('click', logout);