from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.registation_impl import register_user
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

register_api = Blueprint("registration_api", __name__)

@register_api.route('/')
def register():
    if request.method == "POST":
        role = request.form.get("role").upper()

        if role == "STUDENT":
            payload = {
                "username": request.form.get("username"),
                "password": request.form.get("password"),
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "roll_number": request.form.get("roll_number"),
                "degree": request.form.get("degree"),
                "department": request.form.get("department"),
                "batch_year": int(request.form.get("batch_year")),
                "cgpa": float(request.form.get("cgpa")),
                "skills": request.form.get("skills"),
                "role": "STUDENT"
            }
        elif role == "COMPANY":
            payload = {
                "username": request.form.get("username"),
                "password": request.form.get("password"),
                "company_name": request.form.get("company_name"),
                "description": request.form.get("description"),
                "email": request.form.get("email"),
                "headquarters": request.form.get("headquarters"),
                "industry": request.form.get("industry"),
                "website": request.form.get("website"),
                "role": "COMPANY"
            }
        else:
            flash("Invalid role selected.", "danger")
            return redirect(url_for("register"))

        # Send payload to backend API
        response = requests.post("http://localhost:5000/api/register", json=payload)
        if response.status_code in [200, 201]:
            data = response.json()
            flash(data.get("message", "Registration successful!"), "success")
            return redirect(url_for("login"))
        else:
            # display error message
            data = response.json()
            flash(data.get("message", "Registration failed."), "danger")
            return redirect(url_for("register"))

    return render_template("register.html")

@register_api.route("/register_student", methods=["POST"])
@swag_from({
    "tags": ["Register"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {

                    "username": {
                        "type": "string",
                        "example": "gowshik123"
                    },
                    "role": {
                        "type": "string",
                        "example": "STUDENT"
                    },

                    "email": {
                        "type": "string",
                        "example": "gowshik@student.com"
                    },

                    "password": {
                        "type": "string",
                        "example": "password123"
                    },

                    "roll_number": {
                        "type": "string",
                        "example": "21CSE001"
                    },

                    "first_name": {
                        "type": "string",
                        "example": "Gowshik"
                    },

                    "last_name": {
                        "type": "string",
                        "example": "Raj"
                    },

                    "phone": {
                        "type": "string",
                        "example": "9876543210"
                    },

                    "department": {
                        "type": "string",
                        "example": "CSE"
                    },

                    "degree": {
                        "type": "string",
                        "example": "BTech"
                    },

                    "batch_year": {
                        "type": "integer",
                        "example": 2025
                    },

                    "cgpa": {
                        "type": "number",
                        "example": 8.5
                    },

                    "skills": {
                        "type": "string",
                        "example": "Python, SQL, React"
                    }

                },
                "required": [
                    "username",
                    "email",
                    "password",
                    "roll_number",
                    "first_name",
                    "phone",
                    "department",
                    "degree",
                    "batch_year"
                ]
            }
        }
    ],

    "responses": {
        201: {
            "description": "Student registered successfully"
        },
        400: {
            "description": "Validation error"
        }
    }
})
def register_user_student():
    data = request.json
    return register_user(data)


@register_api.route("/register_company", methods=["POST"])
@swag_from({
    "tags": ["Register"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {

                    "username": {
                        "type": "string",
                        "example": "hr_gowshik"
                    },
                    "role": {
                        "type": "string",
                        "example": "COMPANY"
                    },
                    "email": {
                        "type": "string",
                        "example": "hr@abctech.com"
                    },

                    "password": {
                        "type": "string",
                        "example": "password123"
                    },

                    "company_name": {
                        "type": "string",
                        "example": "ABC Technologies"
                    },

                    "website": {
                        "type": "string",
                        "example": "https://abctech.com"
                    },

                    "industry": {
                        "type": "string",
                        "example": "Information Technology"
                    },

                    "headquarters": {
                        "type": "string",
                        "example": "Chennai, India"
                    },

                    "description": {
                        "type": "string",
                        "example": "AI and Cloud solutions company"
                    }

                },
                "required": [
                    "username",
                    "email",
                    "password",
                    "company_name"
                ]
            }
        }
    ],

    "responses": {

        201: {
            "description": "User successfully linked to company",
            "examples": {
                "application/json": {
                    "message": "User successfully linked to company",
                    "user_id": 12,
                    "company_id": 3
                }
            }
        },

        400: {
            "description": "User already mapped to this company"
        },

        500: {
            "description": "Internal server error"
        }

    }
})
def register_user_company():
    data = request.json
    return register_user(data)