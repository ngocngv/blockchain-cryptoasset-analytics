import datetime
from flask import current_app
from flask_script import Command
from application import db
from application.models.user_models import User, Role

class InitDbCommand(Command):
    """ Initialize the database."""
    def run(self):
        init_db()

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """
    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'admin')
    blogger_role = find_or_create_role('blogger', u'blogger')
    
    # Add users
    user = find_or_create_user('Supreme', 'Administrator', 'blockchain.cryptoasset.analytics@gmail.com', 'xxxxxx', admin_role)
    user.roles.append(admin_role)
    user = find_or_create_user('Vuong', 'Trinh', 'vanvuong.trinh@gmail.com', 'xxxxx',blogger_role)
    user.roles.append(admin_role) 
    
    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user



