from datetime import datetime, timedelta

mock_transactions = [
    {
        'id': 1,
        'sellerId': 1,
        'buyerId': 2,
        'auctionBidId': 1,
        'timestamp': datetime.now() - timedelta(days=1)
    },
    {
        'id': 2,
        'sellerId': 2,
        'buyerId': 3,
        'auctionBidId': 2,
        'timestamp': datetime.now() - timedelta(days=2)
    },
    {
        'id': 3,
        'sellerId': 3,
        'buyerId': 4,
        'auctionBidId': 3,
        'timestamp': datetime.now() - timedelta(hours=5)
    },
    {
        'id': 4,
        'sellerId': 4,
        'buyerId': 5,
        'auctionBidId': 4,
        'timestamp': datetime.now() - timedelta(hours=1)
    }
]

mock_users = [
    {
        'id': 1,
        'authId': 101,
        'ingameCurrency': 250.0,
        'profilePicture': 'http://example.com/images/user1.jpg',
        'registrationDate': datetime.now() - timedelta(days=30),
        'status': "ACTIVE"
    },
    {
        'id': 2,
        'authId': 102,
        'ingameCurrency': 125.5,
        'profilePicture': 'http://example.com/images/user2.jpg',
        'registrationDate': datetime.now() - timedelta(days=60),
        'status': "INACTIVE"
    },
    {
        'id': 3,
        'authId': 103,
        'ingameCurrency': 500.0,
        'profilePicture': 'http://example.com/images/user3.jpg',
        'registrationDate': datetime.now() - timedelta(days=15),
        'status': "BANNED"
    },
    {
        'id': 4,
        'authId': 104,
        'ingameCurrency': 1000.0,
        'profilePicture': 'http://example.com/images/user4.jpg',
        'registrationDate': datetime.now() - timedelta(days=5),
        'status': "ACTIVE"
    }
]