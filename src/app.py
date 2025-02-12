from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util,ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonmongo"

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def creat_user():
    
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "email": email
            }
        )
        response = {
            "id":str(id),
            "username": username,
            "password": hashed_password,
            "email": email
        }
        return response
    else:
        return not_found(), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    reponse = json_util.dumps(users)

    return Response(reponse, mimetype='application/json')


@app.route('/user/<id>', methods=["GET"])
def get_oneUser(id):
    users = mongo.db.users.find({"_id": ObjectId(id)})
    reponse = json_util.dumps(users)

    return Response(reponse, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    users = mongo.db.users.delete_one({"_id": ObjectId(id)})
    response = jsonify({
        'message' : 'User ' + id + 'Delete succesfully'
    })
    response.status_code = 200 
    return response


@app.route('/user/<id>', methods=["PUT"])
def update_user(id):

    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and password and email and id:
        hashed_password =  generate_password_hash(password)

        mongo.db.update_one({'_id': ObjectId(id)},
        {'$set':{
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'User ' + id + 'Update Successfully'})

        response.status_code = 200
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        "message" : "Resouce not found " + request.url,
        "status": 404
    }
    return message


if __name__ == "__main__":
    app.run(debug=True)