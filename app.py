from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/deleted/<int:sno>')
def delete(sno):
    user = Todo.query.filter_by(sno=sno).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/')
@app.route('/update/<int:sno>', methods=['POST','GET'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        updating_todo = Todo.query.filter_by(sno=sno).first()
        updating_todo.title = title
        updating_todo.desc = desc
        db.session.add(updating_todo)
        db.session.commit()
        return redirect('/')
    updating_todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', updating_todo=updating_todo)

if __name__ == '__main__':
    app.run(debug=True, port=5050)