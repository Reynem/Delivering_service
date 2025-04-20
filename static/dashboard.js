document.getElementById('addDishForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));

    try {
        const response = await fetch('/api/add-dish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            location.reload();
        } else {
            alert('Error adding dish');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Delete Dish
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this dish?')) {
            const dishName = btn.dataset.id;

            try {
                const response = await fetch(`/api/delete-dish/${dishName}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
                    }
                });

                if (response.ok) {
                    btn.closest('tr').remove();
                } else {
                    alert('Error deleting dish');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });
});

// Edit Dish
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const dish = JSON.parse(btn.dataset.dish);
        const form = document.getElementById('editDishForm');

        form.elements.name.value = dish.name;
        form.elements.category.value = dish.category;
        form.elements.price.value = dish.price;
        form.elements.description.value = dish.description;
    });
});

document.getElementById('editDishForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));

    try {
        const response = await fetch('/change-dish/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
            },
            body: JSON.stringify({
                old_value: formData.name,
                field: 'full', // или конкретное поле для изменения
                new_value: {
                    category: formData.category,
                    price: formData.price,
                    description: formData.description
                }
            })
        });

        if (response.ok) {
            location.reload();
        } else {
            alert('Error updating dish');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});