from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from todo import Todo, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


# with app.app_context():
#     db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content_task = request.form['content']
        new_task = Todo(content=content_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your new task to db!!'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete_task/<string:tid>', methods=['GET', 'POST'])
def delete_task(tid):
    task = Todo.query.filter_by(id=tid).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        print(f"task {tid} deleted")
    else:
        return 'Task not found', 404
    return redirect(url_for('index'))


@app.route('/update_task/<string:tid>', methods=['GET','POST'])
def update_task(tid):
    if request.method == 'POST':
        task = Todo.query.filter_by(id=tid).first()
        task.content = request.form['content']
        task.date_created = func.now()
        db.session.commit()
        return redirect(url_for('index'))
    else:
        task = Todo.query.filter_by(id=tid).first()
        return render_template('update_task.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
