from flask import Flask, make_response, jsonify
import app as main_app

flask_app = main_app.app

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

def get_all_gacha_mock():
    return make_response(jsonify(mock_gacha_list), 200)