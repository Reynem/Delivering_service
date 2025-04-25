print("Скрипт работает");

const db = db.getSiblingDB("dishesDB");

db.createCollection("dishes");
db.createCollection("Users");
db.createCollection("carts");
db.createCollection("admins");

print("Инициализация базы данных dishesDB завершена.");
