ROLL_PRICE = 100

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

mock_gacha_collection_list = [
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

mock_user_list = [
        {
            'id': 1,
            'authId': 101,
            'ingameCurrency': 1500.0,
            'profilePicture': 'profile1.png',
            'registrationDate': '2021-01-01T10:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 2,
            'authId': 102,
            'ingameCurrency': 3000.0,
            'profilePicture': 'profile2.png',
            'registrationDate': '2021-02-01T11:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 3,
            'authId': 103,
            'ingameCurrency': 0.0,
            'profilePicture': 'profile3.png',
            'registrationDate': '2021-03-01T12:00:00',
            'status': 'ACTIVE'
        }
    ]