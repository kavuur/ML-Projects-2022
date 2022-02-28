import os
import re
from flask import  Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_security import roles_accepted
from werkzeug.utils import secure_filename
from diagnose import DiseaseDiagnosis, MODEL
from extensions import db, bcrypt, SQLAlchemyError, OperationalError
from inference import remidies
from models.comment import Comment
from models.history import History
from models.location import Location
from models.post import Post
from models.user import User

farmer = Blueprint('farmer', __name__, static_folder='../static', template_folder='../templates')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@farmer.route('/farmer', methods=['GET'])
@roles_accepted('farmer')
@login_required
def dashboard():
    return render_template('farmer/dashboard.html', current_user=current_user)

@farmer.route('/question/ask', methods=['GET'])
@login_required
def ask_question():
    return render_template("farmer/ask_question.html")

@farmer.route('/post-question', methods=['POST'])
@login_required
def post_question():
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        user_id = current_user.id
        post = Post(title, body, user_id)
        db.session.add(post)
        db.session.commit()
        flash("Question successfully posted ", "success")
        return redirect(url_for("farmer.my_posts"))
    return "error"

@farmer.route('/user/posts', methods=['GET'])
@login_required
def my_posts():
    posts = current_user.posts
    return render_template("farmer/questions.html", posts= posts)

@farmer.route('/comment', methods=['GET','POST'])
@login_required
def comment():
    if request.method=="POST":
        user_id = current_user.id
        _comment = request.form.get("comment")
        post_id = request.form.get("id")
        comment = Comment(_comment=_comment, _userId = user_id, _postId=post_id)
        db.session.add(comment)
        db.session.commit()
        flash("Answer successfully submitted", "success")
        return redirect(url_for('main.questions'))
    return render_template("main/questions.html")


@farmer.route('/profile', methods=['GET'])
@login_required
def edit_profile():
    user_info = current_user
    return render_template('farmer/profile.html', user=user_info)



@farmer.route('/save-profile', methods=['POST', 'GET'])
@login_required
def save_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    street = request.form.get('street')
    city = request.form.get('city')
    country = request.form.get('country')
    try:
        user = User.query.filter_by(id=current_user.id).update({"username": username, "email": email, "phone": phone})
        location = Location.query.filter_by(user_id=current_user.id).update({"street": street, "city": city, "country": country})
    except SQLAlchemyError as e:
        flash(f"{str(e.__dict__['orig'])}", "alert text-center")
        db.session.rollback()
        redirect(url_for("farmer.edit_profile"))
    except OperationalError as o:
        flash(f"{str(o.__dict__['orig'])}", "alert text-center")
        db.session.rollback()
        return redirect(url_for("farmer.edit_profile"))
    else:
        db.session.commit()
    flash("Successfully edit user profile.", "success text-center")
    return redirect(url_for("farmer.edit_profile"))


@farmer.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():
    old_pwd = request.form.get('old_password')
    new_pwd = request.form.get('new_password')
    confirm_pwd = request.form.get('password_confirm')
    user = User.query.filter_by(id=current_user.id).first()
    if user and user.verify_password(old_pwd):
        if new_pwd.__ne__(confirm_pwd):
            flash("Password does not match Password confirmation. Please match the passwords.", "alert")
            return redirect(url_for("farmer.edit_profile"))
        user = User.query.filter_by(id=current_user.id).update({"password": bcrypt.generate_password_hash(new_pwd)})
        db.session.commit()
        flash("Successfully change password!", "success text-center")
        return redirect(url_for("farmer.edit_profile"))
    flash("Incorrectly credentials. Please try again!", "alert text-center")
    return  redirect(url_for("farmer.edit_profile"))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_disease_name(file):
    d = DiseaseDiagnosis()
    image = d.process_image(file)
    pred = d.predict(MODEL, image)
    disease = d.prediction_cls(pred)
    #disease = mappings[pred_v]
    return  disease, remidies[disease]

@farmer.route("/diagnosis", methods=['POST', 'GET'])
@login_required
@roles_accepted("farmer")
def diagnose():
    return render_template("farmer/diagnosis.html", disease="",image_url=None,remidy={"remidy":""})

def format_name(s):
   return re.sub('_+', ' ', s)

@farmer.route("/detect", methods=['POST', 'GET'])
@login_required
@roles_accepted("farmer")
def detect():
    diseas=""
    remidy=""
    if request.method == "POST":
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("No selected file",  "alert text-center")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/uploads', filename))
            diseas, remidy = get_disease_name(f"static/uploads/{filename}")
            keep_history(disease_name=diseas, user_id=current_user.id,image_url=filename)

            return render_template("farmer/diagnosis.html", disease=format_name(diseas), remidy=remidy, image_url=filename)
    return render_template("farmer/diagnosis.html", disease=diseas, remidy=remidy)


def keep_history(disease_name, user_id, image_url):
    history = History(disease=disease_name, user_id=user_id, image=image_url)
    db.session.add(history)
    db.session.commit()

@farmer.route("history/item/<id>", methods=['GET', 'POST'])
def delete_history(id):
    history = History.query.filter_by(id=id).first()
    db.session.delete(history)
    db.session.commit()
    flash("History item delete ", "success")
    return redirect(url_for("farmer.diagnosis_history"))


@farmer.route("diagnosis-history")
def diagnosis_history():
    history = current_user.history;
    return render_template("farmer/diagnosis_history.html", diagnosis_history = history, remidies=remidies,f=format_name)


