from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from db.models import Client

def login(request):
    username = request.json.get('username')
    password = request.json.get('password')

    user = Client.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid username or password'}), 401

    access_token = user.generate_access_token()

    return jsonify({'access_token': access_token})

def register():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')

    user = Client(username=username, password=generate_password_hash(password), name=name)
    user.save()

    access_token = user.generate_access_token()

    return jsonify({'access_token': access_token}), 201
