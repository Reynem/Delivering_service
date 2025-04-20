// --- Edit User ---
document.querySelectorAll('.edit-user-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const userEmail = btn.dataset.userEmail;
        const form = document.getElementById('editUserForm');

        console.log(`Workspaceing details for user: ${userEmail}`);
        // Example of manually finding data from the table (less ideal)
        const row = btn.closest('tr');
        const name = row.cells[0].textContent;
        const phone = row.cells[2].textContent;
        const address = row.cells[3].textContent;
        // --- End Placeholder ---

        // Populate the modal form
        form.elements.email.value = userEmail; // Hidden input for identifier
        form.elements.display_email.value = userEmail; // Readonly field
        form.elements.name.value = name !== 'N/A' ? name : '';
        form.elements.phone.value = phone !== 'N/A' ? phone : '';
        form.elements.address.value = address !== 'N/A' ? address : '';
        // Populate other fields...
    });
});

document.getElementById('editUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const userEmail = formData.get('email'); // Get the identifier
    const updatedData = { // Construct payload based on your API
        name: formData.get('name'),
        phone: formData.get('phone'),
        address: formData.get('address'),
        // Add other fields...
    };

    const apiUrl = `/api/admin/users/${userEmail}`; // Example API endpoint structure

    try {
        const response = await fetch(apiUrl, {
            method: 'PUT', // Or PATCH
            headers: {
                'Content-Type': 'application/json',
                // Add Authorization header if needed
                 'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
            },
            body: JSON.stringify(updatedData)
        });

        if (response.ok) {
            alert('User updated successfully!');
            location.reload(); // Reload the page to see changes
        } else {
            const errorData = await response.json();
            alert(`Error updating user: ${errorData.detail || response.statusText}`);
        }
    } catch (error) {
        console.error('Error updating user:', error);
        alert('An error occurred while updating the user.');
    }
});

// --- Delete User ---
document.querySelectorAll('.delete-user-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const userEmail = btn.dataset.userEmail;
        if (confirm(`Are you sure you want to delete user ${userEmail}?`)) {

            const apiUrl = `/admin/users/delete/${userEmail}`; // Example API endpoint structure

            try {
                const response = await fetch(apiUrl, {
                    method: 'DELETE',
                    headers: {
                        // Add Authorization header if needed
                         'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
                    }
                });

                if (response.ok) {
                    alert('User deleted successfully!');
                    // Remove the row from the table
                    btn.closest('tr').remove();
                    // Or reload the page: location.reload();
                } else {
                     const errorData = await response.json();
                    alert(`Error deleting user: ${errorData.detail || response.statusText}`);
                }
            } catch (error) {
                console.error('Error deleting user:', error);
                 alert('An error occurred while deleting the user.');
            }
        }
    });
});