from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db = SQLAlchemy(app)
 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return "<Note %r>" %self.id 

@app.route("/", methods = ['POST','GET'])
def default():
    if request.method == "POST":
        note_title = request.form['title']
        note_content = request.form['content']

        new_note = Note(title = note_title,content=note_content)

        try:

            db.session.add(new_note)
            db.session.commit()

            return redirect("/")

        except:

            return "Sorry, an error occured"

    else:

        notes = Note.query.order_by(Note.date_created).all()

        return render_template("index.html", notes=notes)


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    
    target_note = Note.query.get_or_404(note_id)

    try:
        db.session.delete(target_note)
        db.session.commit()

        return redirect("/")

    except:
        return "Sorry, an error occured while deleting the specified note"


@app.route('/update/<int:note_id>', methods=['GET', 'POST'])
def update_note(note_id):

    target_note = Note.query.get_or_404(note_id)
    
    if request.method == "POST":

        target_note.title = request.form['title']
        target_note.content = request.form['content']

        try:
            db.session.commit()

            return redirect("/")
        
        except:
            return "Sorry, an error occured while updating the specified note"

    else:

        return render_template("update.html", note=target_note)

if __name__ == "__main__":
    app.run(debug=True)
