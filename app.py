from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"




@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        Todo_data = Todo(title=title, description=description)
        db.session.add(Todo_data)
        db.session.commit()

        # Redirect to the same route to prevent form resubmission
        return redirect('/')

    # Add a sample todo to the database
    # todo = Todo(title="First Todo", description="Test description")
    # db.session.add(todo)
    # db.session.commit()
    
    # Query all todos
    showAll = Todo.query.all()
    # print(showAll)
    
    # Pass the data to the template
    return render_template('index.html', data=showAll)

@app.route('/delete/<int:sno>')
def delete(sno):
    # Fetch the item to be deleted
    todo_to_delete = Todo.query.filter_by(sno=sno).first()
    
    # Delete the item
    db.session.delete(todo_to_delete)
    db.session.commit()
    
    # Redirect to the home page
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    
    todo_to_update = Todo.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        # Update the title and description
        title = request.form['title']
        description = request.form['description']

        todo_to_update.title = title
        todo_to_update.description = description
        
        # Commit the changes
        db.session.commit()
        return redirect('/')

    return render_template('update.html', todo=todo_to_update)

@app.route('/show')
def showAll():
    showAll = Todo.query.all()
    print(showAll)
    return 'This is products page'

if __name__ == '__main__':
    # create db `./instance/todo.db`
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
