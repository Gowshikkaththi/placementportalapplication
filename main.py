from models import create_db_and_tables,engine
from flask import Flask,render_template, request, redirect, url_for, session, flash
from api_routes.registration_endpoints import register_api
from api_routes.admin_endpoints import admin_api
from api_routes.company_endpoints import company_api
from api_routes.student_endpoints import student_api
from flask_login import current_user,LoginManager,login_user
from models.student import Student
from models.company_user import CompanyUser
from flask import abort ,request
from flasgger import Swagger,swag_from
from models.users import User
from config.admin_creation import create_admin
from config.db_creation import db_session
from config.swagger import swagger_template,login_doc
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
import os


create_db_and_tables()
create_admin(engine)
print("admin created")
app = Flask(__name__)

app.register_blueprint(register_api, url_prefix="/register")
app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(student_api, url_prefix="/student")
app.register_blueprint(company_api, url_prefix="/company")

app.config["JWT_SECRET_KEY"] = "#MAD!1@PROJECT*^$"
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']  # Try cookies first, then headers
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Set to True in production
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = os.urandom(24)



@app.route("/login", methods=["POST","GET"])
@swag_from(login_doc)
def login():
    if request.method == "POST":
        db = db_session()
        id = None
        user = db.query(User).filter_by(
            username=request.form.get("username")
        ).first()

        if not user:
            return {"message": "User not found"}, 404

        if not check_password_hash(user.password, request.form.get("password")):
            return {"message": "Invalid password"}, 401
        print('hi')
        print(user.approved_status)
        if user.approved_status != "Approved":
            return {"message": "User not approved"}, 403

        roles = [role.name for role in user.roles]
        if roles[0] =='STUDENT':
            student = db.query(Student).filter_by(
            user_id=user.id
        ).first()
            id = student.id

        if roles[0] =='COMPANY':
            company = db.query(CompanyUser).filter_by(
            user_id=user.id
        ).first()
            id = company.company_id

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "roles": roles
            }
        )


        session["access_token"] = token
        session["roles"] = roles
        session["user_id"] = user.id
        session["table_id"] = id
        if "ADMIN" in roles:
            response =  redirect(url_for("admin_api.admin_dashboard"))
        elif "COMPANY" in roles:
            response =  redirect(url_for("company_api.company_dashboard"))
        elif "STUDENT" in roles:
            response =  redirect(url_for("student_api.student_dashboard"))
        else:
            flash("Role not recognized!", "danger")
            response =  redirect(url_for("login"))
        response.set_cookie(
            'access_token_cookie',
            token,
            httponly=True,  # Can't be accessed by JavaScript (more secure)
            secure=False,  # Set to True in production
            samesite='Lax'
        )

        flash("Login successful!", "success")
        db.close()
        return response

    return render_template("login.html")


@app.route("/logout")
def logout():

    # Clear session data
    session.pop("access_token", None)
    session.pop("roles", None)
    session.pop("user_id", None)
    session.pop("table_id", None)

    flash("Logged out successfully!", "success")

    # Redirect to login
    response = redirect(url_for("login"))

    # Remove JWT cookie
    response.set_cookie(
        "access_token_cookie",
        "",
        expires=0
    )

    return response

swagger = Swagger(app,template=swagger_template)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True, threaded=False)