"""
A simple Flask application for managing Todo items.
This application provides functionality for managing Todo items,
including adding, deleting, and updating them.
It utilizes Flask for web routing and SQLAlchemy for database management.

Classes:
    Todo: Represents a Todo item in the database.

Routes:
    /: Renders the homepage, displaying all Todo items.

Attributes:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    '''
    Class representing a Todo item in the database.

    Attributes:
        id (int): The unique identifier for the Todo item.
        content (str): The content of the Todo item.
        date_created (datetime): The date and time when the Todo item was created.

    Methods:
        __repr__: Returns a string representation of the Todo item.
    '''
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        '''
        Returns a string representation of the Todo item.
        '''
        return f'<Task {self.id}>'


# with app.app_context():
#     db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Route function for homepage
    Returns html content rendered from template:index.html
    '''
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except ValueError as e:
            return ("There is an issue adding your task, error : ", e)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:del_id>')
def delete(del_id):
    '''
    Route function to delete a task
    '''
    task_to_delete = Todo.query.get_or_404(del_id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return ('There was a problem, error:', e)


@app.route('/update/<int:up_id>', methods=['GET', 'POST'])
def update(up_id):
    '''
    Route function to update a task
    '''
    task = Todo.query.get_or_404(up_id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except ValueError:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
