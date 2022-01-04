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

if __name__ == "__main__":
    app.run(debug=True)
