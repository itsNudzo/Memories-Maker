from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import DiaryStory
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        story=request.form.get('story')

        if len(story) < 1:
            flash('Sorry, your story is empty.', category='error')
        else:
            new_story=DiaryStory(data=story, user_id=current_user.id)
            db.session.add(new_story)
            db.session.commit()
            flash('Story added successfully!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-story', methods=['POST'])
def delete_story():
    story=json.loads(request.data)
    storyId=story['storyId']
    story=DiaryStory.query.get(storyId)
    if story:
        if story.user_id == current_user.id:
            db.session.delete(story)
            db.session.commit()
            
    return jsonify({})