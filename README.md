# 🍽️ FastAPI Restaurant Website

This project is a simple restaurant website built with **FastAPI**, featuring a **MongoDB** database (with **Motor** and **Beanie ODM**), user authentication, and an admin panel. It demonstrates how to create a full-featured web application using modern Python technologies.

## ✨ Features

* **👤 User Management**
    * Registration and login with **JWT** authentication 🔐
    * User profile management
    * **Telegram bot** integration for notifications 🤖
    * Two-factor authentication via Telegram ✅

* **📊 Admin Panel**
    * Secure admin dashboard
    * User management (view, edit, delete users)
    * Dish management (add, edit, delete dishes) 🍜

* **🛒 Shopping Cart**
    * Add/remove dishes to cart
    * Adjust item quantities
    * Create orders from cart items 📝

* **💾 Database**
    * **MongoDB** with asynchronous access via **Motor** 🍃
    * **Beanie ODM** for document modeling and validation

## 🛠️ Tech Stack

* **Backend:** FastAPI 🚀, Python 3.9+ 🐍
* **Database:** MongoDB with Motor and Beanie ODM 💾
* **Authentication:** JWT tokens 🔐, Argon2 password hashing
* **Frontend:** HTML, Bootstrap 5, JavaScript 🎨
* **Integrations:** Telegram Bot API 🤖

## 📁 Project Structure

```text
├── admin/                 # Admin panel functionality
│   └── router.py          # Admin routes
├── carts/                 # Shopping cart functionality
│   ├── database.py        # Cart database operations
│   ├── models.py          # Cart data models
│   └── router.py          # Cart routes
├── dishes/                # Dish management
│   ├── database.py        # Dish database operations
│   ├── models.py          # Dish data models
│   └── router.py          # Dish routes
├── templates/             # Jinja2 templates
│   └── admin/             # Admin templates
├── static/                # Static files (CSS, JS, images)
├── users/                 # User management
│   ├── api/               # Telegram bot
|   └─── telegram_bot.py   # Telegram bot class
│   ├── auth.py            # Authentication logic
│   ├── database.py        # User database operations
│   ├── encryption.py      # Password encryption
│   └── router.py          # User routes
├── database.py            # Database connection setup
├── main.py                # Application entry point
├── metadata.py            # Metadata tags for API
└── models.py              # Shared data models
```

## 🚀 Getting Started

### ✅ Prerequisites

* Python 3.9+ 🐍
* MongoDB 🍃
* Telegram Bot Token (for notification features) 🤖

### ⬇️ Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Reynem/Delivering_service.git
    cd Delivering_service
    ```

2.  **Create a `.env` file** in the project root with the following variables:

    ```dotenv
    SECRET_KEY=your_secret_key_here
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
    ```

3.  **Run MongoDB:**

    run docker-compose to start MongoDB. Name of database - dishesDB
    ```bash
    docker-compose up -d
    ```

5.  **Start the application:**

    ```bash
    python main.py
    ```

    Access the website at `http://localhost:8000` and the admin panel at `http://localhost:8000/admin/login` (default credentials: `admin`/`admin`).

## 📡 API Endpoints

* **Users** 🧑‍💻
    * `POST /login/` - User login
    * `POST /register/` - User registration
    * `GET /users/me/` - Get current user details
    * `PATCH /user/profile/` - Update user profile
    * `POST /user/telegram/request-link` - Request Telegram account linking
    * `POST /user/telegram/link` - Link Telegram account

* **Dishes** 🍲
    * `GET /dishes/` - Get all dishes
    * `GET /api/dish/{category}` - Get dishes by category
    * `POST /api/add-dish` - Add a new dish (admin only)
    * `DELETE /api/delete-dish/{name}` - Delete a dish (admin only)
    * `POST /change-dish/` - Update dish details (admin only)

* **Cart** 🛒
    * `POST /api/cart/add` - Add item to cart
    * `GET /api/cart/` - Get cart items
    * `DELETE /api/cart/clear/` - Clear cart
    * `DELETE /api/cart/remove/{dish_name}/` - Remove item from cart
    * `PUT /api/cart/update/{dish_name}/` - Update cart item quantity
    * `POST /api/orders/create` - Create order from cart

* **Admin** 👑
    * `GET /admin/login` - Admin login page
    * `POST /admin/login` - Admin login action
    * `GET /admin/dashboard` - Admin dashboard
    * `GET /admin/users` - Admin user management
    * `DELETE /admin/users/delete/{email}` - Delete user (admin only)

## 🛡️ Security Features

* Password hashing with Argon2 🔒
* JWT authentication with expiring tokens
* Session-based admin authentication
* CORS protection ✅
* Input validation via Pydantic models

## ⚖️ License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
