from flask import Flask, request, abort, jsonify
from models import db,User
from config import ApplicationConfig
from flask_bcrypt import Bcrypt
# app = flask(name) - means its just referecing the app.py file 
app = Flask(__name__)
app.config.from_object(ApplicationConfig)
# Intializing the enecryption for the password
bcrypt = Bcrypt(app)
# Initialize the application to the database 
db.init_app(app)    

with app.app_context(): 
    db.create_all()
    
@app.route("/register", methods=["POST"])
def register_user(): 
    email = request.json["email"]
    password = request.json["password"]
    # Check if user exists
    user_exists = User.query.filter_by(email=email).first() is not None
    some_user = User.query.filter_by(email=email)
    if user_exists: 
        abort(409)    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })
    
@app.route("/login" , methods=["POST"])
def login_user(): 
    email = request.json["email"]
    password = request.json["password"]
    
    user = User.query.filter_by(email=email).first()
    if user is None: 
        return jsonify({"error" : "User Doesnt Exist"},401)
    
    if not bcrypt.check_password_hash(user.password , password): 
        return jsonify({"error" : "Wrong Password"},401)
    
    return jsonify({
        "id": user.id,
        "email": user.email
    })
    
@app.route("/users", methods=["GET"])
def get_users(): 
      # Get all the queries 
    users = User.query.all()

    # Put in a data structure dictionary
    user_list = []
    for user in users:
        user_data = {
            "user": user.email,
            "id": user.id
            # Add more fields as needed
        }
    user_list.append(user_data)
    print(user_list)
    return jsonify(users=user_list)
# Run the app 
# this name == main is used to make sure the server only runs if the script is exceuted directyle from 
# a python interpreter and not used in an imported module 
if __name__ == "__main__":
    app.run(debug=True)