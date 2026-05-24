swagger_template = {
    "swagger": "2.0",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

login_doc = {
    "tags": ["Authentication"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["username", "password"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "JWT token generated"
        },
        "401": {
            "description": "Invalid credentials"
        }
    }
}

view_unapproved_users_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View all unapproved users",
    "description": "Returns a list of users whose approval status is pending",
    "responses": {
        200: {
            "description": "List of unapproved users",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "approved_status": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

update_user_approval_swagger = {
    "tags": ["Admin"],
    "summary": "Approve or reject a user",
    "security": [
        {"Bearer": []}
    ],
    "description": "Admin updates the approval status of a user",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the user to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "Approved"
                    },
                    "admin_id": {
                        "type": "integer",
                        "example": 1
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "User approval updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "approved_status": {"type": "string"}
                }
            }
        },
        404: {
            "description": "User not found"
        }
    }
}

get_pending_companies_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View pending companies",
    "description": "Returns all companies waiting for admin approval",
    "responses": {
        200: {
            "description": "List of pending companies",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "company_name": {"type": "string"},
                        "hr_contact_name": {"type": "string"},
                        "hr_contact_email": {"type": "string"},
                        "hr_contact_phone": {"type": "string"},
                        "website": {"type": "string"},
                        "approval_status": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

update_company_approval_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Approve or reject a company",
    "description": "Admin updates the approval status of a company",
    "parameters": [
        {
            "name": "company_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Company ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "APPROVED"
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Company approval updated",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "company_name": {"type": "string"},
                    "approval_status": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Company not found"
        }
    }
}

get_all_applications_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View all applications",
    "description": "Fetch all student applications for placement drives",
    "responses": {
        200: {
            "description": "List of applications",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "student_id": {"type": "integer"},
                        "drive_id": {"type": "integer"},
                        "application_date": {"type": "string"},
                        "status": {"type": "string"},
                        "notes": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

get_all_placement_drives_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View all placement drives",
    "description": "Fetch all placement drives created by companies",
    "responses": {
        200: {
            "description": "List of placement drives",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "company_id": {"type": "integer"},
                        "job_title": {"type": "string"},
                        "job_description": {"type": "string"},
                        "eligibility_criteria": {"type": "string"},
                        "minimum_CGPA": {"type": "string"},
                        "application_deadline": {"type": "string"},
                        "status": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_package": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

get_pending_placement_drives_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View pending placement drives",
    "description": "Returns all placement drives waiting for admin approval",
    "responses": {
        200: {
            "description": "List of pending placement drives",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "company_id": {"type": "integer"},
                        "job_title": {"type": "string"},
                        "job_description": {"type": "string"},
                        "eligibility_criteria": {"type": "string"},
                        "minimum_CGPA": {"type": "string"},
                        "application_deadline": {"type": "string"},
                        "status": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_package": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

update_drive_status_swagger = {
    "tags": ["Admin"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Update placement drive status",
    "description": "Admin approves or rejects a placement drive",
    "parameters": [
        {
            "name": "drive_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Placement drive ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "APPROVED"
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Placement drive status updated",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "company_id": {"type": "integer"},
                    "job_title": {"type": "string"},
                    "status": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Placement drive not found"
        }
    }
}

create_placement_drive_swagger = {
    "tags": ["Company"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Create placement drive",
    "description": "Company creates a new placement drive",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["company_id", "job_title"],
                "properties": {
                    "company_id": {
                        "type": "integer",
                        "example": 2
                    },
                    "job_title": {
                        "type": "string",
                        "example": "Backend Developer"
                    },
                    "job_description": {
                        "type": "string",
                        "example": "Spring Boot developer role"
                    },
                    "eligibility_criteria": {
                        "type": "string",
                        "example": "B.Tech CSE / MCA"
                    },
                    "minimum_CGPA": {
                        "type": "string",
                        "example": "7.0"
                    },
                    "application_deadline": {
                        "type": "string",
                        "example": "2026-04-30T23:59:00"
                    },
                    "location": {
                        "type": "string",
                        "example": "Bangalore"
                    },
                    "salary_package": {
                        "type": "string",
                        "example": "10 LPA"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Placement drive created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "company_id": {"type": "integer"},
                    "job_title": {"type": "string"},
                    "status": {"type": "string"}
                }
            }
        }
    }
}


get_drives_by_company_swagger = {
    "tags": ["Company"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View company placement drives",
    "description": "Returns all placement drives created by a specific company",
    "parameters": [
        {
            "name": "company_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Company ID"
        }
    ],
    "responses": {
        200: {
            "description": "List of placement drives created by the company",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "job_title": {"type": "string"},
                        "job_description": {"type": "string"},
                        "eligibility_criteria": {"type": "string"},
                        "minimum_CGPA": {"type": "string"},
                        "application_deadline": {"type": "string"},
                        "status": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_package": {"type": "string"}
                    }
                }
            }
        }
    }
}

get_applications_by_drive_swagger = {
    "tags": ["Company"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "View applications for a placement drive",
    "description": "Returns all student applications for a specific placement drive",
    "parameters": [
        {
            "name": "drive_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Placement drive ID"
        }
    ],
    "responses": {
        200: {
            "description": "List of applications for the drive",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "student_id": {"type": "integer"},
                        "drive_id": {"type": "integer"},
                        "application_date": {"type": "string"},
                        "status": {"type": "string"},
                        "notes": {"type": "string"}
                    }
                }
            }
        },
        404: {
            "description": "Drive not found"
        }
    }
}


get_student_by_id_swagger = {
    "tags": ["Company"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Get student details",
    "description": "Fetch details of a student by student ID",
    "parameters": [
        {
            "name": "student_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Student ID"
        }
    ],
    "responses": {
        200: {
            "description": "Student details retrieved successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "roll_number": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "email": {"type": "string"},
                    "user_id": {"type": "integer"}
                }
            }
        },
        404: {
            "description": "Student not found"
        }
    }
}


update_application_status_swagger = {
    "tags": ["Company"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Update application status",
    "description": "Company updates the status of a student application (e.g., SHORTLISTED, REJECTED)",
    "parameters": [
        {
            "name": "application_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Application ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "SHORTLISTED"
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Application status updated",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "student_id": {"type": "integer"},
                    "drive_id": {"type": "integer"},
                    "status": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Application not found"
        }
    }
}

get_approved_drives_swagger = {
    "tags": ["Student"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Get approved placement drives",
    "description": "Fetch all placement drives approved by admin for students to apply",
    "responses": {
        200: {
            "description": "List of approved placement drives",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "company_name": {"type": "string"},
                        "job_title": {"type": "string"},
                        "job_description": {"type": "string"},
                        "eligibility_criteria": {"type": "string"},
                        "minimum_CGPA": {"type": "number"},
                        "application_deadline": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_package": {"type": "string"},
                        "status": {"type": "string"},
                        "created_at": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}


apply_for_drive_swagger = {
    "tags": ["Student"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Apply for a placement drive",
    "description": "Student applies to a placement drive",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["student_id", "drive_id"],
                "properties": {
                    "student_id": {
                        "type": "integer",
                        "example": 5
                    },
                    "drive_id": {
                        "type": "integer",
                        "example": 2
                    },
                    "notes": {
                        "type": "string",
                        "example": "Interested in backend role"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Application created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "student_id": {"type": "integer"},
                    "drive_id": {"type": "integer"},
                    "status": {"type": "string"},
                    "notes": {"type": "string"}
                }
            }
        },
        400: {
            "description": "Student already applied"
        }
    }
}


update_student_swagger = {
    "tags": ["Student"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Update student profile",
    "description": "Update student details such as name, CGPA, department, etc.",
    "parameters": [
        {
            "name": "student_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Student ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "John Doe"},
                    "email": {"type": "string", "example": "john@email.com"},
                    "department": {"type": "string", "example": "CSE"},
                    "cgpa": {"type": "number", "example": 8.5},
                    "phone": {"type": "string", "example": "9876543210"}
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Student updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "department": {"type": "string"},
                    "cgpa": {"type": "number"}
                }
            }
        },
        404: {
            "description": "Student not found"
        }
    }
}


get_student_applications_swagger = {
    "tags": ["Student"],
    "security": [
        {"Bearer": []}
    ],
    "summary": "Get student applications",
    "description": "Fetch all placement drive applications submitted by a student",
    "parameters": [
        {
            "name": "student_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Student ID"
        }
    ],
    "responses": {
        200: {
            "description": "List of applications",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "application_id": {"type": "integer"},
                        "application_date": {"type": "string"},
                        "application_status": {"type": "string"},
                        "drive": {
                            "type": "object",
                            "properties": {
                                "drive_id": {"type": "integer"},
                                "job_title": {"type": "string"},
                                "company_name": {"type": "string"},
                                "location": {"type": "string"},
                                "salary_package": {"type": "string"},
                                "application_deadline": {"type": "string"}
                            }
                        },
                        "notes": {"type": "string"}
                    }
                }
            }
        },
        500: {
            "description": "Server error"
        }
    }
}

get_company_by_id_swagger = {
    "tags": ["Company"],
"security": [
        {"Bearer": []}
    ],
    "summary": "Get company details by ID",
    "description": "Fetch details of a company using its ID",
    "parameters": [
        {
            "name": "company_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the company"
        }
    ],
    "responses": {
        200: {
            "description": "Company details retrieved successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "company_name": {"type": "string"},
                    "website": {"type": "string"},
                    "approval_status": {"type": "string"},
                    "description": {"type": "string"},
                    "industry": {"type": "string"},
                    "headquarters": {"type": "string"},
                    "created_at": {"type": "string"},
                    "updated_at": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Company not found"
        }
    }
}

get_student_details_swagger = {
    "tags": ["Student"],
"security": [
        {"Bearer": []}
    ],
    "summary": "Get student details by ID",
    "description": "Fetch details of a student using their ID",
    "parameters": [
        {
            "name": "student_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the student"
        }
    ],
    "responses": {
        200: {
            "description": "Student details retrieved successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "roll_number": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "gender": {"type": "string"},
                    "date_of_birth": {"type": "string"},
                    "department": {"type": "string"},
                    "degree": {"type": "string"},
                    "specialization": {"type": "string"},
                    "batch_year": {"type": "integer"},
                    "cgpa": {"type": "number"},
                    "tenth_percentage": {"type": "number"},
                    "twelfth_percentage": {"type": "number"},
                    "diploma_percentage": {"type": "number"},
                    "active_backlogs": {"type": "integer"},
                    "total_backlogs": {"type": "integer"},
                    "placement_status": {"type": "string"},
                    "willing_to_relocate": {"type": "boolean"},
                    "github_url": {"type": "string"},
                    "linkedin_url": {"type": "string"},
                    "portfolio_url": {"type": "string"},
                    "leetcode_rating": {"type": "integer"},
                    "hackerrank_rating": {"type": "integer"},
                    "skills": {"type": "string"},
                    "created_at": {"type": "string"},
                    "updated_at": {"type": "string"}
                }
            }
        },
        404: {
            "description": "Student not found"
        }
    }
}

get_admin_by_id_swagger = {
    "tags": ["Admin"],
"security": [
        {"Bearer": []}
    ],
    "summary": "Get admin details by ID",
    "description": "Fetch details of an admin user using their user ID",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the admin user"
        }
    ],
    "responses": {
        200: {
            "description": "Admin details retrieved successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "active": {"type": "boolean"},
                    "approved_status": {"type": "string"},
                    "created_at": {"type": "string"},
                    "created_by": {"type": "integer"},
                    "approved_at": {"type": "string"},
                    "approved_by": {"type": "integer"},
                    "roles": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        404: {"description": "User not found"},
        400: {"description": "User is not an admin"}
    }
}

