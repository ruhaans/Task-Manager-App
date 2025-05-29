from flask import request, jsonify
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, Category
from datetime import datetime


@app.route('/register', methods=['POST'])
def register():
    data=request.get_json()

    username=data.get('username')
    email=data.get('email')
    password=data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Please fill all the details"}), 400
    
    if User.query.filter((User.username == username) | (User.email==email)).first():
        return jsonify({"error": "Username or email already exists"}), 409
    
    hashed_password=generate_password_hash(password)

    new_user=User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered succesfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data= request.get_json()

    email= data.get('email')
    password=data.get('password')

    if not email or not password:
        return jsonify({"error": "Please enter details"}), 400
    
    user= User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify ({"error": "Please enter valid email or password."}), 401


    access_token = create_access_token(identity=str(user.id))

    return jsonify(
        {
            "message": "Login Succesfull",
            "access token": access_token
        }
    ), 200


@app.route('/tasks', methods=['POST'])
@jwt_required()
def tasks():
    current_user_id= get_jwt_identity()
    data= request.get_json()

    title= data.get("title")
    description= data.get('description')
    due_date_str= data.get('due_date')
    category_id= data.get('category_id')

    if not title:
        return jsonify({"error": "title is required."}), 400
    
    due_date=None
    if due_date_str:
        try:
            due_date= datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except(ValueError):
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if category_id:
        category= Category.query.get(category_id)
        if not category:
            return jsonify ({"error": "category not found."})
        
    new_task=Task(
        title=title,
        description=description,
        due_date=due_date,
        user_id=current_user_id,
        category_id=category_id
    ) 

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"}), 201   


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id=get_jwt_identity()

    tasks= Task.query.filter_by(user_id=current_user_id).all()

    task_list=[]
    for task in tasks:
        task_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            "completed": task.is_completed 

        })

    return jsonify(task_list), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"error": "Task not found or not authorized"}), 404

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'due_date' in data:
        try:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    if 'completed' in data:
        task.is_completed = data['completed']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({"error": "Category not found"}), 404
        task.category_id = data['category_id']

    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"error": "Task not found or not authorized"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200
