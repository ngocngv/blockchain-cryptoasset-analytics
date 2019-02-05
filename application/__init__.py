from datetime import datetime
import os
from flask import Flask, url_for
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter, current_user, user_registered
from flask_wtf.csrf import CSRFProtect
from flask_blogging import SQLAStorage, BloggingEngine
from flask_principal import Principal, UserNeed, RoleNeed, identity_loaded
import flask_admin
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_heroku import Heroku

# Instantiate Flask extensions
db = SQLAlchemy()
csrf_protect = CSRFProtect()
mail = Mail()
migrate = Migrate()
blog_engine = BloggingEngine()
principal = Principal()
admin = {}

def create_app(config=None):
    """Create a Flask applicationlicaction.
    """
    # Instantiate Flask
    application = Flask(__name__)

    # Load application Config settings
    if config is not None:
        application.config.from_object('config.Config')

    # Setup Flask-SQLAlchemy
    db.init_app(application)

    # Setup Flask-Migrate
    migrate.init_app(application, db)
    
    # Setup Heroku
    heroku = Heroku(application)

    # Setup Flask-Mail
    mail.init_app(application)
    
    # Setup Flask-Principal
    principal.init_app(application)
    
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(application)
        
    # Setup Flask-Blogging
    with application.app_context():
        storage = SQLAStorage(db=db)
        db.create_all()
        blog_engine.init_app(application, storage)
        
    from application.models.user_models import User
    @blog_engine.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))       

    @identity_loaded.connect_via(application)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, "id"):
            identity.provides.add(UserNeed(current_user.id))
        # Shortcut to the give admins "blogger" role.
        #if hasattr(current_user, "is_admin"):
            #if current_user.is_admin:
                #identity.provides.add(RoleNeed("blogger"))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    # Register blueprints
    from application.views.misc_views import main_blueprint
    application.register_blueprint(main_blueprint)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    application.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to application.config.ADMINS
    init_email_error_handler(application)

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User, Role, MyRegisterForm

    db_adapter = SQLAlchemyAdapter(db, User)  # Setup the SQLAlchemy DB Adapter
    user_manager = UserManager(db_adapter, application,  # Init Flask-User and bind to application
                               register_form=MyRegisterForm)
    # Create admin
    global admin
    admin = flask_admin.Admin(application, 'Admin manager', template_mode='bootstrap3',)
    from .models.user_models import UserModelView,PostModelView, RoleModelView
    Post = storage.post_model
    admin.add_view(UserModelView(User, db.session))
    #admin.add_view(RoleModelView(Role, db.session))
    #admin.add_view(sqla.ModelView(Role, db.session))
    admin.add_view(PostModelView(Post, db.session))  
    admin.add_link(MenuLink(name='Index', category='Index', url='../'))  
    
    return application


def init_email_error_handler(application):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to application.config.ADMINS.
    """
    if application.debug: return  # Do not send error emails while developing

    # Retrieve email settings from application.config
    host = application.config['MAIL_SERVER']
    port = application.config['MAIL_PORT']
    from_addr = application.config['MAIL_DEFAULT_SENDER']
    username = application.config['MAIL_USERNAME']
    password = application.config['MAIL_PASSWORD']
    secure = () if application.config.get('MAIL_USE_TLS') else None

    # Retrieve application settings from application.config
    to_addr_list = application.config['ADMINS']
    subject = application.config.get('application_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    application.logger.addHandler(mail_handler)

    # Log errors using: application.logger.error('Some error message')



