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
