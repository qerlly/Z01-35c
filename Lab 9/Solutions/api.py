import sys
import flask
from flask import request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI
from safrs import jsonapi_rpc

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
                        (msg, fromUser, toUser) 
                        VALUES (?, ?, ?);"""
    
        data_tuple = (content["message"], content["userFrom"], content["userTo"])
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
    return '''
<table border="1" bgcolor="#FFFFFF" width=100%>    
    <tr>
        <th align= "left">
            <h1>User : User description</h1>
            <h2>Represents user details.</h2>   
            <h3>User attributes:</h3>   
            <ul>
            <li>login (String): unique identifier</li>
            <li>password (String): a secret word or phrase that must be used to gain admission to a place.</li>
            </ul>
            <h2>User Collection.</h2>   
            
            <details>
                <summary><mark>List all users:</mark></summary>
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/users/all</em></p>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json</em></p>
                <p>BODY : <em>[{"login":user1, "password":1234}, {"login":user2, "password":1111}]</em></p>
            </details>
            
            <details>
                <summary><mark>Retrieve user:</mark></summary> 
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/users?login={login}</em></p>
                <p>Parameters : <em>login</em> - unique identifie</p>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json, X-My-Header:The Value</em></p>
                <p>BODY : <em>{"login":user3, "password":33333}</em></p>
            </details>
            
            <details>
                <summary><mark>Create new user:</mark></summary>
                <p>PUT http://127.0.0.1:5000/api/v1/resources/users/add/{login}</p>
                <p>Parameters : <em>login</em> - unique identifie</p>
                <p>Response : <em>201</em></p>
                <p>HEADERS : <em>Content-Type:application/json</em></p>
                <p>BODY : <em>{"login":user, "password":1234}</em></p>
            </details>
        </th>
        
        <th align= "left">
            <h1>Message : Message description</h1>
            <h2>Represents message details.</h2>   
            <h3>Message attributes:</h3>   
            <ul>
            <li>message (String): text from one user to another</li>
            <li>userFrom (String): unique identifier first user</li>
            <li>userTo (String): unique identifier second user</li>
            </ul>
            <h2>Message Collection.</h2>   
            
            <details>
                <summary><mark>List all messages:</mark></summary>
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/messages/all</em></p>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json</em></p>
                <p>BODY : <em>[{"message":hi, "userFrom":user1, "userTo":user2}, {"message":hello, "userFrom":user2, "userTo":user1}]</em></p>
            </details>
            
            <details>
                <summary><mark>Retrieve message to user:</mark></summary> 
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/messages/to?userTo={login}</em></p>
                <p>Parameters : <em>login</em> - unique identifie</p>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json, X-My-Header:The Value</em></p>
                <p>BODY : <em>[{"message":hi, "userFrom":user1, "userTo":user2}, {"message":hello, "userFrom":admin, "userTo":user2}]</em></p>
            </details>
            
            
            <details>
                <summary><mark>Retrieve message from user:</mark></summary> 
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/messages/from?userFrom={login}</em></p>
                <p>Parameters : <em>login</em> - unique identifie</p>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json, X-My-Header:The Value</em></p>
                <p>BODY : <em>[{"message":hi, "userFrom":user1, "userTo":user2}, {"message":hello, "userFrom":user1, "userTo":user2}]</em></p>
            </details>
            
            <details>
               <summary><mark>Retrieve message from user to another user:</mark></summary> 
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/messages/users?userFrom={loginFrom}&userTo={loginTo}</em></p>
                <p>Parameters : </p>
                 <ul>
                    <li><em>loginFrom</em>: unique identifier user1</li>
                    <li><em>loginTo</em>: unique identifier user2</li>
                </ul>
                <p>Response : <em>200</em></p>
                <p>HEADERS : <em>Content-Type:application/json, X-My-Header:The Value</em></p>
                <p>BODY : <em>[{"message":hi, "userFrom":user1, "userTo":user2}, {"message":hello, "userFrom":user1, "userTo":user2}]</em></p>
            </details>
            
            <details>
                <summary><mark>Create new message:</mark></summary>
                <p>PUT http://127.0.0.1:5000/api/v1/resources/messages/{loginFrom}/add/{loginTo}</p>
                <p>Parameters : </p>
                 <ul>
                    <li><em>loginFrom</em>: unique identifier user1</li>
                    <li><em>loginTo</em>: unique identifier user2</li>
                </ul>
                <p>Response : <em>201</em></p>
                <p>HEADERS : <em>Content-Type:application/json</em></p>
                <p>BODY : <em>{"message":hi, "userFrom":user1, "userTo":user2}</em></p>
            </details>
        </th>
    </tr>
</table>
'''


@app.route('/api/v1/resources/users/add/<login>', methods=['GET', 'POST'])
def add_user(login):
    content = request.json
    try:
        sqliteConnection = sqlite3.connect('sqlite.db')
        cursor = sqliteConnection.cursor()
        
        sqlite_insert_with_param = """INSERT INTO users
                        (login, password) 
                        VALUES (?, ?);"""
    
        data_tuple = (content["login"], content["password"])
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


if __name__ == "__main__":
    app.run(host=host)   