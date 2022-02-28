import flask_security
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user
from flask_security import logout_user, SQLAlchemyUserDatastore, roles_accepted
from werkzeug.security import check_password_hash

from models.location import Location
from models.post import Post
from models.role import Role
from models.user import User
from extensions import db, login_manager, bcrypt, SQLAlchemyError, OperationalError

main = Blueprint('main', __name__, static_folder='../static', template_folder='../templates')


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

#LOGIN PAGE
@main.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

#LOGGIN IN
@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember_me = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        login_user(user)

        flash(f"Hi {user.username}!", "success")

        if user.roles[0].name.__eq__("farmer"):
            return redirect(url_for('main.questions'))
        if user.roles[0].name.__eq__("admin"):
            return redirect(url_for('admin.questions'))
        else:
            flash("Error! Recreate your account, please", "alert")
            return "NO DEFINED ROLE"
    flash("Invalid Password/ Email. Please Try Again!", "alert")
    return render_template("auth/login.html")
@login_required
@main.route('/register', methods=['GET'])
def register():
    return render_template("auth/register.html")


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
@main.route('/register', methods=[ 'POST'])
def add_farmer():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if password.__ne__(password_confirm):
            flash("Password does not match Password confirmation. Please match the passwords.", "alert")
            return render_template("auth/register.html")
        # LOCATION
        street = request.form.get('street')
        city = request.form.get('city')
        country = request.form.get('country')

        farmer_role = Role(name='farmer')
        try:
            user = user_datastore.create_user(username=username, email=email,
                                              password=bcrypt.generate_password_hash(password), roles=[farmer_role])
            db.session.add(user)
            db.session.commit()
            location = Location(street=street, city=city, country=country, user_id=user.id)
            db.session.add(location)
            db.session.commit()
        except SQLAlchemyError as e:
            flash(f"{str(e.__dict__['orig'])}", "danger text-center")
            db.session.rollback()
            return render_template("auth/register.html")
        except OperationalError as o:
            flash(f"{str(o.__dict__['orig'])}", "danger text-center")
            db.session.rollback()
            return render_template("auth/register.html")
        else:
            db.session.commit()
        return redirect(url_for("main.login"))

@main.route("/questions")
def questions():
    QSTNS = Post.query.all()
    questions = [];
    for qst in QSTNS:
        question = {}
        user = User.query.get(qst.user_id)
        question = {
            "user_id":qst.user_id,
            "id":qst.id,
            "title":qst.title,
            "body": qst.body,
            "created_at":qst.created_at,
            "user":user.username,
            "user_profile":user.username[0],
            "no_comments": qst.comments
        }
        questions.append(question)
    return  render_template("main/questions.html", qsts=questions, current_user= current_user)

@main.route('/question/<id>', methods=['GET'])
def question(id):
    post = Post.query.get(id)
    user = User.query.get(post.user_id)
    _comments = post.comments
    comments = []
    for comment in _comments:
        _user = User.query.get(comment.user_id)
        comment ={"user":_user,"comment":comment}
        comments.append(comment)
    return render_template("main/post.html", post=post, user=user, comments=comments, current_user=current_user)

@main.route("/tags")
def tags():
    return render_template("main/tagged_qstns.html")


@main.route("/users")
def users():
    users = User.query.all()
    users = [user for user in users if user.roles[0]=="farmer"]
    return render_template("main/user_qstns.html", users=users)
@main.route("/user-posts/<id>")
def user_posts(id):
    posts = Post.query.filter_by(user_id = id).all()
    return render_template("farmer/questions.html", posts= posts)
@main.route("/")
def index():
    return render_template("index.html", current_user=current_user)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/help')
def help():
    return render_template("help.html")

@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/search/<text>',  methods=['GET'])
def search_by_id(text):
    search_results = Post.all()
    return render_template('main/search_qstns.html', object_frames=search_results, search_txt=text)


