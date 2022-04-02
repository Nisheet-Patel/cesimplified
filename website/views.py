from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session, jsonify
from flask_login import login_required, current_user
from .models import Course,Topic,Videos
from . import db

views = Blueprint('views',__name__)

def list_to_dict(_list):
    # [(id, 'title', 'img_name', total_videos, 'course_title')]
    topic_data = [{
            "id": data[0],
            "title": data[1],
            "img_name": data[2],
            "total_videos": data[3],
            "course_title": data[4]
        } for data in _list]
    return topic_data

@views.route('/')
def login():
    return render_template("login.html")

@views.route('/course')
@login_required
def course():
    course_data = db.session.query(Course).order_by(Course.id).all()
    return render_template('index.html', course=course_data)

#  send json data for selected course
@views.route('/get/course/<course_id>')
@login_required
def send_data(course_id):
    if course_id == '0':
        topic_data = db.session.query(Topic.id ,Topic.title, Topic.img_name, Topic.total_videos, Course.title).join(Course).all()
    else:    
        topic_data = db.session.query(Topic.id ,Topic.title, Topic.img_name, Topic.total_videos, Course.title).join(Course).filter(Course.id == course_id).all()
    
    data = list_to_dict(topic_data)
    return jsonify(topic=data)


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
        video_data = db.session.query(Videos).filter(Videos.title.contains(str(value))).all()

        return render_template('search.html', videos=video_data, search_value=value)
    return render_template('search.html', search_value='None')