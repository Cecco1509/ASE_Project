from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

def get_all_admins():
    admins = db.session.execute(db.select(Admin)).scalars()
    if admins:
        return jsonify([admin.to_dict() for admin in admins])
    return jsonify({"message":"Admin not found"})

def get_single_admin(adminId):
    admin = db.session.execute(db.select(Admin).where(Admin.id==adminId)).scalar_one()
    if admin:
        return jsonify(admin.to_dict())
    retun None

def get_admin_by_username(username):
    admin = db.session.execute(db.select(Admin).where(Admin.username==username)).scalar_one()
    if admin:
        return jsonify(admin.to_dict())
    return jsonify({"message":"Admin not found"})

def create_admin(json_data):
    if json_data:
        admin = Admin(username=json_data['username'], password=json_data['password'])
        db.session.add(admin)
        db.session.commit()
        return jsonify({"adminId":admin.id})
    return None

def update_admin(adminId, json_data):
    if json_data:
        admin = get_single_admin(adminId)
        if admin == None:
            return None
        admin.username=json_data['username']
        admin.password=json_data['password']
        admin.verified = True
        db.session.commit()
        return jsonify({"message":"Admin sucessfully updated."})
    return jsonify({"message":"Invalid admin data"})

def delete_admin(adminId):
    admin = get_single_admin
    if admin == None:
        return None
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"messgae":"Admin sucessfully deleted."})
