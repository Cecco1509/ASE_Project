from app import app
from app import db
import sys
sys.path.append('/app')
from models import *
from flask import Flask, request, make_response, jsonify
from sqlalchemy import func

@app.route('/gacha', methods=['GET'])
def get_all_gachas():
    gachas = db.session.execute(db.select(Gacha)).scalars()
    if gachas:
        return make_response(jsonify([gacha.to_dict() for gacha in gachas]), 200)
    return make_response(jsonify({"message":"Gachas not found"}), 404)

@app.route('/gacha/<int:gachaId>', methods=['GET'])
def get_single_gacha(gachaId):
    gacha = db.get_or_404(Gacha, gachaId)
    return make_response(jsonify(gacha.to_dict()), 200)

@app.route('/gacha/random', methods=['GET'])
def get_random_gacha():
    """Get a random gacha from the database."""
    # Use `func.newid()` for SQL Server to order by random
    gacha = db.session.execute(db.select(Gacha).order_by(func.newid()).limit(1)).scalar_one_or_none()

    if gacha:
        return make_response(jsonify(gacha.to_dict()), 200)
    return make_response(jsonify({"message": "No gachas found"}), 404)

@app.route('/gacha', methods=['POST'])
def create_gacha():
    json_data = request.get_json()
    if json_data:
        gacha = Gacha(name=json_data['name'], image=json_data['image'], rarityPercent=json_data['rarityPercent'], description=json_data['description'])
        db.session.add(gacha)
        db.session.commit()
        return make_response(jsonify({"gachaId":gacha.id}), 200)
    return make_response(jsonify({"message":"Invalid gacha data"}), 400)

@app.route('/gacha/<int:gachaId>', methods=['PUT'])
def update_gacha(gachaId):
    json_data = request.get_json()
    if json_data:
        gacha = db.get_or_404(Gacha, gachaId)
        gacha.name=json_data['name']
        gacha.image=json_data['image']
        gacha.rarityPercent=json_data['rarityPercent']
        gacha.description=json_data['description']
        gacha.verified = True
        db.session.commit()
        return make_response(jsonify({"message":"Gacha sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid gacha data"}), 400)

@app.route('/gacha/<int:gachaId>', methods=['DELETE'])
def delete_gacha(gachaId):
    gacha = db.get_or_404(Gacha, gachaId)
    db.session.delete(gacha)
    db.session.commit()
    return make_response(jsonify({"message":"Gacha sucessfully deleted."}), 200)
