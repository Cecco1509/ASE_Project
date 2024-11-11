from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/admin', methods=['GET'])
def get_all_admins():
    admin = db.session.execute(db.select(Admin)).scalars()
    if admin:
        return make_response(jsonify(admin), 200)
    return make_response(jsonify({"message":"Admin not found"}), 404)

@app.route('/admin/<int:adminId>', methods=['GET'])
def get_single_admin(adminId):
    admin = db.session.execute(db.select(Admin).where(Admin.id==adminId)).scalar()
    if admin:
        return make_response(jsonify(admin.to_dict()), 200)
    return make_response(jsonify({"message":"Admin not found"}), 404)

@app.route('/admin', methods=['POST'])
def create_admin():
    json_data = request.get_json()
    if json_data:
        admin = Admin(username=json_data['username'], password=json_data['password'])
        db.session.add(admin)
        db.session.commit()
        return make_response(jsonify(admin.id), 200)
    return make_response(jsonify({"message":"Invalid admin data"}), 400)

@app.route('/admin/<int:adminId>', methods=['PUT'])
def update_admin(adminId):
    json_data = request.get_json()
    if json_data:
        admin = db.session.execute(db.select(Admin).where(Admin.id==AdminId)).scalar_one()
        if admin:
            admin.username=json_data.username
            admin.password=json_data.password
            admin.verified = True
            db.session.commit()
            return make_response(jsonify({"message":"Admin sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested admin does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid admin data"}), 400)

@app.route('/admin/<int:adminId>', methods=['DELETE'])
def delete_admin(adminId):
    admin = db.session.execute(db.select(Admin).where(Admin.id==adminId)).scalar_one()
    if admin:
            db.session.delete(admin)
            db.session.commit()
            return make_response(jsonify({"messgae":"Admin sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested admin does not exist"}), 404)
