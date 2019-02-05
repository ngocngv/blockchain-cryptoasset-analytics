from flask_user import UserMixin, current_user
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from hashlib import md5
from application import db
from flask_admin.contrib.sqla import ModelView
from flask_blogging import SQLAStorage
# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    telegram = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    discord = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    api_key = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    api_secret = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    #is_admin = db.Column(db.Boolean, default=False)
    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    def get_name(self):
        return self.first_name+" "+self.last_name # typically the user's name
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    def __repr__(self):
        if self.is_admin:
            return '<Admin: {0}>'.format(self.first_name)
        return '<User: {0}>'.format(self.first_name)
        
# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes
    def __repr__(self):
        return '<{0}>'.format(self.name)

# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# Define the User registration form
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])

# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name (*)', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name (*)', validators=[
        validators.DataRequired('Last name is required')])
    telegram = StringField('Telegram')
    discord = StringField('Discord')
    api_secret = StringField('Binance API secret')
    api_key = StringField('Binance API key')
    submit = SubmitField('Save')

 # Customized Role model for SQL-Admin
class RoleModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role('admin')
        return False

class PostModelView(ModelView):
    column_exclude_list = ('text')
    column_auto_select_related = True
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role('admin')
        return False

class UserModelView(ModelView): 
    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)
    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True
    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.has_role('admin')
        return False
    column_exclude_list = ('password','api_key','api_secret','confirmed_at')
    searchable_columns_list = ('first_name', 'last_name','email') 
    column_sortable_list = ('first_name', 'last_name','email')
    can_create = True
    can_delete = False   
    # If you want to make them not editable in form view: use this piece:
    form_widget_args = {
        'email': {
            'readonly': True
        },
    }

