import flask
from flask import request, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config["DEBUG"] = True

messages = []

@app.route('/api/v1/resources/messages/all', methods=['GET'])
def api_messages():
    return jsonify(messages)
    

@app.route('/api/v1/resources/messages/<loginFrom>/add/<login>', methods=['GET', 'POST'])
def add_message(loginFrom, login):   
    content = request.json
    print(content['message'])
    messages.append(content)
    return jsonify({"login":login})
    

@app.route('/api/v1/resources/messages/users', methods=['GET'])
def api_all_messages_for_to_user_filter():
    if 'userFrom' in request.args:
        user1 = str(request.args['userFrom'])
    else:
        return "Error: No users fields provided. Please specify an users."
    if 'userTo' in request.args:
        user2 = str(request.args['userTo'])
    else:
        return "Error: No users fields provided. Please specify an users."
        
    results = []
    indexes = []
    i = 0
    
    for msg in messages:
        if msg['userFrom'] == user1 and msg['userTo'] == user2:
            results.append(msg)
            indexes.append(i)
        i += 1
    
    indexes.reverse()
    for index in indexes:
        del messages[index]
        
    return jsonify(results)
    
 
@app.route('/api/v1/resources/messages/to', methods=['GET'])
def api_all_messages_for_user_filter():
    if 'userTo' in request.args:
        user1 = str(request.args['userTo'])
    else:
        return "Error: No users fields provided. Please specify an users."
    
    results = []

    for msg in messages:
        if msg['userTo'] == user1:
            results.append(msg)

    return jsonify(results)
    

@app.route('/api/v1/resources/messages/from', methods=['GET'])
def api_all_messages_from_user_filter():
    if 'userFrom' in request.args:
        user1 = str(request.args['userFrom'])
    else:
        return "Error: No users fields provided. Please specify an users."
    
    results = []

    for msg in messages:
        if msg['userFrom'] == user1:
            results.append(msg)

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
                <p><em><b>GET</b> http://127.0.0.1:5000/api/v1/resources/api/v1/resources/users/all</em></p>
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

app.run()