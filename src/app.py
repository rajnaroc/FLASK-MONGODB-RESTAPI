from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash


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
        mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "email": email
            }
        )
        response = {
            "id": str(id),
            "username": username,
            "password": hashed_password,
            "email": email
        }
        return response
    else:
        return {"message" :"Faltan datos!"}

if __name__ == "__main__":
    app.run(debug=True)