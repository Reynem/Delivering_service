// static/main.js

document.addEventListener('DOMContentLoaded', function() {
    loadMenu(); // Функция для загрузки меню (предполагается, что она у вас есть)
    setupCartEventListeners();
    updateCartDisplay(); // Обновляем отображение корзины при загрузке страницы
});

function getToken() {
    // Ваша функция для получения токена авторизации
    return localStorage.getItem('token');
}

function setupCartEventListeners() {
    const cartButton = document.getElementById('cartButton');
    const cartPopup = document.getElementById('cartPopup');
    const clearCartButton = document.getElementById('clearCart');
    const checkoutButton = document.getElementById('checkoutButton');
    const menuGrid = document.getElementById('menu'); // Предполагается, что у вас есть элемент с id "menu"

    if (cartButton) {
        cartButton.addEventListener('click', toggleCartPopup);
    }

    // Закрытие корзины при клике вне окна
    document.addEventListener('click', function(event) {
        if (cartPopup && cartButton && !cartPopup.contains(event.target) && !cartButton.contains(event.target)) {
            cartPopup.style.display = 'none';
        }
    });

    if (clearCartButton) {
        clearCartButton.addEventListener('click', clearShoppingCart);
    }

    if (checkoutButton) {
        checkoutButton.addEventListener('click', checkout);
    }

    // Пример: Добавление обработчиков для кнопок "Добавить в корзину" на элементах меню
    if (menuGrid) {
        menuGrid.addEventListener('click', function(event) {
            if (event.target.classList.contains('add-to-cart-button')) {
                const dishName = event.target.dataset.name;
                addToCart(dishName);
            }
        });
    }
}

function toggleCartPopup() {
    const cartPopup = document.getElementById('cartPopup');
    if (cartPopup) {
        cartPopup.style.display = cartPopup.style.display === 'none' ? 'block' : 'none';
        if (cartPopup.style.display === 'block') {
            loadCartItems(); // Загружаем товары при открытии корзины
        }
    }
}

async function addToCart(dishName) {
    const token = getToken();
    if (!token) {
        alert('Пожалуйста, войдите, чтобы добавить товары в корзину.');
        return;
    }

    // Находим кнопку, которая вызвала событие (клик)
    const button = event.target.closest('.add-to-cart-button');
    if (!button) return;

    const price = parseFloat(button.dataset.price);
    const category = button.dataset.category;

    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Если ваша авторизация использует Bearer token
            },
            body: JSON.stringify({
                dish_name: dishName,
                quantity: 1,
                price: price,
                category: category
            })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === "OK") {
                loadCartItems(); // Обновляем отображение корзины после добавления
                updateCartDisplay(); // Обновляем счетчик корзины
            } else {
                console.error('Ошибка при добавлении в корзину:', data.message);
                alert(data.message || 'Не удалось добавить товар в корзину.');
            }
        } else {
            const error = await response.json();
            console.error('Ошибка при добавлении в корзину:', error);
            alert('Не удалось добавить товар в корзину.');
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('Произошла ошибка при добавлении товара в корзину.');
    }
}

async function loadCartItems() {
    const token = getToken();
    if (!token) {
        console.warn('Пользователь не авторизован, не могу загрузить корзину.');
        return;
    }

    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');
    if (!cartItemsContainer || !cartTotalElement) return;

    cartItemsContainer.innerHTML = '<p>Загрузка корзины...</p>';
    cartTotalElement.textContent = 'Итого: 0 ₽';

    try {
        const response = await fetch('/api/cart/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        // Если сессия истекла
        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        if (response.ok) {
            const cartData = await response.json();
            console.log('Данные корзины, полученные от сервера:', cartData);
            if (cartData.status === "OK") {
                displayCartItems(cartData);
            } else {
                console.error('Ошибка при загрузке корзины:', cartData.message);
                cartItemsContainer.innerHTML = `<p>Не удалось загрузить корзину: ${cartData.message}</p>`;
            }
        } else {
            const error = await response.json();
            console.error('Ошибка при загрузке корзины:', error);
            cartItemsContainer.innerHTML = '<p>Не удалось загрузить корзину.</p>';
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        cartItemsContainer.innerHTML = '<p>Произошла ошибка при загрузке корзины.</p>';
    }
}

function displayCartItems(cartData) {
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');
    const cartCountElement = document.getElementById('cartCount');
    if (!cartItemsContainer || !cartTotalElement || !cartCountElement) return;

    cartItemsContainer.innerHTML = ''; // Очищаем предыдущее содержимое

    let totalPrice = 0;
    let totalQuantity = 0;

    if (cartData && cartData.items && Array.isArray(cartData.items)) {
        cartData.items.forEach(item => {
            const cartItemDiv = document.createElement('div');
            cartItemDiv.classList.add('cart-item');
            const itemName = item.dish_name;
            const itemPrice = item.price !== undefined ? item.price : 'Цена не указана';
            const itemQuantity = item.quantity !== undefined ? item.quantity : 0;

            cartItemDiv.innerHTML = `
                <div class="cart-item-details">
                    <span class="cart-item-name">${itemName}</span>
                    <span class="cart-item-price">${itemPrice} ₽</span>
                </div>
                <div class="cart-item-quantity">Кол-во: ${itemQuantity}</div>
                <button class="remove-from-cart-button" data-name="${itemName}">Удалить</button>
            `;
            cartItemsContainer.appendChild(cartItemDiv);
            totalPrice += (itemPrice || 0) * itemQuantity;
            totalQuantity += itemQuantity;
        });

        const parsedTotalPrice = cartData.total_price !== undefined ? cartData.total_price : 0;
        cartTotalElement.textContent = `Итого: ${parsedTotalPrice.toFixed(2)} ₽`;
        cartCountElement.textContent = totalQuantity;

        // Добавляем обработчики для кнопок "Удалить"
        const removeButtons = cartItemsContainer.querySelectorAll('.remove-from-cart-button');
        removeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const dishName = this.dataset.name;
                removeFromCart(dishName);
            });
        });
    } else {
        cartItemsContainer.innerHTML = '<p class="cart-empty">Ваша корзина пуста.</p>';
        cartTotalElement.textContent = 'Итого: 0 ₽';
        cartCountElement.textContent = '0';
    }
}

async function removeFromCart(dishName) {
    const token = getToken();
    if (!token) {
        alert('Пожалуйста, войдите.');
        return;
    }

    try {
        const response = await fetch(`/api/cart/remove/${encodeURIComponent(dishName)}/?quantity=1`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === "OK") {
                loadCartItems(); // Обновляем содержимое корзины
                updateCartDisplay(); // Обновляем счетчик
            } else {
                console.error('Ошибка при удалении из корзины:', data.message);
                alert(data.message || 'Не удалось удалить товар из корзины.');
            }
        } else {
            const error = await response.json();
            console.error('Ошибка при удалении из корзины:', error);
            alert('Не удалось удалить товар из корзины.');
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('Произошла ошибка при удалении товара из корзины.');
    }
}

async function clearShoppingCart() {
    const token = getToken();
    if (!token) {
        alert('Пожалуйста, войдите.');
        return;
    }

    if (confirm('Вы уверены, что хотите очистить корзину?')) {
        try {
            const response = await fetch('/api/cart/clear/', {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === "OK") {
                    loadCartItems(); // Обновляем содержимое корзины
                    updateCartDisplay(); // Обновляем счетчик
                } else {
                    console.error('Ошибка при очистке корзины:', data.message);
                    alert(data.message || 'Не удалось очистить корзину.');
                }
            } else {
                const error = await response.json();
                console.error('Ошибка при очистке корзины:', error);
                alert('Не удалось очистить корзину.');
            }
        } catch (error) {
            console.error('Ошибка сети:', error);
            alert('Произошла ошибка при очистке корзины.');
        }
    }
}

async function checkout() {
    const token = getToken();
    if (!token) {
        alert('Пожалуйста, войдите, чтобы оформить заказ.');
        return;
    }

    try {
        const response = await fetch('/api/orders/create', { // Вам нужно реализовать этот эндпоинт на бэкенде
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
            // В теле запроса можно отправить дополнительную информацию о заказе, если необходимо
            // body: JSON.stringify({})
        });

        if (response.ok) {
            const orderDetails = await response.json();
            alert(`Заказ успешно оформлен! Номер вашего заказа: ${orderDetails.order_id || 'неизвестен'}`);
            clearShoppingCart(); // Очищаем корзину после успешного оформления заказа
        } else {
            const error = await response.json();
            console.error('Ошибка при оформлении заказа:', error);
            alert('Не удалось оформить заказ.');
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('Произошла ошибка при оформлении заказа.');
    }
}

async function updateCartDisplay() {
    const token = getToken();
    const cartCountElement = document.getElementById('cartCount');
    if (!token || !cartCountElement) {
        cartCountElement.textContent = '0';
        return;
    }

    try {
        const response = await fetch('/api/cart/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const cartData = await response.json();
            cartCountElement.textContent = cartData.items ? cartData.items.reduce((sum, item) => sum + item.quantity, 0) : '0';
        } else {
            console.warn('Не удалось получить количество товаров в корзине для отображения.');
            cartCountElement.textContent = '0';
        }
    } catch (error) {
        console.error('Ошибка сети при обновлении счетчика корзины:', error);
        cartCountElement.textContent = '0';
    }
}

// Пример функции для загрузки меню (вам нужно реализовать свою логику)
async function loadMenu() {
    try {
        const response = await fetch('/dishes/'); // Используем ваш эндпоинт для получения всех блюд
        if (response.ok) {
            const dishes = await response.json();
            const menuContainer = document.getElementById('menu');
            if (menuContainer) {
                menuContainer.innerHTML = ''; // Очищаем предыдущее меню
                dishes.forEach(dish => {
                    const dishElement = document.createElement('div');
                    dishElement.classList.add('menu-item'); // Добавьте свой класс для стиля
                    dishElement.innerHTML = `
                        <h3>${dish.name}</h3>
                        <p>Цена: ${dish.price} ₽</p>
                        <button
                            class="add-to-cart-button"
                            data-name="${dish.name}"
                            data-price="${dish.price}"
                            data-category="${dish.category}"
                        >Добавить в корзину</button>
                    `;
                    menuContainer.appendChild(dishElement);
                });
            }
        } else {
            console.error('Не удалось загрузить меню.');
        }
    } catch (error) {
        console.error('Ошибка при загрузке меню:', error);
    }
}

function handleUnauthorized() {
    // Очистим токен и перенаправим на страницу логина
    localStorage.removeItem('token');
    alert('Ваша сессия истекла, пожалуйста, войдите снова.');
    window.location.href = '/login'; // или другой URL страницы логина
}