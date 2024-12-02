from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Todo model for the database
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(100), nullable=False)  # New column for user
    status = db.Column(db.String(50), nullable=False, default='Open')  # New column for status

# Initialize the database
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        user = request.form["user"]
        status = request.form["status"]
        
        # Check if the title and description are empty
        if not title or not desc:
            error_message = 'Title and Description or Assign User cannot be empty...!'
        else:
            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_todo = Todo(title=title, desc=desc, date_created=date_created, user=user, status=status)
            db.session.add(new_todo)
            db.session.commit()
            return redirect("/")  # Redirect to avoid resubmission

    # Fetch all todos to display them on the page
    all_todos = Todo.query.all()
    return render_template("index.html", allTodo=all_todos, error=error_message)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        todo.user = request.form["user"]
        todo.status = request.form["status"]
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>", methods=["POST"])
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
