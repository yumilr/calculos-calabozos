from flask import Flask, render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import datetime
from datetime import datetime
import threading

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
app.secret_key = bytearray(b'23423423432345234')
user_session_key = 'user'

key_users = 'users'
key_messages = 'messages'
key_questions = 'questions'
key_difficulties = 'difficulties'
counter = 0

cache = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html')
    # return render_template('index.html')

"""
@app.route('/authenticate', methods=['POST'])
def authenticate():
    #msg = json.loads(request.data)
    #if msg['username'] == msg['password']:
    #    r_msg = {'msg':'Welcome'}
    #    json_msg = json.dumps(r_msg)
    #    return Response(json_msg, status=200)
    #r_msg = {'msg':'Failed'}
    #json_msg = json.dumps(r_msg)
    #return Response(json_msg, status=401)
    msg = json.loads(request.data)
    username = msg['username']
    password = msg['password']
    db_session = db.getSession(engine)
    dbResponse = db_session.query(entities.User).filter(entities.User.username == username).filter(entities.User.password == password)
    data = dbResponse[:]
    if len(data) != 0:
        r_msg = {'msg':'Welcome', 'id':data[0].id, 'username':data[0].username}
        session[user_session_key] = json.dumps(data[0], cls=connector.AlchemyEncoder)
        json_msg = json.dumps(r_msg)
        return Response(json_msg, status=200, mimetype='application/json')
    r_msg = {'msg':'Failed'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=401, mimetype='application/json')
"""

#CRUD users
@app.route('/users', methods = ['POST'])
def create_user():
    try:
        c = json.loads(request.form['values'])
    except:
        c = json.loads(request.data)
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password'],
        score=0
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    r_msg = {'msg':'UserCreated'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')
    message = {'status': 404, 'message': 'Not Found'}
    return Response(json.dumps(message), status=404, mimetype='application/json')

@app.route('/users', methods = ['GET'])
def get_users():
    data = []
    update_cache: bool = False
    max_time: int = 20

    if key_users in cache:
        update_cache = not (datetime.now() - cache[key_users]['time']).total_seconds() < max_time
        data = cache[key_users]['data']
    else:
        update_cache = True

    if update_cache:
        db_session = db.getSession(engine)
        dbResponse = db_session.query(entities.User).order_by(entities.User.id)
        db_session.close()
        data = dbResponse[:]
        cache[key_users] = {'data':data, 'time':datetime.now()}
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    db_session = db.getSession(engine)
    id = request.form['key']
    user = db_session.query(entities.User).filter(entities.User.id == id).first()

    c = json.loads(request.form['values'])

    for key in c.keys():
        setattr(user, key, c[key])

    db_session.add(user)
    db_session.commit()
    return 'Updated User'

@app.route('/users/<id>', methods = ['PUT'])
def update_user2(id):
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).first()

    c = json.loads(request.data)
    for key in c.keys():
        setattr(user, key, c[key])

    db_session.add(user)
    db_session.commit()

    message = {'msg':'User updated'}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    return Response(json_message, status=201, mimetype='application/json')


@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).one()
    db_session.delete(user)
    db_session.commit()
    return "Deleted User"

@app.route('/current', methods = ['GET'])
def current_user():
    user_json = session['current']
    return Response(user_json, status=200, mimetype='application/json')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    session.clear()
    msg = json.loads(request.data)
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.username == msg['username'], entities.User.password == msg['password']).first()
    db_session.close()
    #print(user.username)
    if user:
        session['current'] = json.dumps(user, cls = connector.AlchemyEncoder)
        r_msg = {'msg':'Welcome', 'id':user.id, 'username':user.username, 'name':user.name, 'fullname':user.fullname, 'password':user.password, 'score':user.score}
        json_msg = json.dumps(r_msg)
        session['logged_user']=user.id
        session['used_questions_id']=[]
        session['user_score']=user.score
        session['timer']=30
        return Response(json_msg, status=200, mimetype='application/json')
    r_msg = {'msg':'Failed'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=401, mimetype='application/json')

@app.route('/deauthenticate', methods=['POST'])
def deauthenticate():
    r_msg = {'msg':'Bye Bye'}
    json_msg = json.dumps(r_msg)
    session['logged_user']=''
    return Response(json_msg, status=200, mimetype='application/json');

@app.route('/difficulties',methods=['GET'])
def get_difficulty():
    data = []
    update_cache: bool = False
    max_time: int = 20

    if key_difficulties in cache:
        update_cache = not (datetime.now() - cache[key_difficulties]['time']).total_seconds() < max_time
        data = cache[key_difficulties]['data']
    else:
        update_cache = True

    if update_cache:
        db_session = db.getSession(engine)
        dbResponse = db_session.query(entities.Difficulty).order_by(entities.Difficulty.id)
        db_session.close()
        data = dbResponse[:]
        cache[key_difficulties] = {'data': data, 'time': datetime.now()}
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    diff = json.loads(request.data)
    #print(diff)
    #print(diff['difficulty_value'])
    session['selected_difficulty'] = int(diff['difficulty_value']) #html lo envía como string, casteamos

    db_session = db.getSession(engine)
    dbResponse = db_session.query(entities.Difficulty).filter(entities.Difficulty.id==session['selected_difficulty']).first()
    db_session.close()
    session["timer"] = dbResponse.time
    r_msg={'msg':'Success'}
    #print(session)
    r_msg = json.dumps(r_msg)
    return Response(r_msg, status=200, mimetype='application/json')

@app.route('/random_question', methods=['GET'])
def random_question():
    data = []
    db_session = db.getSession(engine)
    #print(session)
    #print(cache)
    used_questions=session['used_questions_id']
    question = db_session.query(entities.Question).\
        filter(entities.Question.difficulty_id==session['selected_difficulty'],
               entities.Question.id.notin_(used_questions)).first()
    if question.answer_type_id == 1:
        wrong_answers=db_session.query(entities.WrongAnswer).\
            filter(entities.WrongAnswer.question_id==question.id)
        wrong_answers=wrong_answers[:]
    else:
        wrong_answers=[]
    db_session.close()
    data = {'question':question, 'wrong_answers':wrong_answers, 'time' : session['timer']}
    session['used_questions_id']=used_questions+[question.id]
    #print(session)
    #print(data)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/random_question/<difficulty_id>', methods=['GET'])
def random_question2(difficulty_id):
    data = []
    db_session = db.getSession(engine)
    #print(session)
    used_questions=[]
    question = db_session.query(entities.Question).\
        filter(entities.Question.difficulty_id==difficulty_id,
               entities.Question.id.notin_(used_questions)).first()
    if question.answer_type_id == 1:
        wrong_answers=db_session.query(entities.WrongAnswer).\
            filter(entities.WrongAnswer.question_id==question.id)
        wrong_answers=wrong_answers[:]
    else:
        wrong_answers=[]
    db_session.close()
    data = {'question':question, 'wrong_answers':wrong_answers}
    #session['used_questions_id']=used_questions+[question.id]
    #print(session)
    #print(data)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/validate', methods=['POST'])
def validate():
    answer = json.loads(request.data)
    question_id=answer['question_id']
    answer_cont=answer['answer']
    db_session = db.getSession(engine)
    question = db_session.query(entities.Question).\
        filter(entities.Question.id==question_id).first() #obtenemos la pregunta
    if question.right_answer == answer_cont:
        session['user_score']=session['user_score']+10
        ans_msg = {'msg': 'Success','score': session['user_score']}
        user = db_session.query(entities.User).\
            filter(entities.User.id == session['logged_user']).first()
        setattr(user, 'score', session['user_score'])
        db_session.add(user)
        db_session.commit()
    else:
        ans_msg = {'msg': 'Failed'}
    db_session.close()
    r_msg = json.dumps(ans_msg)
    return Response(r_msg, status=200, mimetype='application/json')

@app.route('/user_score', methods=['GET'])
def score():
    ans_msg = {'user_score': session['user_score']}
    s_msg = json.dumps(ans_msg)
    return Response(s_msg, status=200, mimetype='application/json')



@app.route('/ranking', methods = ['GET'])
def get_ranks():
    data = []
    update_cache: bool = False
    max_time: int = 20
    db_session = db.getSession(engine)
    dbResponse = db_session.query(entities.User).order_by(entities.User.score.desc())
    db_session.close()
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


# validate -> compara con la respuesta correcta(atributo en la tabla de preguntas)
#     (PENDIENTE)         ->right: suma puntos a score en users   ->wrong: no suma,
#
# (PENDIENTE) get ranking -> select tabla usuarios y ordenarlos por score
# (PENDIENTE) log out ->
# PENDIENTE: CAMBIAR ORDEN EN QUE SE MUESTRAN LAS RESPUESTAS
# descomentar línea     #session['used_questions_id']=used_questions+[question.id],
# para que no se repita la pregunta
# (PENDIENTE) diseño


@app.route('/questions', methods = ['GET'])
def get_question():
    data = []
    update_cache: bool = False
    max_time: int = 20

    if key_questions in cache:
        update_cache = not (datetime.now() - cache[key_users]['time']).total_seconds() < max_time
        data = cache[key_questions]['data']
    else:
        update_cache = True

    if update_cache:
        db_session = db.getSession(engine)
        dbResponse = db_session.query(entities.Question)#.order_by(entities.Question.id) #no recuerdo si por defecto están ordenados
        db_session.close()
        data = dbResponse[:]
        cache[key_questions] = {'data':data, 'time':datetime.now()}
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/questions', methods = ['POST'])
def create_question():
    try:
        c = json.loads(request.form['values'])
    except:
        c = json.loads(request.data)

    question = entities.Question(
        content=c['content'],
        difficulty_id=int(c['difficulty_id']),
        answer_type_id=2,
        right_answer=c['right_answer'],
        accept_error=bool(c['accept_error']),
        margin_error=float(c['margin_error']),
    )

    session = db.getSession(engine)
    session.add(question)
    session.commit()
    r_msg = {'msg':'Question Created'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)

#maná en html -> has obtenido tanto
if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
