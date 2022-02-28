import sqlalchemy.sql
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from flask_security import roles_accepted
from werkzeug.utils import secure_filename, redirect

from extensions import db
from models.comment import Comment
from models.post import Post
from models.user import User

admin = Blueprint('admin', __name__, static_folder='../static', template_folder='../templates')


@admin.route('/')
@roles_accepted('admin')
def dashboard():
    user = current_user.username
    return render_template('admin/dashboard.html', username=user, current_user=current_user)

@admin.route("/all-questions")
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
    return  render_template("admin/questions.html", qsts=questions)



@admin.route("/tick", methods=[ 'POST'])
def tick_answer():

    value = request.form.get('check_answer')
    if str(value) == "checked":
        value = "None"
    elif str(value)=="None":
        value = "checked"

    comment = Comment.query.filter_by(id=request.form.get("post_id")).update({"ticked": value})
    db.session.commit()
    return redirect(request.referrer)
