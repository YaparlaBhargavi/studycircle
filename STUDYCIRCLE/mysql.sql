-- Step 1: Create Database
-- The application connects to this database.
CREATE DATABASE IF NOT EXISTS circle;
USE circle;

-- Step 2: Create users Table
-- This table stores user registration data, including hashed passwords.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Step 3: Create subjects Table
-- This table lists the subjects available in the application.
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Insert Sample Subjects
-- These are the initial subjects users can select from.
INSERT IGNORE INTO subjects (name) VALUES 
('Machine Learning'),
('Software Engineering'),
('Operating System'),
('Trinkering Lab'),
('Full Stack Development');

-- Step 4: Create progress_tracking Table
-- This table is used to track a user's progress on specific topics.
CREATE TABLE IF NOT EXISTS progress_tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    subject VARCHAR(100),
    topic_name VARCHAR(255),
    progress_status ENUM('Not Started', 'In Progress', 'Completed'),
    update_text TEXT,
    study_hours FLOAT DEFAULT 0,
    session_count INT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Step 5: Create the chat Table
-- This table stores all chat messages from users.
CREATE TABLE IF NOT EXISTS chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Step 6: Create the reminders Table
-- This table stores reminders scheduled by users.
CREATE TABLE IF NOT EXISTS reminders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
