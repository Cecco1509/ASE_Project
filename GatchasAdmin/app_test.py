from flask import Flask, request, make_response, jsonify
from handle_errors import handle_errors

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

mock_gacha_list = [
        {
            'id': 1,
            'name': 'Gacha 1',
            'description': 'Description for Gacha 1',
            'image': 'image1.png',
            'rarityPercent': 25.9
        },
        {
            'id': 2,
            'name': 'Gacha 2',
            'description': 'Description for Gacha 2',
            'image': 'image2.png',
            'rarityPercent': 0.7
        },
        {
            'id': 3,
            'name': 'Gacha 3',
            'description': 'Description for Gacha 3',
            'image': 'image3.png',
            'rarityPercent': 57.3
        }
    ]

mock_gachacollection_list = [
        {
            'id': 1,
            'gachaId': 1,
            'userId': 1,
            'timestamp': '2021-07-01T12:00:00',
            'source': 'ROLL'
        },
        {
            'id': 2,
            'gachaId': 2,
            'userId': 1,
            'timestamp': '2021-07-01T12:01:00',
            'source': 'AUCTION'
        },
        {
            'id': 3,
            'gachaId': 3,
            'userId': 2,
            'timestamp': '2021-07-01T12:02:00',
            'source': 'ROLL'
        }
    ]


"""Fetch all gacha items."""
@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def get_all_gacha():
    """Fetch all gacha items."""
    return make_response(jsonify(mock_gacha_list), 200)

"""Fetch a single gacha item by ID."""
@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    # cbeck if gachaId is valid
    if gachaId < 1 or gachaId > len(mock_gacha_list):
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    return make_response(jsonify(mock_gacha_list[gachaId-1]), 200)

"""Create a new gacha item."""
@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    """Create a new gacha item."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, add the new gacha item to the mock list
    new_gacha = {
        'id': len(mock_gacha_list) + 1,
        'name': json_data['name'],
        'description': json_data['description'],
        'image': json_data['image'],
        'rarityPercent': json_data['rarityPercent']
    }
    mock_gacha_list.append(new_gacha)
    return make_response({"gachaId": new_gacha['id']}, 200)

def is_valid_gacha_data(data):
    """
    Validate the input JSON data for creating a gacha item.
    Checks for required fields, data types, and formats.
    """
    required_fields = {
        "name": str,
        "image": str,
        "rarityPercent": float,
        "description": str,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid type for field '{field}': Expected {expected_type.__name__}"

    # Additional validation: rarityPercent should be between 0 and 100
    if not (0 <= data["rarityPercent"] <= 100):
        return False, "Rarity percent must be a value between 0 and 1."

    return True, "Data is valid"

"""Update a gacha item."""
@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    """Update a gacha item."""
    json_data = request.get_json()

    # check if data is valid
    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)
    
    is_valid, validation_message = is_valid_gacha_data(json_data)
    if not is_valid:
        return make_response(jsonify({"message": validation_message}), 400)

    # all data is valid, update the gacha item in the mock list
    gacha_item = next((gacha for gacha in mock_gacha_list if gacha['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    
    gacha_item.update(json_data)
    return make_response({"message":"Gacha sucessfully updated."}, 200)

"""Delete a gacha item.""" 
@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
def delete_gacha(gachaId):
    """Delete a gacha item."""
    global mock_gacha_list

    # check if gachaId is valid
    gacha_item = next((gacha for gacha in mock_gacha_list if gacha['id'] == gachaId), None)
    if not gacha_item:
        return make_response(jsonify({"message": f"Gacha item with ID {gachaId} not found"}), 404)
    
    # all data is valid, delete the gacha item from the mock list
    mock_gacha_list = [gacha for gacha in mock_gacha_list if gacha['id'] != gachaId]

    return make_response({"message":"Gacha sucessfully deleted."}, 200)

"""Get all gacha collections."""
mock_get_all_gachacollections = None

@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
def get_all_gachacollections():
    """Get all gacha collections."""
    return make_response(jsonify(mock_gachacollection_list), 200)

def create_app():
    return app