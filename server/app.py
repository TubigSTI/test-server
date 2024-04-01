from flask import Flask, request, abort, jsonify, session
from models import db,User
from config import ApplicationConfig
from flask_session import Session
from flask_cors import CORS,cross_origin
from flask_bcrypt import Bcrypt
# app = flask(name) - means its just referecing the app.py file 
app = Flask(__name__)
app.config.from_object(ApplicationConfig)
# Intializing the enecryption for the password
bcrypt = Bcrypt(app)
# Allowing Cross Origin 
CORS(app, supports_credentials=True)
# Initialize the application to the database 
db.init_app(app)    
# Intializing Server Session in App 
server_sesion = Session(app)

with app.app_context(): 
    db.create_all()
    
# Managing Session cookie

@app.route("/@me")
def get_current_user(): 
    user_id = session.get("user_id")
    
    if not user_id:
        return jsonify({"error": "unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
        
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route("/register", methods=["POST"])
def register_user(): 
    email = request.json["email"]
    password = request.json["password"]
    # Check if user exists
    user_exists = User.query.filter_by(email=email).first() is not None
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
    # checks if the users DOESNT exist, returns 401 error 
    if user is None: 
        return jsonify({"error" : "User Doesnt Exist"},401)
    # If the user exist but the password doesnt match, return 401 error 
    if not bcrypt.check_password_hash(user.password , password): 
        return jsonify({"error" : "Wrong Password"},401)
    # Creating a session cookie everytime user logsin 
    session["user_id"] = user.id
    
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
    # Loop through the queries and get user and id only
    for user in users:
        # Create object for the user and id details 
        user_data = {
            "user": user.email,
            "id": user.id
            # Add more fields as needed
        }
        # push or append the user item to the empty array 
        user_list.append(user_data)
    # print all the user
    print(user_list)
    return jsonify(users=user_list)

@app.route ("/delete", methods=["DELETE"])
def delete_users(): 
    # Get all the user queries
    users = User.query.all()
    # Delete all the users 
    for user in users: 
          db.session.delete(user)
    # Commit Session 
    db.session.commit()

# Run the app 
# this name == main is used to make sure the server only runs if the script is exceuted directyle from 
# a python interpreter and not used in an imported module 
if __name__ == "__main__":
    app.run(debug=True)