import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_problem_statement_pdf():
    pdf_filename = "Student_Lab_Problem_Statement.pdf"
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor('#1E3A8A') # Deep Blue
    secondary_color = colors.HexColor('#0F172A') # Dark Slate
    accent_color = colors.HexColor('#2563EB') # Bright Royal Blue
    bg_light = colors.HexColor('#F8FAFC')
    border_color = colors.HexColor('#E2E8F0')
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1, # Center
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=secondary_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    code_inline_style = ParagraphStyle(
        'CodeInline',
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderPadding=3
    )

    story = []

    # Header Banner
    story.append(Paragraph("CLOUD COMPUTING & DEVOPS PRACTICAL EXAM", title_style))
    story.append(Paragraph("Lab Assignment: Multi-Tier Flask + MySQL Web Application Deployment", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=10))

    # Meta Info Table (Time, Marks, Tech Stack)
    meta_data = [
        [
            Paragraph("<b>Subject:</b> Cloud Application Deployment", body_style),
            Paragraph("<b>Time Allowed:</b> 2 Hours (120 Mins)", body_style),
            Paragraph("<b>Total Marks:</b> 100 Marks", body_style)
        ],
        [
            Paragraph("<b>Target Stack:</b> Python (Flask), PyMySQL, MySQL Server", body_style),
            Paragraph("<b>Deployment Target:</b> AWS EC2 / Azure VM / GCP / Local Host", body_style),
            Paragraph("<b>Evaluation Mode:</b> Practical Demonstration", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 170, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Objective & Problem Statement
    story.append(Paragraph("1. Objective & Scenario", heading2_style))
    story.append(Paragraph(
        "<b>Scenario:</b> You are working as a Cloud DevOps Engineer. A team has delivered a Flask web application that requires database connection pooling with MySQL. Your objective is to set up the MySQL relational database, configure environment variables, secure database credentials, and successfully deploy the web application so that users can register, login, reset passwords, and administrators can monitor user registrations.",
        body_style
    ))

    # Section 2: Detailed Tasks & Marks Allocation
    story.append(Paragraph("2. Tasks & Functional Requirements", heading2_style))

    tasks = [
        ("Task 1: MySQL Database Initialization (20 Marks)", [
            "Install and start MySQL Server on your deployment server.",
            "Create a database named <code>cloud_test_db</code>.",
            "Create a table named <code>users</code> with columns: <code>id</code> (Auto PK), <code>username</code> (UNIQUE), <code>email</code> (UNIQUE), <code>password_hash</code>, <code>role</code> ('user'/'admin'), and <code>created_at</code>.",
            "Insert a default administrator account (Username: <code>admin</code>, Password: <code>admin123</code> hashed)."
        ]),
        ("Task 2: Flask App & Environment Configuration (20 Marks)", [
            "Set up a Python Virtual Environment (<code>venv</code>) and install packages from <code>requirements.txt</code>.",
            "Configure <code>.env</code> file with valid MySQL connection parameters (<code>MYSQL_HOST</code>, <code>MYSQL_USER</code>, <code>MYSQL_PASSWORD</code>, <code>MYSQL_DB</code>).",
            "Ensure the app successfully establishes a database connection without hardcoding secret keys."
        ]),
        ("Task 3: User Authentication & Protected Dashboard (20 Marks)", [
            "<b>User Registration:</b> Allow new users to sign up. Store passwords securely using password hashing.",
            "<b>User Login:</b> Authenticate user credentials and create session cookies.",
            "<b>User Dashboard:</b> Restrict access to authenticated users only; display account profile details.",
            "<b>Password Reset:</b> Allow users to reset their passwords using their username or email."
        ]),
        ("Task 4: Administrator Management Portal (20 Marks)", [
            "Provide a dedicated Admin Login interface (<code>/admin/login</code>).",
            "Verify that only users with <code>role='admin'</code> can access the Admin Dashboard.",
            "Display live metrics: Total Registered Student Users and Total Administrator Accounts.",
            "Render a data table listing all registered users with their username, email, role, and registration date."
        ]),
        ("Task 5: Cloud Deployment & Security Configuration (20 Marks)", [
            "Run the application on host <code>0.0.0.0</code> and port <code>5000</code>.",
            "Configure inbound firewall rules (AWS Security Group / Azure NSG / ufw) to allow port 5000 traffic.",
            "Demonstrate a working live web application accessible via IP address or Domain."
        ])
    ]

    for title, steps in tasks:
        story.append(Paragraph(f"<b>{title}</b>", body_style))
        for step in steps:
            story.append(Paragraph(f"• {step}", bullet_style))
        story.append(Spacer(1, 4))

    # Section 3: Evaluation Rubric Table
    story.append(Paragraph("3. Evaluation Rubric & Marking Scheme", heading2_style))
    
    rubric_data = [
        ["Criteria", "Description", "Max Marks"],
        ["Database Setup", "Correct schema, constraints, and default admin seed query execution", "20 Marks"],
        ["App Configuration", "Environment variables set up in .env, packages installed cleanly", "20 Marks"],
        ["User Features", "Registration, Login, Password Reset, and Dashboard working properly", "20 Marks"],
        ["Admin Features", "Admin authentication, count metrics, and user table working properly", "20 Marks"],
        ["Cloud Deployment", "Application live and accessible over server Public IP / URL", "20 Marks"],
        ["Total Score", "Practical Demonstration & Code Review", "100 Marks"]
    ]

    rubric_table = Table(rubric_data, colWidths=[130, 310, 100])
    rubric_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-2), bg_light),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E2E8F0')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), secondary_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(rubric_table)
    story.append(Spacer(1, 10))

    # Section 4: Submission Deliverables
    story.append(Paragraph("4. Student Submission Deliverables", heading2_style))
    story.append(Paragraph("Each student must present the following during practical evaluation:", body_style))
    story.append(Paragraph("1. Live Demonstration URL: <code>http://&lt;your-server-ip&gt;:5000</code>", bullet_style))
    story.append(Paragraph("2. Admin Credentials Demonstration using <code>admin</code> account.", bullet_style))
    story.append(Paragraph("3. MySQL CLI Output showing <code>SELECT * FROM users;</code> with at least 2 registered student users.", bullet_style))

    # Build Document
    doc.build(story)
    print(f"Problem Statement PDF generated at: {pdf_path}")

if __name__ == '__main__':
    generate_problem_statement_pdf()
