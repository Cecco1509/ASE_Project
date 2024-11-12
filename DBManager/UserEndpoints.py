from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify
from enums import UserStatus

@app.route('/user', methods=['GET'])
def get_all_users():
    users = db.session.execute(db.select(User)).scalars()
    if users:
        return make_response(jsonify(users), 200)
    return make_response(jsonify({"message":"Users not found"}), 404)

@app.route('/user/<int:userId>', methods=['GET'])
def get_single_user(userId):
    user = db.session.execute(db.select(User).where(User.id==userId)).scalar()
    if user:
        return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"message":"User not found"}), 404)

@app.route('/user', methods=['POST'])
def create_user():
    json_data = request.get_json()
    if json_data:
        user = User(authId=json_data['authId'], profilePicture=json_data['profilePicture'], ingameCurrency=json_data['ingameCurrency'],registrationDate=json_data['registrationDate'], status=json_data['status'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify(user.id), 200)
    return make_response(jsonify({"message":"Invalid user data"}), 400)

@app.route('/user/<int:userId>', methods=['PUT'])
def update_user(userId):
    json_data = request.get_json()
    if json_data:
        user = db.session.execute(db.select(User).where(User.id==userId)).scalar_one()
        if user:
            user.ingameCurrency=json_data['ingameCurrency']
            user.profilePicture=json_data['profilePicture']
            user.status=json_data['status']
            user.verified = True
            db.session.commit()
            return make_response(jsonify({"messgae":"User sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested user does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid user data"}), 400)

@app.route('/user/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    user = db.session.execute(db.select(user).where(User.id==userId)).scalar_one()
    if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"messgae":"User sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested user does not exist"}), 404)
