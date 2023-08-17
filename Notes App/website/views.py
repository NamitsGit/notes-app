from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Note
import json

views = Blueprint("views", __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        data = request.form.get("note")
        if len(data) < 1:
            flash("Could not add note as note is too short! Try again!", category="error")
        else:
            user_id = int(current_user.id)
            note = Note(data=data, user_id=user_id)
            db.session.add(note)
            db.session.commit()
            flash("Note added successfully!", category="success")
    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_node():
    note = json.loads(request.data)
    note_id = note["noteId"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})        