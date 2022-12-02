from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integrer, default=0)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

@app.route("/", methods=['POST' , 'GET'])
def index():
    if request.method == 'POST':
        task_content= request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'no se pudo agregar su tarea'
    else:
        Tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return rendirect('/')
    except:
        return 'No se pudo eliminar su tarea'

@app.route('/update/<int:id>', methods=['POST' , 'GET'])
def update(id):
    task= Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['conntent']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'No se pudo actualizar esta tarea'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)