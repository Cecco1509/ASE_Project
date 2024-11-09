import requests
from flask import Flask, make_response, jsonify, request
from models import GachaItem

app = Flask(__name__)

# Simulated in-memory database (dict) TODO: delete when db is ready
gacha_collection = {
    "1": GachaItem("1", "Sword of Destiny", "sword.jpg", 0.01, "A powerful sword that can cut through anything."),
    "2": GachaItem("2", "Shield of Light", "shield.jpg", 0.05, "A shield that can block any attack."),
    "3": GachaItem("3", "Staff of Power", "staff.jpg", 0.1, "A staff that can cast powerful spells."),
    "4": GachaItem("4", "Bow of Justice", "bow.jpg", 0.15, "A bow that never misses its target."),
    "5": GachaItem("5", "Armor of the Gods", "armor.jpg", 0.2, "Armor that makes the wearer invincible."),
    "6": GachaItem("6", "Ring of the Ancients", "ring.jpg", 0.25, "A ring that grants the wearer immortality.")
}

@app.route('/gacha', methods=['GET'])
def get_all_gacha_items():
    """Simulate fetching all gacha items."""
    return make_response(jsonify([item.to_dict() for item in gacha_collection.values()]), 200)

@app.route('/gacha', methods=['POST'])
def add_gacha_item():
    """Simulate adding a new gacha item."""
    json_data = request.get_json()
    if json_data:
        gacha_item = GachaItem.from_dict(json_data)
        gacha_collection[gacha_item.gacha_id] = gacha_item
        return make_response(jsonify(json_data), 200)
    return make_response(jsonify({"message": "DBManager_Gacha: Error missing JSON data"}), 400)

@app.route('/gacha/<int:gacha_id>', methods=['DELETE'])
def delete_gacha_item(gacha_id):
    """Simulate deleting a gacha item."""
    gacha_collection.pop(gacha_id, None)
    return make_response(jsonify({"message": f"DBManager_Gacha: Gacha item {gacha_id} deleted successfully"}), 200)

@app.route('/gacha/<int:gacha_id>', methods=['PATCH'])
def update_gacha_item(gacha_id):
    """Simulate updating a gacha item."""
    new_data = request.get_json()
    print(f"DBManager_Gacha: Updating gacha item {gacha_id} with data {new_data}")
    if new_data:
        item = gacha_collection[str(gacha_id)] # TODO handle KeyError
        if not item:
            return make_response(jsonify({"message": f"Error item {gacha_id} not found"}), 404)
        item.name = new_data.get("name", item.name)
        item.image = new_data.get("image", item.image)
        item.rarity_percentage = new_data.get("rarity_percentage", item.rarity_percentage)
        item.description = new_data.get("description", item.description)
        return make_response(jsonify(item.to_dict()), 200)
    return make_response(jsonify({"message": "DBManager_Gacha: Error missing JSON data"}), 400)

def create_app():
    return app