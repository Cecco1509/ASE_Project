from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify






@app.route('/user', methods=['GET'])
def get_all_users():
    users = db.session.execute(db.select(User)).scalars()
    if users:
        return make_response(jsonify([user.to_dict() for user in users]), 200)
    return make_response(jsonify({"message":"Users not found"}), 404)





@app.route('/user/auth/<int:accountId>', methods=['GET'])
def get_user_by_authId(accountId):
    user = db.session.execute(db.select(User).where(User.authId==accountId)).scalar_one()
    if user:
        return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"message":"User not found"}), 404)




@app.route('/user/<int:userId>', methods=['GET'])
def get_single_user(userId):
    user = db.get_or_404(User,userId)
    if user:
        return make_response(jsonify(user.to_dict()), 200)
    return make_response(jsonify({"message":"User not found"}), 404)

@app.route('/user', methods=['POST'])
def create_user():
    json_data = request.get_json()
    if json_data:
        user = User(authId=json_data['authId'], profilePicture=json_data['profilePicture'], ingameCurrency=json_data['ingameCurrency'],registrationDate=json_data['registrationDate'], status=UserStatus[json_data['status']])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"userId":user.id}), 200)
    return make_response(jsonify({"message":"Invalid user data"}), 400)

@app.route('/user/<int:userId>', methods=['PUT'])
def update_user(userId):
    json_data = request.get_json()
    if json_data:
        user = db.get_or_404(User, userId)
        user.ingameCurrency=json_data['ingameCurrency']
        user.profilePicture=json_data['profilePicture']
        user.status=json_data['status']
        user.verified = True
        db.session.commit()
        return make_response(jsonify({"messgae":"User sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid user data"}), 400)

@app.route('/user/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    user = db.get_or_404(User, userId)
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({"messgae":"User sucessfully deleted."}), 200)

@app.route('/user/<int:userId>', methods=['PATCH'])
def patch_user(userId):
    json_data = request.get_json()
    if json_data:
        user = db.get_or_404(User, userId)
        if 'ingameCurrency' in json_data:
            res = db.session.query(User.ingameCurrency).with_for_update().filter_by(id=userId).first()
            money = float(res[0])
            amount = float(json_data['ingameCurrency'])
            if money + amount > 0:
                print("(", money, " + (",amount,") = ", money + amount, flush=True)
                user.ingameCurrency = money + amount
            else:
                return make_response(jsonify({"message":"Not enough money"}), 400)
        if 'profilePicture' in json_data:
            user.profilePicture = json_data['profilePicture']
        if 'status' in json_data:
            user.status = json_data['status']
        db.session.commit()
        return make_response(jsonify({"messgae":"User sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid user data"}), 400)