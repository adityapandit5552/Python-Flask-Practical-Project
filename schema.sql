-- =========================================================
-- Database Schema for Flask + MySQL Student Deployment Test
-- =========================================================

-- 1. Create Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `cloud_test_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `cloud_test_db`;

-- 2. Create Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` ENUM('user', 'admin') DEFAULT 'user',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Seed Default Admin Account
-- Default Username: admin
-- Default Email: admin@cloudtest.com
-- Default Password: admin123 (hashed using Werkzeug)
-- Werkzeug hashed password for 'admin123'
INSERT INTO `users` (`username`, `email`, `password_hash`, `role`)
VALUES (
    'admin', 
    'admin@cloudtest.com', 
    'scrypt:32768:8:1$7nXZwQ3p6Yp7$24c883ed6df65ecf50a8b9eeb2db8fa0b555d4ee7e3fa4923e5904d9c791dd15e3474327299a9cfb0114ae39f7a77d54238eeb5ca5d1e2e4efcf291bfecf074d', 
    'admin'
)
ON DUPLICATE KEY UPDATE `username`=`username`;
