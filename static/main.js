


async function fetchDishes() {
            try {
                const response = await fetch("http://localhost:8000/dishes");
                if (!response.ok) {
                    throw new Error("Ошибка загрузки данных");
                }
                const dishes = await response.json();
                renderDishes(dishes);
            } catch (error) {
                console.error("Ошибка при загрузке блюд:", error);
            }
        }

        function renderDishes(dishes) {
            const menuContainer = document.getElementById("menu");
            menuContainer.innerHTML = "";

            dishes.forEach(dish => {
                const dishElement = document.createElement("div");
                dishElement.classList.add("dish");
                dishElement.innerHTML = `<h3>${dish.name}</h3><p>${dish.category}</p><p>${dish.price} руб.</p>`;
                menuContainer.appendChild(dishElement);
            });
        }

        fetchDishes();

 document.addEventListener('DOMContentLoaded', function() {
        const token = localStorage.getItem('token');
        const loginLink = document.getElementById('loginLink');
        const registerLink = document.getElementById('registerLink');
        const cabinetLink = document.getElementById('cabinetLink');
        const logoutButton = document.getElementById('logoutButton');
        const cartButton = document.getElementById('cartButton');
        const cartPopup = document.getElementById('cartPopup');

        if (token) {
            loginLink.style.display = 'none';
            registerLink.style.display = 'none';
            cabinetLink.style.display = 'inline-block';
            logoutButton.style.display = 'inline-block';
        } else {
            cabinetLink.style.display = 'none';
            logoutButton.style.display = 'none';
            loginLink.style.display = 'inline-block';
            registerLink.style.display = 'inline-block';
        }

        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('token');
            window.location.reload();
        });

        cartButton.addEventListener('click', function() {
            cartPopup.style.display = cartPopup.style.display === 'none' ? 'block' : 'none';
        });

        document.addEventListener('click', function(event) {
            if (!cartPopup.contains(event.target) && !cartButton.contains(event.target)) {
                cartPopup.style.display = 'none';
            }
        });
    });
