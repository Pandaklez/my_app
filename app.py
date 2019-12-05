from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'  # имя таблицы
    id = db.Column(db.Integer, primary_key=True)  # имя колонки = специальный тип (тип данных, первичный ключ)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)

# here frontend starts

@app.route('/')
def question_page():
    questions = Questions.query.all() # имя_таблицы.query.взять_все()
    tmp = "test something"
    return render_template(
        'questions.html',
        questions=questions,
        tmp=tmp
    )

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')

    user = User(
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    answer = Answers(id=user.id, q1=q1, q2=q2)
    db.session.add(answer)
    db.session.commit()
    return render_template('process.html')

if __name__ == "__main__":
    app.run(debug=True)
