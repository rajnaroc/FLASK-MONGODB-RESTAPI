from flask import Flask, request
from flask_pymongo import PyMongo



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonmongo"

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def creat_user():
    
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    print(username,password, email)

    return {"mesage":"received"}


if __name__ == "__main__":
    app.run(debug=True)