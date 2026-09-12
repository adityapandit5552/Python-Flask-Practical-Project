# Flask + MySQL Cloud Deployment Lab

A practical cloud deployment project based on a Python Flask web application integrated with a MySQL/MariaDB database. The project demonstrates deploying a database-driven web application on a cloud Linux environment and configuring application-to-database connectivity.

## Project Overview

This project was used as a practical cloud computing lab to understand the deployment and configuration of a Python Flask web application with a relational database.

The application was deployed on a cloud server and accessed through its public IP address. The application successfully connects to a MySQL/MariaDB database for storing and retrieving user information.

## Features

- User registration
- User login and logout
- Session-based authentication
- User dashboard
- Password reset functionality
- Administrator portal
- User management
- User statistics
- Role-based access
- MySQL/MariaDB database integration
- Responsive web interface
- Database connectivity monitoring

## Deployment and Configuration

- Deployed the Flask web application on a Linux-based cloud server.
- Configured the Python environment and required application dependencies.
- Configured MySQL/MariaDB database connectivity.
- Created and configured the application database and user table.
- Configured environment variables for database credentials.
- Verified application-to-database connectivity through the running application.
- Tested user registration, login, session management, and dashboard functionality.
- Accessed the deployed application through the server's public IP address.

## Database

The application uses MySQL/MariaDB as the relational database.

The database stores user information including:

- User ID
- Username
- Email
- Password Hash
- User Role
- Account Creation Date

Password information is stored using password hashing rather than plain-text passwords.

## Technologies Used

- **Programming Language:** Python
- **Framework:** Flask
- **Database:** MySQL / MariaDB
- **Database Connector:** PyMySQL
- **Operating System:** Linux
- **Cloud Platform:** AWS EC2
- **Version Control:** Git, GitHub
- **Frontend:** HTML, CSS
- **Environment Configuration:** Environment Variables

## Project Structure

```text
Python-Flask-Practical-Project/
│
├── app.py
├── config.py
├── schema.sql
├── requirements.txt
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   └── ...
│
├── screenshots/
│
└── README.md
```

## Application Screenshots

### Home Page

The application home page provides navigation to the login, registration, and administrator sections.

![Home Page](home.png)

### User Registration

The registration page allows new users to create an account with username, email, and password.

![User Registration](createaccount.png)

### User Login

Registered users can log in using their username or email and password.

![User Login](loginpage.png)

### User Dashboard

After successful authentication, users can access their dashboard and view their account information.

![User Dashboard](dashboard.png)

### Database Verification

The MariaDB database was verified using SQL commands, showing registered users and their stored account information.

![Database](Databases.png)

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/adityapandit5552/Python-Flask-Practical-Project.git
cd Python-Flask-Practical-Project
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create the MySQL/MariaDB database and configure the required database credentials using environment variables.

### 5. Run the Application

```bash
python3 app.py
```

The application can then be accessed through the configured server address and port.

## Learning Outcomes

This project provided practical experience with:

- Flask application deployment
- Linux server environment
- Cloud server deployment
- MySQL/MariaDB database configuration
- Application-to-database connectivity
- Environment variable configuration
- User authentication and sessions
- Git and GitHub
- Basic cloud application troubleshooting
