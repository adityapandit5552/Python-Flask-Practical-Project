import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    pdf_filename = "MySQL_Database_Queries_Student_Lab.pdf"
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor('#4F46E5') # Indigo
    secondary_color = colors.HexColor('#1E293B') # Dark slate
    accent_color = colors.HexColor('#0EA5E9') # Cyan
    bg_code = colors.HexColor('#0F172A') # Dark code bg
    text_code = colors.HexColor('#38BDF8') # Light cyan code text
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    
    heading2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        fontName='Courier',
        fontSize=9,
        leading=13,
        textColor=text_code,
        backColor=bg_code,
        borderPadding=10,
        spaceBefore=6,
        spaceAfter=12
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("MySQL Database Queries & Setup Guide", title_style))
    story.append(Paragraph("Cloud Computing Student Deployment Lab | Flask + MySQL Project", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=15))

    # Section 1: Overview
    story.append(Paragraph("1. Overview & Setup Instructions", heading2_style))
    story.append(Paragraph(
        "This document contains the exact MySQL database schema, table creation queries, seed data, and verification statements required for students deploying the Flask + MySQL web application.",
        body_style
    ))

    # Section 2: Full SQL Script
    story.append(Paragraph("2. Complete MySQL Database Creation Script", heading2_style))
    story.append(Paragraph("Copy and execute the following SQL statements in MySQL Command Line Interface (CLI), MySQL Workbench, or phpMyAdmin:", body_style))

    sql_script = """-- =========================================================
-- Flask + MySQL Student Deployment Test - Database Setup
-- =========================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS `cloud_test_db` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

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

-- 3. Seed Initial Administrator User
-- Default Credentials: Username: admin | Password: admin123
INSERT INTO `users` (`username`, `email`, `password_hash`, `role`)
VALUES (
    'admin', 
    'admin@cloudtest.com', 
    'scrypt:32768:8:1$7nXZwQ3p6Yp7$24c883ed6df65ecf50a8b9eeb2db8fa0b555d4ee7e3fa4923e5904d9c791dd15e3474327299a9cfb0114ae39f7a77d54238eeb5ca5d1e2e4efcf291bfecf074d', 
    'admin'
)
ON DUPLICATE KEY UPDATE `username`=`username`;"""

    story.append(Preformatted(sql_script, code_style))

    # Section 3: Database Table Structure Details
    story.append(Paragraph("3. Table Schema Structure (`users`)", heading2_style))
    
    table_data = [
        ["Column Name", "Data Type", "Constraints", "Description"],
        ["id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique record identifier"],
        ["username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Student / User login name"],
        ["email", "VARCHAR(100)", "NOT NULL, UNIQUE", "User email address"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "Werkzeug secure password hash"],
        ["role", "ENUM('user','admin')", "DEFAULT 'user'", "Role authorization level"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Registration timestamp"]
    ]

    t = Table(table_data, colWidths=[90, 110, 150, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#1E293B')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Section 4: Useful Testing & Verification Queries
    story.append(Paragraph("4. Student Verification SQL Queries", heading2_style))
    story.append(Paragraph("Students can run these queries to test and verify database operations during lab evaluation:", body_style))

    queries_text = """-- Query 1: View all registered users
SELECT id, username, email, role, created_at FROM users;

-- Query 2: Count total registered users
SELECT COUNT(*) AS total_students FROM users WHERE role = 'user';

-- Query 3: Search user by username or email
SELECT * FROM users WHERE username = 'admin' OR email = 'admin@cloudtest.com';

-- Query 4: Reset password manually (if needed)
UPDATE users SET password_hash = '<new_hash>' WHERE username = 'student1';

-- Query 5: Delete test user account
DELETE FROM users WHERE username = 'test_user';"""

    story.append(Preformatted(queries_text, code_style))

    # Build Document
    doc.build(story)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    generate_pdf()
