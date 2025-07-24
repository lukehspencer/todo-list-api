# Flask app

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import create_access_token, jwt_required
from models import db, bcrypt, jwt, UserModel, TodoModel

app = Flask(__name__) # creates Flask object
api = Api(app) # initializes an api within a Flaks application
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # change configuration settings (define where database will exist)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Key"

bcrypt.init_app(app) # initialize Bcrypt in app
jwt.init_app(app) # initialize JWTManager in app
db.init_app(app) # initialize database in app

#with app.app_context(): # run when you want to recreate the ENTIRE database
    #db.create_all()

class Register(Resource): # register a user (inherits http methods from Resource class)
    def post(self): # adds user to database
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="Username of user is required", required=True) # extract username from json data in request
        parser.add_argument("password", type=str, help="Password of user is required", required=True) # extract password from json data in request
        args = parser.parse_args() # parses username and password into a dictionary

        user = UserModel.query.filter_by(username=args["username"]).first() #searches the database for a user with the username that was specified in the request
        if user:
            abort(401, message=f"User with name {args["username"]} and password {args["password"]} already exists")

        user = UserModel(username=args["username"], password=args["password"]) # creates a new user
        db.session.add(user) # adds user to database
        db.session.commit() # saves changes

        return {"username": args["username"], "password": args["password"]}, 201

api.add_resource(Register, "/register") # adds a new endpoint to the flask api

class Login(Resource): # login user (inherits http methods from Resource class)
    def post(self): # check if user is in database
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="Username of user is required", required=True)
        parser.add_argument("password", type=str, help="Password of user is required", required=True)
        args = parser.parse_args()

        user = UserModel.query.filter_by(username=args["username"]).first()
        if not user:
            abort(401, message=f"Invalid username")
        if not user.check_password(args["password"]):
            abort(401, message="Invalid password")
        
        token = create_access_token(identity=str(user.uid)) # creates a token
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(key="access_token", value=token, httponly=True, secure=True) # stores the token in a cookie (used to automatically login user)
        return response
        
api.add_resource(Login, "/login") # adds a new endpoint to the flask api

resourceFields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
}

nestedFields = {
    "data": fields.Nested(resourceFields),
    "page": fields.Integer,
    "limit": fields.Integer,
    "total": fields.Integer
}

class TodoList(Resource): # get, create, and delete a todo task (inherits http methods from Resource class)
    @marshal_with(nestedFields) # automatically formats (serializes) the response into json
    @jwt_required() # checks if token is in the request body (checks to see if user successfully logged in and received an access token)
    def get(self): # get all tasks
        tasks = TodoModel.query.all() # obtains all tasks in the database
        if not tasks:
            abort(404, message="Tasks cannot be found...")
        
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        paginate = TodoModel.query.paginate(page=page)
        total = paginate.total
        totalData = {"data": tasks, "page": page, "limit": limit, "total": total}

        return totalData
    
    @marshal_with(resourceFields)
    @jwt_required()
    def post(self): # create a task
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, help="Todo task title is required", required=True)
        parser.add_argument("description", type=str, help="Description is required", required=True)
        args = parser.parse_args()

        task = TodoModel(title=args["title"], description=args["description"])
        db.session.add(task)
        db.session.commit()

        return task, 201
    
    @jwt_required()
    def delete(self): # delete all tasks
        tasks = TodoModel.query.all()
        if not tasks:
            abort(404, message="Tasks cannot be found...")
        
        TodoModel.query.delete()
        db.session.commit()

        return "", 204
    
api.add_resource(TodoList, "/todos") # adds a new endpoint to the flask api

class TodoListByID(Resource): # get, update, and delete a specific task by ID (inherits http methods from Resource class)
    @marshal_with(resourceFields)
    @jwt_required()
    def get(self, taskID): # get a task with ID=taskID
        result = TodoModel.query.filter_by(id=taskID).first()
        if not result:
            abort(404, message="Task cannot be found...")
        
        return result
        
    @marshal_with(resourceFields)
    @jwt_required()
    def patch(self, taskID): #update a task with ID=taskID
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, help="Todo task title is required", required=True)
        parser.add_argument("description", type=str, help="Description is required", required=True)
        args = parser.parse_args()
        
        result = TodoModel.query.filter_by(id=taskID).first() # filters todo tasks by a certain ID
        if not result:
            abort(404, message="Task cannot be found...")
        
        if args["title"]: # checks if the user wants to change the title of the task
            result.title = args["title"]
        if args["description"]: # checks if the user wants to change the description of the task
            result.description = args["description"]

        db.session.commit()

        return result
    
    @jwt_required()
    def delete(self, taskID): # delete a task with ID=taskID
        result = TodoModel.query.filter_by(id=taskID).first()
        if not result:
            abort(404, message="Task cannot be found...")
        
        TodoModel.query.filter_by(id=taskID).delete()
        
        tasks = TodoModel.query.all()
        for task in tasks:
            if task.id>taskID:
                task.id-=1

        db.session.commit()

        return "", 204
        
api.add_resource(TodoListByID, "/todos/<int:taskID>") # adds a new endpoint to the flask api (requires an int paramater like /todos/1)

if __name__ == "__main__":
    app.run(debug=True) # runs app