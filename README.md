# Flask + MySQL Cloud Student Deployment Test

This repository contains a complete, lightweight, and modern Flask web application integrated with a MySQL database. It is designed as a practical lab exercise for cloud computing students to test deploying web applications and database integrations on cloud instances (e.g., AWS EC2, Azure VMs, GCP Compute, Heroku/Render).

---

## 📋 Features Included

1. **User Registration**: Register new accounts with secure password hashing (`Werkzeug`).
2. **User Login & Session Management**: Session-based login for users and admins.
3. **User Dashboard**: Protected dashboard displaying user account metrics.
4. **Password Reset**: Password update functionality by username/email.
5. **Admin Portal**: Admin login and dashboard displaying total user counts and a registered user directory table.
6. **Glassmorphism Dark Theme**: Fully responsive CSS styling with status badges and animations.

---

## 🗄️ MySQL Database Setup & SQL Queries

Give the following SQL queries / commands to your students or execute `schema.sql`:

### 1. Create Database and Table manually in MySQL CLI:

```sql
-- Step 1: Create the Database
CREATE DATABASE IF NOT EXISTS `cloud_test_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `cloud_test_db`;

-- Step 2: Create Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` ENUM('user', 'admin') DEFAULT 'user',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 3: Insert Default Seed Admin User (Password: admin123)
INSERT INTO `users` (`username`, `email`, `password_hash`, `role`)
VALUES (
    'admin', 
    'admin@cloudtest.com', 
    'scrypt:32768:8:1$7nXZwQ3p6Yp7$24c883ed6df65ecf50a8b9eeb2db8fa0b555d4ee7e3fa4923e5904d9c791dd15e3474327299a9cfb0114ae39f7a77d54238eeb5ca5d1e2e4efcf291bfecf074d', 
    'admin'
)
ON DUPLICATE KEY UPDATE `username`=`username`;
```

### Or Import the `schema.sql` file directly:
```bash
mysql -u root -p < schema.sql
```

---

## 🚀 Quickstart Instructions for Students

### 1. Clone & Navigate to Project Directory
```bash
git clone <repository_url>
cd flask_with_mysql
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / MacOS
cp .env.example .env
```

Open `.env` and set your configuration:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=cloud_test_db

SECRET_KEY=super_secret_cloud_test_key
PORT=5000
```

### 5. Run the Application
```bash
python app.py
```

Open your browser and visit: `http://localhost:5000` (or `http://<your-cloud-instance-ip>:5000`)

---

## 🔐 Default Admin Test Credentials

- **Username**: `admin`
- **Email**: `admin@cloudtest.com`
- **Password**: `admin123`
- **Admin Portal Link**: `http://localhost:5000/admin/login`

---

## 📂 Project Structure

```
flask_with_mysql/
├── app.py                  # Core Flask routes & PyMySQL logic
├── config.py               # Environment configuration loader
├── schema.sql              # Database setup & admin seed queries
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment setup template
├── .env                    # Local environment variables (DB host/user/pass)
├── README.md               # Student deployment guide & instructions
├── templates/
│   ├── base.html           # Base layout with navigation & toast alerts
│   ├── index.html          # Landing page with DB connection status
│   ├── register.html       # Student registration page
│   ├── login.html          # User login page
│   ├── reset_password.html # Password reset page
│   ├── dashboard.html      # User dashboard
│   ├── admin_login.html    # Administrator login portal
│   └── admin_dashboard.html# Admin panel showing total user counts & directory
└── static/
    └── css/
        └── style.css       # Glassmorphism dark mode design system
```
