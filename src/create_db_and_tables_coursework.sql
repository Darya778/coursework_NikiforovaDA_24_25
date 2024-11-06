CREATE DATABASE db_info_users;

USE db_info_users;

-- Таблица сотрудников
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255),
    patronymic VARCHAR(255),
    position VARCHAR(255),
    department VARCHAR(255),
    card_id VARCHAR(20) UNIQUE NOT NULL,
    hire_date DATE,
    salary DECIMAL(10,2),
    phone VARCHAR(20),
    email VARCHAR(255)
);

-- Таблица квалификаций
CREATE TABLE qualifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    qualification VARCHAR(255),
    level VARCHAR(255),
    certificate_number VARCHAR(255),
    expiry_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Таблица отпусков
CREATE TABLE vacations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    start_date DATE,
    end_date DATE,
    type VARCHAR(255),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Таблица болезней
CREATE TABLE sick_leaves (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    start_date DATE,
    end_date DATE,
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Таблица задач
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    description TEXT,
    status VARCHAR(255),
    deadline DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

