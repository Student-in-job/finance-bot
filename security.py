from database import SessionLocal, Admin
import os
from dotenv import load_dotenv

load_dotenv()

def is_user_admin(user_id):
    with SessionLocal() as session:
        return session.query(Admin).filter_by(user_id=user_id).first() is not None

def register_admin(user_id, username, pin):
    if pin != os.getenv("ADMIN_SECRET_PIN"):
        return False
    with SessionLocal() as session:
        if not session.query(Admin).filter_by(user_id=user_id).first():
            new_admin = Admin(user_id=user_id, username=username)
            session.add(new_admin)
            session.commit()
        return True
