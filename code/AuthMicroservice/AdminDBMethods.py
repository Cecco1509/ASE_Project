from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

def get_all_admins():
    admins = db.session.execute(db.select(Admin)).scalars()
    if admins:
        return [admin.to_dict() for admin in admins]
    return {"message":"Admin not found"}

def get_single_admin(adminId):
    try:
        admin = db.session.execute(db.select(Admin).where(Admin.id==adminId)).scalar_one()
        return admin.to_dict()
    except:
        return None

def get_admin_by_username(username):
    try:
        admin = db.session.execute(db.select(Admin).where(Admin.username==username)).scalar_one()
        return admin.to_dict()
    except:
        return None

def create_admin(json_data):
    if json_data:
        admin = Admin(username=json_data['username'], password=json_data['password'], salt=json_data['salt'])
        db.session.add(admin)
        db.session.commit()
        return {"adminId":admin.id}
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
        return {"message":"Admin sucessfully updated."}
    return None

def delete_admin(adminId):
    admin = get_single_admin()
    if admin == None:
        return None
    db.session.delete(admin)
    db.session.commit()
    return{"message":"Admin sucessfully deleted."}
