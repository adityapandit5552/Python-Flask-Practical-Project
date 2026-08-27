import os
import sys
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    """Establishes a MySQL database connection using PyMySQL."""
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except pymysql.MySQLError as e:
        app.logger.error(f"Database Connection Error: {e}")
        return None

# Helper decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in as Administrator.', 'warning')
            return redirect(url_for('admin_login'))
        if session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    db_status = "Connected" if get_db_connection() else "Disconnected (Check .env configuration)"
    return render_template('index.html', db_status=db_status)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please ensure MySQL is running.', 'danger')
            return render_template('register.html')

        try:
            with conn.cursor() as cursor:
                # Check existing user
                cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash('Username or Email already registered. Please login.', 'warning')
                    return redirect(url_for('login'))

                # Hash password and insert user
                hashed_pw = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                    (username, email, hashed_pw, 'user')
                )
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
        except pymysql.MySQLError as e:
            flash(f'An error occurred during registration: {e}', 'danger')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please check your MySQL server.', 'danger')
            return render_template('login.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s OR email = %s",
                    (username_or_email, username_or_email)
                )
                user = cursor.fetchone()

                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['email'] = user['email']
                    session['role'] = user['role']

                    flash(f'Welcome back, {user["username"]}!', 'success')
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username/email or password.', 'danger')
        except pymysql.MySQLError as e:
            flash(f'Database error: {e}', 'danger')
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not identifier or not new_password:
            flash('Please fill in all fields.', 'danger')
            return render_template('reset_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('reset_password.html')

        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('reset_password.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (identifier, identifier))
                user = cursor.fetchone()

                if not user:
                    flash('Account not found with provided Username or Email.', 'danger')
                    return render_template('reset_password.html')

                hashed_pw = generate_password_hash(new_password)
                cursor.execute(
                    "UPDATE users SET password_hash = %s WHERE id = %s",
                    (hashed_pw, user['id'])
                )
                flash('Password updated successfully! Please log in with your new password.', 'success')
                return redirect(url_for('login'))
        except pymysql.MySQLError as e:
            flash(f'Error resetting password: {e}', 'danger')
        finally:
            conn.close()

    return render_template('reset_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    user_info = None
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (session['user_id'],))
                user_info = cursor.fetchone()
        finally:
            conn.close()
    return render_template('dashboard.html', user=user_info)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('admin_login.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
                user = cursor.fetchone()

                if user and user['role'] == 'admin' and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['email'] = user['email']
                    session['role'] = user['role']

                    flash('Authenticated successfully as Admin.', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid admin credentials or account is not an administrator.', 'danger')
        except pymysql.MySQLError as e:
            flash(f'Database error: {e}', 'danger')
        finally:
            conn.close()

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    if not conn:
        flash('Database error while loading administrator panel.', 'danger')
        return render_template('admin_dashboard.html', total_users=0, total_admins=0, users=[])

    try:
        with conn.cursor() as cursor:
            # Count total registered users
            cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role = 'user'")
            total_users = cursor.fetchone()['total']

            # Count total admin accounts
            cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role = 'admin'")
            total_admins = cursor.fetchone()['total']

            # Fetch list of all registered users
            cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
            all_users = cursor.fetchall()

        return render_template(
            'admin_dashboard.html',
            total_users=total_users,
            total_admins=total_admins,
            users=all_users
        )
    except pymysql.MySQLError as e:
        flash(f'Error fetching admin statistics: {e}', 'danger')
        return render_template('admin_dashboard.html', total_users=0, total_admins=0, users=[])
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
