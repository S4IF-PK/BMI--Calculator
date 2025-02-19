# import os
# import subprocess
# import platform
# import urllib.parse
# import random
# from concurrent.futures import ThreadPoolExecutor ,as_completed
# # print(platform.system())
# def url_maker(message,num):
#     encoded_msg = urllib.parse.quote(message)
#     return f"https://wa.me/{num}?text={encoded_msg}"
# def number_file_handler(file_name):
#     count = 0
#     numbers = []
#     with open(file_name, 'r') as file:
#         for line in file:  # Read the file line by line
#             number = line.strip() 
#             numbers.append(number)
#             count +=1
#         return count,numbers

# def ask():
#     while True:
#         ask_num_file = input("Enter Number file name: ")
#         if os.path.exists(ask_num_file):
#             break
#         else:
#             print("File not Exist !!")
#     while True:
#         ask_msg = input("What is Your message :")
#         if os.path.exists(ask_msg):
#             with open(ask_msg,"r") as f:
#                 msg_content = f.read()
#                 print(msg_content)
#             break
#         else:
#             print("Msg File not Exist !!")
#     numbers = number_file_handler(ask_num_file)
#     for _ in range(numbers[0]):
#         os.system(f"start {url_maker(message=msg_content,num=numbers[1][_])}")


# def zong():
#     zongcode = ['+92310','+92311','+92312','+92313','+92314','+92315','+92316','+92317','+92318','+92319','+92370']
#     return f'{(random.choice(zongcode))}{random.randrange(1000000,9999999)}'
# def jazz():
#     jazzcode = ['+92301','+92302','+92303','+92304','+92305','+92306','+92307','+92308','+92309','+92320','+92321','+92322','+92323','+92324','+92325','+92326','+92327','+92328','+92329']
#     return f'{(random.choice(jazzcode))}{random.randrange(1000000,9999999)}'
# def telenor():
#     telenorcode = ['+92340','+92341','+92342','+92343','+92344','+92345','+92346','+92347','+92348','+92349']
#     return f'{(random.choice(telenorcode))}{random.randrange(1000000,9999999)}'
# def ufone():
#     ufonecode = ['+92330','+92331','+92332','+92333','+92334','+92335','+92336','+92337','+92338','+92339']
#     return f'{(random.choice(ufonecode))}{random.randrange(1000000,9999999)}'
# def numbers_gen(quantity,file_name):
#     number_set = set()
#     with ThreadPoolExecutor(max_workers=os.cpu_count()) as exe:
#         results = [exe.submit(random.choice([zong,jazz,ufone,telenor])) for _ in range(quantity)]
#         for result in as_completed(results):
#             number_set.add(result.result())
#     with open(file_name,"a") as file:
#         for number in number_set:
#             file.write(number+"\n")


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 
