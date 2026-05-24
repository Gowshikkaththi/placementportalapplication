# Placement Portal Application — MAD1

A full-stack college placement portal built with **Flask**, **SQLAlchemy**, and **JWT authentication**. It manages the complete placement lifecycle — from student and company registration, through admin approvals, to placement drive applications and status tracking — with a role-based access system for three user types: Admin, Company, and Student.

Swagger UI is available at `http://localhost:5000/apidocs` for interactive API exploration.

---

## Table of Contents

1. [Features](#1-features)
2. [Project Structure](#2-project-structure)
3. [Architecture Overview](#3-architecture-overview)
4. [Database Models](#4-database-models)
5. [Authentication & Authorization](#5-authentication--authorization)
6. [API Endpoints](#6-api-endpoints)
7. [Role Workflows](#7-role-workflows)
8. [Setup & Running Locally](#8-setup--running-locally)
9. [Environment & Configuration](#9-environment--configuration)
10. [Tech Stack](#10-tech-stack)

---

## 1. Features

**Admin**
- View and approve/reject pending student registrations
- View and approve/reject company registrations
- Review and approve/reject placement drives submitted by companies
- View all applications and all placement drives

**Company**
- Register and await admin approval
- Create placement drives (job title, description, eligibility, CGPA cutoff, deadline, salary, location)
- View all drives posted by the company
- View applications received for each drive
- Update application status (shortlisted, selected, rejected)
- View student profiles

**Student**
- Register with academic details (CGPA, backlogs, department, batch year, skills)
- View all approved placement drives they haven't applied to yet
- Apply for drives with optional notes
- Track application status across all applied drives
- Update their own profile (skills, LinkedIn, GitHub, LeetCode/HackerRank ratings, etc.)

---

## 2. Project Structure

```
placementportalapplicationmad1/
│
├── main.py                        # App entry point — Flask app, blueprints, login/logout routes
│
├── api_routes/
│   ├── admin_endpoints.py         # Admin blueprint — approval routes + dashboard
│   ├── company_endpoints.py       # Company blueprint — drives, applications, profile
│   ├── registration_endpoints.py  # Registration blueprint — student & company signup
│   └── student_endpoints.py       # Student blueprint — drives, applications, profile
│
├── controller_impl/
│   ├── admin_impl.py              # Business logic for admin operations
│   ├── company_impl.py            # Business logic for company operations
│   ├── registation_impl.py        # Registration logic for students and companies
│   └── student_impl.py            # Business logic for student operations
│
├── models/
│   ├── __init__.py                # Imports all models; exposes create_db_and_tables()
│   ├── users.py                   # User model (base auth entity)
│   ├── roles.py                   # Role model (ADMIN, STUDENT, COMPANY)
│   ├── user_role.py               # Many-to-many join table: users <-> roles
│   ├── student.py                 # Student profile model
│   ├── company.py                 # Company model
│   ├── company_user.py            # Maps a user account to a company
│   ├── placement_drive.py         # Placement drive model
│   └── application.py             # Application model (student <-> drive)
│
├── config/
│   ├── constants.py               # Role name constants
│   ├── db_creation.py             # SQLAlchemy engine + session factory + Base
│   ├── decorators.py              # @role_required JWT decorator
│   ├── admin_creation.py          # Seeds the default admin user on startup
│   └── swagger.py                 # Swagger template + inline API docs
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── company_dashboard.html
│   └── student_dashboard.html
│
├── static/
│   └── css/style.css
│
└── requirements.txt
```

---

## 3. Architecture Overview

The app follows a layered architecture:

```
Browser / API Client
        |
        v
  Flask Routes (api_routes/)          <- HTTP layer, request parsing, response formatting
        |
        v
  Controller Impl (controller_impl/)  <- Business logic, DB queries, validation
        |
        v
  SQLAlchemy Models (models/)         <- ORM entities mapped to SQLite tables
        |
        v
  SQLite Database (placement23f1002989.db)
```

**Blueprints** keep routes modular. Each actor (admin, company, student, registration) lives in its own blueprint registered in `main.py` with a distinct URL prefix.

**Separation of concerns:** Route files handle HTTP concerns only — parsing JSON, returning status codes, redirecting. All database work and business logic lives in `controller_impl/`.

---

## 4. Database Models

### User
Central auth entity. Every person in the system — admin, student, or company HR — has a `User` row.

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `username` | String | Unique |
| `email` | String | Unique |
| `password` | String | Hashed via Werkzeug |
| `active` | Boolean | |
| `approved_status` | String | `"Pending"` or `"Approved"` |
| `created_at` | DateTime | |
| `approved_at` / `approved_by` | DateTime / Integer | Audit trail for approvals |

### Role
Three roles exist: `ADMIN`, `STUDENT`, `COMPANY`. Linked to `User` via the `roles_users` join table (many-to-many).

### Student
Extended profile for student users. Linked 1-to-1 with `User`.

Key fields: `roll_number`, `department`, `degree`, `batch_year`, `cgpa`, `tenth_percentage`, `twelfth_percentage`, `active_backlogs`, `total_backlogs`, `placement_status`, `skills`, `github_url`, `linkedin_url`, `leetcode_rating`, `hackerrank_rating`.

Indexes on `batch_year` and `placement_status` for efficient filtering.

### Company
Represents a hiring organisation. Approval status starts as `PENDING`.

Key fields: `company_name`, `website`, `industry`, `headquarters`, `description`, `approval_status` (enum: `PENDING / APPROVED / REJECTED`).

### CompanyUser
Join table mapping a `User` account to a `Company`. One user represents one company.

### PlacementDrive
A job opening posted by a company.

Key fields: `job_title`, `job_description`, `eligibility_criteria`, `minimum_CGPA`, `application_deadline`, `location`, `salary_package`, `status` (enum: `PENDING / APPROVED / CLOSED / REJECTED`).

New drives start as `PENDING` and must be admin-approved before students can see them.

### Application
Tracks a student's application to a placement drive.

Key fields: `student_id`, `drive_id`, `application_date`, `status` (enum: `APPLIED / SHORTLISTED / SELECTED / REJECTED`), `notes`.

---

## 5. Authentication & Authorization

### Login Flow

`POST /login` accepts `username` + `password` via form. On success it:
1. Verifies the password hash using `werkzeug.security.check_password_hash`
2. Checks `approved_status == "Approved"` (blocks pending users)
3. Creates a JWT via `flask_jwt_extended` containing the user's roles
4. Stores the token in both Flask `session` (for template rendering) and an `httponly` cookie
5. Redirects to the appropriate dashboard based on role

### Logout

`GET /logout` clears the session, expires the JWT cookie, and redirects to login.

### Role-Based Access Control

All API endpoints (except registration and login) are protected by the `@role_required` decorator defined in `config/decorators.py`:

```python
@role_required("ADMIN")
def approve_user(user_id):
    ...
```

The decorator wraps `@jwt_required()` from `flask_jwt_extended`, reads the `roles` claim from the JWT, and returns a redirect to login if the required role is absent.

JWT tokens are accepted from both cookies and headers (`JWT_TOKEN_LOCATION = ['cookies', 'headers']`), allowing both browser-based and direct API access.

---

## 6. API Endpoints

### Registration — prefix `/register`

| Method | Path | Description |
|---|---|---|
| GET | `/register/` | Render registration form |
| POST | `/register/register_student` | Register a new student |
| POST | `/register/register_company` | Register a new company HR user |

### Auth — root

| Method | Path | Description |
|---|---|---|
| GET/POST | `/login` | Login and receive JWT |
| GET | `/logout` | Clear session and JWT cookie |

### Admin — prefix `/admin`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/admin/admin/dashboard` | ADMIN | Render admin dashboard |
| GET | `/admin/unapproved-users` | ADMIN | List users pending approval |
| PUT | `/admin/users/<id>/approval` | ADMIN | Approve or reject a user |
| GET | `/admin/pending-companies` | ADMIN | List companies pending approval |
| PUT | `/admin/companies/<id>/approval` | ADMIN | Approve or reject a company |
| GET | `/admin/placement-drives` | ADMIN | List all placement drives |
| GET | `/admin/placement-drives/pending` | ADMIN | List pending placement drives |
| PUT | `/admin/placement-drives/<id>/status` | ADMIN | Approve/reject/close a drive |
| GET | `/admin/applications` | ADMIN | List all applications |
| GET | `/admin/admin/<id>` | ADMIN | Get admin user details |
| GET | `/admin/users/<id>/approve/<status>` | ADMIN | Quick-approve user (dashboard shortcut) |
| GET | `/admin/companies/<id>/approve/<status>` | ADMIN | Quick-approve company (dashboard shortcut) |
| GET | `/admin/drives/<id>/approve/<status>` | ADMIN | Quick-approve drive (dashboard shortcut) |

### Company — prefix `/company`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/company/dashboard/` | — | Render company dashboard |
| POST | `/company/placement-drives` | COMPANY | Create a new placement drive |
| GET | `/company/<id>/placement-drives` | COMPANY | List all drives for a company |
| GET | `/company/placement-drives/<id>/applications` | COMPANY | View applications for a drive |
| PUT | `/company/applications/<id>/status` | COMPANY | Update application status |
| GET | `/company/students/<id>` | COMPANY | View a student's profile |
| GET | `/company/<id>` | COMPANY | Get company details |

### Student — prefix `/student`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/student/dashboard` | — | Render student dashboard |
| GET | `/student/drives/<student_id>` | STUDENT | List approved drives not yet applied to |
| POST | `/student/apply` | STUDENT | Apply for a placement drive |
| PUT | `/student/<student_id>` | STUDENT | Update student profile |
| GET | `/student/<student_id>/applications` | STUDENT | View own application history |
| GET | `/student/details/<student_id>` | STUDENT | Get full student profile |

---

## 7. Role Workflows

### Student Registration & Application

```
Student registers  -->  approved_status = "Approved" (automatic)
        |
        v
Logs in  -->  JWT issued with role STUDENT
        |
        v
Views approved placement drives (drives not yet applied to)
        |
        v
Applies for a drive  -->  Application created with status APPLIED
        |
        v
Company updates status  -->  SHORTLISTED / SELECTED / REJECTED
        |
        v
Student tracks status via GET /student/<id>/applications
```

### Company Registration & Drive Posting

```
Company HR registers  -->  approved_status = "Pending"
        |
        v
Admin approves user  -->  approved_status = "Approved"
Admin approves company  -->  Company.approval_status = APPROVED
        |
        v
Company logs in  -->  JWT issued with role COMPANY
        |
        v
Creates a placement drive  -->  Drive.status = PENDING
        |
        v
Admin approves drive  -->  Drive.status = APPROVED
        |
        v
Students can now see and apply to the drive
```

### Admin Approval Flow

```
Admin logs in  (seeded automatically on startup via create_admin())
        |
        v
Dashboard shows: pending users / pending companies / pending drives
        |
        v
Approves or rejects each via dashboard links or REST API
```

---

## 8. Setup & Running Locally

### Prerequisites

- Python 3.10+

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd placementportalapplicationmad1

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

The app starts at `http://localhost:5000`.

On first run, `create_db_and_tables()` creates the SQLite database file (`placement23f1002989.db`) and all tables automatically. `create_admin()` seeds the default admin account.

### Swagger UI

Open `http://localhost:5000/apidocs` to explore and test all endpoints interactively.

### Quick Test Flow

1. Open `http://localhost:5000/login` — log in with the seeded admin credentials.
2. Open `http://localhost:5000/register` — register a student or a company.
3. As admin, approve the new user from the dashboard.
4. Log in as the student and browse available drives.

---

## 9. Environment & Configuration

All configuration lives in `main.py` and `config/db_creation.py`. Update these values before deploying:

| Setting | Current Value | Production Recommendation |
|---|---|---|
| `JWT_SECRET_KEY` | `"#MAD!1@PROJECT*^$"` | Use a long random secret stored in an environment variable |
| `JWT_COOKIE_SECURE` | `False` | Set `True` (HTTPS only) |
| `JWT_COOKIE_CSRF_PROTECT` | `False` | Set `True` |
| `app.secret_key` | `os.urandom(24)` | Use a fixed secret so sessions survive restarts |
| Database URL | `sqlite:///placement23f1002989.db` | Replace with PostgreSQL/MySQL for production |
| `debug=True` | Enabled | Set `False` in production |

---

## 10. Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask |
| ORM | SQLAlchemy |
| Database | SQLite (file-based, auto-created) |
| Authentication | Flask-JWT-Extended (JWT in cookie + header) |
| Password Hashing | Werkzeug Security |
| API Documentation | Flasgger (Swagger UI at `/apidocs`) |
| Session Management | Flask session |
| Role Mixin | Flask-Security RoleMixin / UserMixin |
| Frontend | Jinja2 templates + plain CSS |
