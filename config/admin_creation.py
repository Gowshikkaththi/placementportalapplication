from sqlalchemy.orm import Session

from config.constants import student_role, description , company_role
from models.users import User
from models.roles import Role
from models.user_role import roles_users
from werkzeug.security import generate_password_hash
from datetime import datetime



def create_admin(engine):
    session = Session(engine)

    try:
        # 1️⃣ Ensure ADMIN role exists
        admin_role = session.query(Role).filter_by(name="ADMIN").first()

        if not admin_role:
            admin_role = Role(
                name="ADMIN",
                description="System Administrator"
            )
            session.add(admin_role)
            session.commit()  # Commit to ensure role exists
            print("ADMIN role created")

        student = session.query(Role).filter_by(name=student_role).first()

        if not student:
            student = Role(
                name=student_role,
                description=description[student_role]
            )
            session.add(student)
            session.commit()  # Commit to ensure role exists
            print("Student role created")

        company = session.query(Role).filter_by(name=company_role).first()

        if not company:
            company = Role(
                name=company_role,
                description=description[company_role]
            )
            session.add(company)
            session.commit()  # Commit to ensure role exists
            print("company role created")

        # 2️⃣ Check if admin user exists
        admin_user = session.query(User).filter_by(username="admin").first()

        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@placement.com",
                password=generate_password_hash("admin123"),
                active=True,
                approved_status = "Approved",
                created_by="SYSTEM"
            )

            session.add(admin_user)
            session.flush()  # Get the user ID without committing

            # Method 1: Using the relationship (should work)
            admin_user.roles.append(admin_role)

            # Optional auditing
            admin_user.approved_by = admin_user.id
            admin_user.approved_at = datetime.utcnow()

            session.commit()
            print("Admin user created successfully with ADMIN role!")

            # Verify the association was created
            check_association = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id
                )
            ).first()
            print(f"Association created: {check_association is not None}")

        else:
            print("Admin user already exists")

            # Check if user already has the role
            has_role = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id,
                    roles_users.c.role_id == admin_role.id
                )
            ).first()

            if not has_role:
                # Method 2: Direct insert if relationship isn't working
                session.execute(
                    roles_users.insert().values(
                        user_id=admin_user.id,
                        role_id=admin_role.id
                    )
                )
                session.commit()
                print("ADMIN role assigned to existing admin user via direct insert!")
            else:
                print("Admin user already has ADMIN role")

    except Exception as e:
        session.rollback()
        print(f"Error creating admin: {e}")
        raise
    finally:
        session.close()