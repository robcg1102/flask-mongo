from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pyreact' # Usa la URI de MongoDB en string para conectar tu DB
mongo = PyMongo(app)

CORS(app)

dbUsers = mongo.db.users

@app.route('/')
def method_name():
    return '<h1 style="text-align: center">Bienvenido</h1>'

# ! GET_ALL Todos los usuarios

@app.route('/users', methods=["GET"])
def getUsers():
    users = []
    for user in dbUsers.find():
        users.append({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })

    return jsonify(users)

# ! GET_ONE Un usuario

@app.route('/users/<id>', methods=["GET"])
def getUser(id):
    user = dbUsers.find_one({"_id": ObjectId(id)})
    
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

# ! CREATE_ONE Crear un usuario

@app.route('/users', methods=["POST"])
def createUser():
    id = dbUsers.insert_one({
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    }).inserted_id
    
    return jsonify(str(ObjectId(id)))

# ! UPDATE_ONE Actualizar un usuario

@app.route('/users/<id>', methods=["PUT"])
def updateUser(id):
    dbUsers.update_one({"_id": ObjectId(id)}, {"$set" :{
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    }})
    return jsonify({
        'status': 'User with id: ' + id + ' updated succesfully'
    })

# ! DELETE_ONE Eliminar un usuario

@app.route('/users/<id>', methods=["DELETE"])
def deleteUser(id):
    dbUsers.delete_one({"_id": ObjectId(id)})
    return jsonify({
        'status': 'User with id: ' + id + ' deleted succesfully'
    })

if __name__ == '__main__':
    app.run(debug=True)