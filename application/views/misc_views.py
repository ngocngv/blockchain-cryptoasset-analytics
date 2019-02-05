from flask import Blueprint, redirect, render_template,current_app, request, url_for
from flask_user import current_user, login_required, roles_accepted
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
from flask_blogging import SQLAStorage,BloggingEngine
from flask_blogging.views import _get_blogging_engine, _is_blogger
import application
from application import db,blog_engine
from application.models.user_models import UserProfileForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    blogging_engine = _get_blogging_engine(current_app)
    storage = blogging_engine.storage
    meta = {}
    meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
    posts = storage.get_posts()
    return render_template("index.html", posts=posts,meta = meta)
    
@main_blueprint.route('/.well-known/brave-payments-verification.txt')
def brave():
    return redirect("https://kenhtaichinh.herokuapp.com/static/.well-known/brave-payments-verification.txt")
    
@main_blueprint.route('/afterlogin')
def afterlogin():
    identity_changed.send(current_app._get_current_object(),identity=Identity(current_user.id))
    blogging_engine = _get_blogging_engine(current_app)
    storage = blogging_engine.storage	
    meta = {}
    meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
    posts = storage.get_posts()
    return render_template("index.html", posts=posts,meta = meta)    
    
@main_blueprint.route('/afterlogout')
def afterlogout():
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    blogging_engine = _get_blogging_engine(current_app)
    storage = blogging_engine.storage
    meta = {}
    meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
    posts = storage.get_posts()
    return render_template("index.html", posts=posts, meta = meta)  

@main_blueprint.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form)
    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)
        # Save user_profile
        db.session.commit()
        # Redirect to home page
        return redirect(url_for('main.index'))
    # Process GET or invalid POST
    return render_template('flask_user/user_profile_page.html',form=form)


