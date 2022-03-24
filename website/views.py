from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_required, current_user
from .models import Course,Topic,Videos
from . import db

views = Blueprint('views',__name__)

@views.route('/')
def login():
    return render_template("login.html")

@views.route('/course')
@login_required
def course():
    course_data = db.session.query(Course).join(Topic, Topic.course_id == Course.id).order_by(Course.id).all()
    topic_data = db.session.query(Topic.id ,Topic.title, Course.title).join(Course).all()
    print(course_data,topic_data)
    return render_template('index.html', course=course_data, topic=topic_data)

@views.route('/course/<course>/<topic_id>')
@login_required
def topic(course, topic_id):
    topic_data = db.session.query(Topic).get(topic_id)
    videos_data = Videos.query.filter_by(topic_id=topic_data.id).all()

    return render_template('topic-page.html', topic=topic_data, videos=videos_data)

@views.route('/search', methods=['GET','POST'])
@login_required
def search():
    if request.method == 'POST':
        value = request.form.get('search-value')
        print("--------VALUE",value)
        video_data = db.session.query(Videos).filter(Videos.title.contains(str(value))).all()
        print(video_data)

        return render_template('search.html', videos=video_data, search_value=value)
    return render_template('search.html', search_value='None')