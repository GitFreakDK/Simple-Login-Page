CREATE SCHEMA user_db_management;

USE user_db_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE office_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(15) NOT NULL,
    office_name VARCHAR(100) DEFAULT NULL,
    payments FLOAT DEFAULT 0.0,
    total_work_hours INT DEFAULT 0,
    task_completion VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (phone) REFERENCES users(phone) ON DELETE CASCADE
);

SELECT * FROM users;

SELECT * FROM office_details;