from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/admin', methods=['GET'])
def get_all_admins():
    admins = db.session.execute(db.select(Admin)).scalars()
    if admins:
        return make_response(jsonify([admin.to_dict() for admin in admins]), 200)
    return make_response(jsonify({"message":"Admin not found"}), 404)

@app.route('/admin/<int:adminId>', methods=['GET'])
def get_single_admin(adminId):
    admin = db.get_or_404(Admin, adminId)
    return make_response(jsonify(admin.to_dict()), 200)

@app.route('/admin', methods=['POST'])
def create_admin():
    json_data = request.get_json()
    if json_data:
        admin = Admin(username=json_data['username'], password=json_data['password'])
        db.session.add(admin)
        db.session.commit()
        return make_response(jsonify({"adminId":admin.id}), 200)
    return make_response(jsonify({"message":"Invalid admin data"}), 400)

@app.route('/admin/<int:adminId>', methods=['PUT'])
def update_admin(adminId):
    json_data = request.get_json()
    if json_data:
        admin = db.get_or_404(Admin, adminId)
        admin.username=json_data['username']
        admin.password=json_data['password']
        admin.verified = True
        db.session.commit()
        return make_response(jsonify({"message":"Admin sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid admin data"}), 400)

@app.route('/admin/<int:adminId>', methods=['DELETE'])
def delete_admin(adminId):
    admin = db.get_or_404(Admin, adminId)
    db.session.delete(admin)
    db.session.commit()
    return make_response(jsonify({"messgae":"Admin sucessfully deleted."}), 200)
