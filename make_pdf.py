import os

def create_pure_python_pdf(pdf_path):
    # PDF Header
    pdf_bytes = bytearray()
    pdf_bytes.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    objects = []

    # Obj 1: Catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

    # Obj 2: Pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")

    # Obj 4: Font Helvetica
    objects.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")

    # Obj 5: Font Helvetica Normal
    objects.append(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # Obj 6: Font Courier
    objects.append(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n")

    # Build Content Stream
    stream = []
    
    # Title Header
    stream.append("0.31 0.27 0.90 rg") # Indigo color accent
    stream.append("50 740 512 4 re f") # Top accent bar
    
    stream.append("BT")
    stream.append("/F1 20 Tf")
    stream.append("0.06 0.09 0.16 rg")
    stream.append("50 710 Td")
    stream.append("(MySQL Database Queries & Setup Guide) Tj")
    stream.append("ET")

    stream.append("BT")
    stream.append("/F2 11 Tf")
    stream.append("0.39 0.45 0.55 rg")
    stream.append("50 690 Td")
    stream.append("(Cloud Computing Student Deployment Lab | Flask + MySQL) Tj")
    stream.append("ET")

    # Section 1 Header
    stream.append("BT")
    stream.append("/F1 13 Tf")
    stream.append("0.06 0.09 0.16 rg")
    stream.append("50 660 Td")
    stream.append("(1. Overview & Instructions) Tj")
    stream.append("ET")

    stream.append("BT")
    stream.append("/F2 9.5 Tf")
    stream.append("0.20 0.25 0.33 rg")
    stream.append("50 642 Td")
    stream.append("(This document contains all MySQL table queries and setup commands for students.) Tj")
    stream.append("ET")

    # Section 2 Header
    stream.append("BT")
    stream.append("/F1 13 Tf")
    stream.append("0.06 0.09 0.16 rg")
    stream.append("50 615 Td")
    stream.append("(2. MySQL Database Setup Script (schema.sql)) Tj")
    stream.append("ET")

    # Dark Code Box Background
    stream.append("0.06 0.09 0.16 rg")
    stream.append("45 285 522 315 re f")

    # SQL Commands inside Code Box
    sql_lines = [
        "-- Step 1: Create Database",
        "CREATE DATABASE IF NOT EXISTS `cloud_test_db`",
        "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "",
        "USE `cloud_test_db`;",
        "",
        "-- Step 2: Create Users Table",
        "CREATE TABLE IF NOT EXISTS `users` (",
        "    `id` INT AUTO_INCREMENT PRIMARY KEY,",
        "    `username` VARCHAR(50) NOT NULL UNIQUE,",
        "    `email` VARCHAR(100) NOT NULL UNIQUE,",
        "    `password_hash` VARCHAR(255) NOT NULL,",
        "    `role` ENUM('user', 'admin') DEFAULT 'user',",
        "    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;",
        "",
        "-- Step 3: Seed Default Admin Account (Password: admin123)",
        "INSERT INTO `users` (`username`, `email`, `password_hash`, `role`)",
        "VALUES (",
        "    'admin',",
        "    'admin@cloudtest.com',",
        "    'scrypt:32768:8:1$7nXZwQ3p6Yp7$24c883ed6df65ecf50a8b...',",
        "    'admin'",
        ") ON DUPLICATE KEY UPDATE `username`=`username`;"
    ]

    y_code = 582
    for line in sql_lines:
        line_escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream.append("BT")
        stream.append("/F3 8.5 Tf")
        if line.startswith("--"):
            stream.append("0.58 0.64 0.72 rg") # Comment grey
        elif line.startswith("CREATE") or line.startswith("USE") or line.startswith("INSERT") or line.startswith("VALUES"):
            stream.append("0.22 0.74 0.97 rg") # Cyan keyword
        else:
            stream.append("0.97 0.98 0.99 rg") # White text
        stream.append(f"55 {y_code} Td")
        stream.append(f"({line_escaped}) Tj")
        stream.append("ET")
        y_code -= 12

    # Section 3: Verification Queries
    stream.append("BT")
    stream.append("/F1 13 Tf")
    stream.append("0.06 0.09 0.16 rg")
    stream.append("50 255 Td")
    stream.append("(3. Student Lab Verification Queries) Tj")
    stream.append("ET")

    verif_queries = [
        "1. View all users:       SELECT id, username, email, role FROM users;",
        "2. Count total users:     SELECT COUNT(*) AS student_count FROM users WHERE role='user';",
        "3. Admin login query:     SELECT * FROM users WHERE username='admin' AND role='admin';",
        "4. Reset password query:  UPDATE users SET password_hash='<hash>' WHERE id=1;"
    ]

    y_ver = 235
    for q in verif_queries:
        q_escaped = q.replace('(', '\\(').replace(')', '\\)')
        stream.append("BT")
        stream.append("/F2 9 Tf")
        stream.append("0.20 0.25 0.33 rg")
        stream.append(f"50 {y_ver} Td")
        stream.append(f"({q_escaped}) Tj")
        stream.append("ET")
        y_ver -= 14

    # Footer
    stream.append("0.31 0.27 0.90 rg")
    stream.append("50 45 512 1 re f")
    stream.append("BT")
    stream.append("/F2 8.5 Tf")
    stream.append("0.58 0.64 0.72 rg")
    stream.append("50 30 Td")
    stream.append("(Cloud Deployment Lab Guide - Generated for Student Evaluation) Tj")
    stream.append("ET")

    stream_content = "\n".join(stream).encode('latin1')
    stream_len = len(stream_content)

    # Obj 7: Content Stream
    objects.append(f"7 0 obj\n<< /Length {stream_len} >>\nstream\n".encode('latin1') + stream_content + b"\nendstream\nendobj\n")

    # Obj 3: Page Definition (linking fonts F1, F2, F3 and content obj 7)
    objects.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> /Contents 7 0 R >>\nendobj\n")

    # Compile offsets and write PDF
    offsets = []
    current_pos = len(pdf_bytes)

    body_bytes = bytearray()
    for obj in objects:
        offsets.append(current_pos)
        body_bytes.extend(obj)
        current_pos += len(obj)

    xref_pos = current_pos
    xref = f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode('latin1')
    for off in offsets:
        xref += f"{off:010d} 00000 n \n".encode('latin1')

    trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode('latin1')

    full_pdf_bytes = pdf_bytes + body_bytes + xref + trailer

    with open(pdf_path, 'wb') as f:
        f.write(full_pdf_bytes)

    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    pdf_out = os.path.join(os.getcwd(), 'MySQL_Database_Queries_Student_Lab.pdf')
    create_pure_python_pdf(pdf_out)
