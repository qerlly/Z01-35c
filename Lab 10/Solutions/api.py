import sys
import flask
from flask import request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI
from safrs import jsonapi_rpc
from flask_socketio import SocketIO, emit

db = SQLAlchemy()

class User(SAFRSBase, db.Model):
    """
        description: User description
    """
    __tablename__ = "users"
    login = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, default="1111")
    
    @jsonapi_rpc(http_methods=['POST','GET'])
    def addMessage(self, message, userFrom, userTo):
        '''
            description : Send a message to user
            args:
                message:
                    type : string 
                    example : Hello
                userFrom:
                    type : string 
                    example : user1
                userTo:
                    type : string 
                    example : user2
        '''
        content = 'Message to {} : {}\n'.format(self.login, userTo)
        return { 'result' : 'sent {}'.format(content)}
    
    @jsonapi_rpc(http_methods=['POST','GET'])
    def addUser(self, login, password):
        '''
            description : Register a new user
            args:
                login:
                    type : string 
                    example : user1
                password:
                    type : string 
                    example : 142aa
        '''
        content = 'New user {} : {}\n'.format(self.login, login)
        return { 'result' : 'sent {}'.format(content)}

class Message(SAFRSBase, db.Model):
    """
        description: Message description
    """
    __tablename__ = "messages"
    id = db.Column(db.String, primary_key=True)
    message = db.Column(db.String, default="hi")
    userFrom = db.Column(db.String, default="user1")
    userTo = db.Column(db.String, default="user2")
    
    @jsonapi_rpc(http_methods=['GET'])
    def getMessageFromUser(self, userFrom, userTo):
        """
            description : Get message from user
            args:
                userFrom:
                    type : string 
                    example : user1
                userTo:
                    type : string 
                    example : user2
        """
        content = 'Message {} : {}\n'.format(self.login, userTo)
        return { 'result' : 'sent {}'.format(content)}
    
class Online(SAFRSBase, db.Model):
    """
        description: Online description
    """
    __tablename__ = "online"
    id = db.Column(db.String, primary_key=True)
    login = db.Column(db.String, default="user1")
    czas = db.Column(db.String, default="12/20/2020 16:30")

def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(User)
    api.expose_object(Message)
    api.expose_object(Online)
    print("Created API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))

def create_app(config_filename=None, host="localhost"):
    app = flask.Flask(__name__)
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")
    db.init_app(app)

    with app.app_context():
        db.create_all()
        for i in range(200):
            user = User(login=f"user{i}", password=f"12412{i}")
            message = Message(message=f"test msg {i}", userFrom=f"user{i}", userTo=f"user{i+1}")
            online = Online(login=f"user{i}", czas=f"12/20/2020 16:20:{i}")

        create_api(app, host)
    
    return app

host = sys.argv[1] if sys.argv[1:] else "127.0.0.1"
app = create_app(host=host)
socketio = SocketIO(app)

@app.route('/api/v1/resources/users/online/all', methods=['GET'])
def api_online_all():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_msg = cur.execute('SELECT * FROM online;').fetchall()
    return jsonify(all_msg)
    

@app.route('/api/v1/resources/users/online/delete/<login>', methods=['DELETE'])
def delete_user_online(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sql = "DELETE FROM online WHERE login = '" + content["login"] + "'"
        
        cursor.execute(sql)
        sqliteConnection.commit()    
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})

@app.route('/api/v1/resources/users/online/add/<login>', methods=['GET', 'POST'])
def add_user_online(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sqlite_insert_with_param = """INSERT INTO online
                        (login, czas) 
                        VALUES (?, ?);"""
    
        data_tuple = (content["login"], content["czas"])
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()    
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})
    
    
@app.route('/api/v1/resources/messages/all', methods=['GET'])
def api_messages():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_msg = cur.execute('SELECT * FROM messages;').fetchall()
    return jsonify(all_msg)
    

@app.route('/api/v1/resources/messages/<loginFrom>/add/<login>', methods=['GET', 'POST'])
def add_message(loginFrom, login): 
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sqlite_insert_with_param = """INSERT INTO messages
                        (msg, fromUser, toUser, datatime, status) 
                        VALUES (?, ?, ?, ?, ?);"""
        
        socketio.emit('message')        

        data_tuple = (content["message"], content["userFrom"], content["userTo"], content["datetime"], content["status"])
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()    
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})
    
    
@app.route('/api/v1/resources/messages/read/<login>', methods=['GET', 'POST'])
def read_msg(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sql = "UPDATE messages SET status = '" + content["status"] + "' WHERE datatime = '" + content["datatime"] + "'"
        cursor.execute(sql)
        sqliteConnection.commit()    
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})
     

@app.route('/api/v1/resources/messages/users', methods=['GET'])
def api_all_messages_for_to_user_filter():
    query_parameters = request.args

    uFrom = query_parameters.get('userFrom')
    uTo = query_parameters.get('userTo')

    query = "SELECT * FROM messages WHERE"
    to_filter = []

    if uFrom:
        query += ' fromUser=? AND'
        to_filter.append(uFrom)
    if uTo:
        query += ' toUser=? AND'
        to_filter.append(uTo)
    if not (uFrom or published):
        return page_not_found(404)

    query = query[:-4] + ';'
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)
    
 
@app.route('/api/v1/resources/messages/to', methods=['GET'])
def api_all_messages_for_user_filter():
    query_parameters = request.args

    Uto = query_parameters.get('userTo')

    query = "SELECT * FROM messages WHERE"
    to_filter = []

    if Uto:
        query += ' toUser=? AND'
        to_filter.append(Uto)
    if not (Uto or published):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)
    

@app.route('/api/v1/resources/messages/from', methods=['GET'])
def api_all_messages_from_user_filter():
    query_parameters = request.args

    Ufrom = query_parameters.get('userFrom')

    query = "SELECT * FROM messages WHERE"
    to_filter = []

    if Ufrom:
        query += ' fromUser=? AND'
        to_filter.append(Ufrom)
    if not (Ufrom or published):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return ''''''


@app.route('/api/v1/resources/users/add/<login>', methods=['GET', 'POST'])
def add_user(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sqlite_insert_with_param = """INSERT INTO users
                        (login, password, status) 
                        VALUES (?, ?, ?);"""
        socketio.emit('login')        

        data_tuple = (content["login"], content["password"], content["status"])
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()   
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})
    

@app.route('/api/v1/resources/users/login/<login>', methods=['GET', 'POST'])
def login_user(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sql = "UPDATE users SET status = '" + content["status"] + "' WHERE login = '" + content["login"] + "'"
        socketio.emit('login')

        cursor.execute(sql)
        sqliteConnection.commit()    
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return jsonify({"login":login})


@app.route('/api/v1/resources/users/all', methods=['GET'])
def api_users_all():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM users;').fetchall()

    return jsonify(all_users)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/users', methods=['GET'])
def api_users_filter():
    query_parameters = request.args

    login = query_parameters.get('login')
    password = query_parameters.get('password')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if login:
        query += ' login=? AND'
        to_filter.append(login)
    if password:
        query += ' password=? AND'
        to_filter.append(password)
    if not (login or published):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    
if __name__ == "__main__":
    socketio.run(app)