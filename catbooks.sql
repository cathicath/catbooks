CREATE DATABASE catbooks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE catbooks_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
);

-- Insert example users
INSERT INTO users (username, password) VALUES ('frodo', 'ring123');
INSERT INTO users (username, password) VALUES ('samwise', 'shire4ever');
INSERT INTO users (username, password) VALUES ('gimli', 'andmyaxe');


CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    author VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    review_text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    file_path VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    image VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);
