from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/gachacollection', methods=['GET'])
def get_all_gachascollections():
    collections = db.session.execute(db.select(GachaCollection)).scalars()
    if collections:
        return make_response(jsonify(collections), 200)
    return make_response(jsonify({"message":"Gachas collections not found"}), 404)

@app.route('/gachacollection/<int:userId>', methods=['GET'])
def get_single_gachacollection(userId):
    collection = db.session.execute(db.select(GachaCollection).where(Gachacollection.userId==userId)).scalar()
    if collection:
        return make_response(jsonify(collection.to_dict()), 200)
    return make_response(jsonify({"message":"Gacha collection not found"}), 404)

@app.route('/gachacollection', methods=['POST'])
def create_gachacollection():
    json_data = request.get_json()
    if json_data:
        collection = GachaCollection(gachaId=json_data['gachaId'], userId=json_data['userId'], timestamp=json_data['timestamp'], source=json_data['source'])
        db.session.add(collection)
        db.session.commit()
        return make_response(jsonify(collection.id), 200)
    return make_response(jsonify({"message":"Invalid gacha collection data"}), 400)

@app.route('/gachacollection/<int:collectionId>', methods=['PUT'])
def update_gachacollection(collectionId):
    json_data = request.get_json()
    if json_data:
        collection = db.session.execute(db.select(GachaCollection).where(GachaCollection.id==gachaId)).scalar_one()
        if collection:
            collection.gachaId=json_data.gachaId
            collection.userId=json_data.userId
            collection.timestamp=json_data.timestamp
            collection.source=json_data.source
            collection.verified = True
            db.session.commit()
            return make_response(jsonify({"message":"Gacha collection sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested gacha collection does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid gacha collection data"}), 400)

@app.route('/gachacollection/<int:collectionId>', methods=['DELETE'])
def delete_gachacollection(collectionId):
    collection = db.session.execute(db.select(GachaCollection).where(GachaCollection.id==gachaId)).scalar_one()
    if collection:
            db.session.delete(collection)
            db.session.commit()
            return make_response(jsonify({"messgae":"Gacha collection sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested gacha collection does not exist"}), 404)
