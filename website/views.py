from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        title = request.form.get('title')
        note = request.form.get('note')

        # Retrieve the uploaded file
        file = request.files['file']

        video = file.filename

        # Save the file to the uploads folder
        file.save('./website/static/media/' + file.filename)

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(title=title,data=note,video=video, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete/<int:id>')
def delete_note(id):  
    note = Note.query.get(id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Data removed added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/Detail/<int:id>')
def detail_note(id): 
    note = Note.query.get(id)
    # return note.title
    return render_template('details.html', note=note, user=current_user)
