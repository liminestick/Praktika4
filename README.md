# Praktika4
Практическая работа номер 4

Задание 5: 
	название и описание предметной области (осмысленное): Пользователи сайта
	SQL для создания таблиц: CREATE TABLE addresses (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)

CREATE TABLE metadata (
    metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    userAgent TEXT,
    hexcolor TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phoneNumber TEXT NOT NULL,
    email TEXT NOT NULL
)
	файлы исходных данных (можно обрезать до такого размера, чтобы влезли в GitHub): Приложенны в папке
	скрипт для инициализации базы данных (создание таблиц): В задании
	скрипт для загрузки данных из файлов в базу данных: В задании
	файл базы данных: В задании
	скрипт с выполнением запросов к базе данных: В задании
