import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   if request.method == 'POST':
      note = request.form.get('note')
      
      if len(note) < 1:
         flash('Note is too short!', category='error')
      else:
         new_note = Note(data=note, user_id=current_user.id)
         db.session.add(new_note)
         db.session.commit()
         flash('Note added!', category='success')
   return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
   note = json.loads(request.data)
   noteId = note['noteId']
   note = Note.query.get(noteId)
   if note: 
      if note.user_id == current_user.id:
         db.session.delete(note)
         db.session.commit()
         return jsonify({})
      

@views.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)

    # Security: only owner can edit
    if note.user_id != current_user.id:
        flash("Not authorized!", category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        note.data = request.form.get('note')
        db.session.commit()
        flash("Note updated successfully!", category="success")
        return redirect(url_for('views.home'))

    return render_template("edit_note.html", note=note)



##@views.route('/features')
##def features():
##   return render_template("features.html")

##@views.route('/about')
##def about():
##   return render_template("about.html")