from datetime import datetime, timedelta

# Mock data for Auction
mock_auctions = [
    {
        'id': 1,
        'gachaCollectionId': 1,
        'userId': 1,
        'auctionStart': datetime.now() - timedelta(days=1),
        'auctionEnd': datetime.now() + timedelta(days=1),
        'minimumBid': 50.0,
        'timestamp': datetime.now() - timedelta(days=4),
        'status': "ACTIVE"
    },
    {
        'id': 2,
        'gachaCollectionId': 2,
        'userId': 2,
        'auctionStart': datetime.now() - timedelta(days=3),
        'auctionEnd': datetime.now() - timedelta(days=1),
        'minimumBid': 100.0,
        'timestamp': datetime.now() - timedelta(days=3),
        'status': "PASSED"
    },
    {
        'id': 3,
        'gachaCollectionId': 3,
        'userId': 3,
        'auctionStart': datetime.now(),
        'auctionEnd': datetime.now() + timedelta(days=5),
        'minimumBid': 200.0,
        'timestamp': datetime.now() ,
        'status': "PASSED"
    },
    {
        'id': 4,
        'gachaCollectionId': 4,
        'userId': 4,
        'auctionStart': datetime.now() + timedelta(days=4),
        'auctionEnd': datetime.now() + timedelta(days=5),
        'minimumBid': 200.0,
        'timestamp': datetime.now() ,
        'status': "ACTIVE"
    }
]

# Mock data for AuctionBid
mock_auction_bids = [
    {
        'id': 1,
        'userId': 4,
        'bidCode': "1:1",  # auctionId:bid_num
        'bidAmount': 55.0,
        'auctionId': 1,
        'timestamp': datetime.now() - timedelta(hours=2)
    },
    {
        'id': 2,
        'userId': 2,
        'bidCode': "1:2",
        'bidAmount': 60.0,
        'auctionId': 1,
        'timestamp': datetime.now() - timedelta(hours=1)
    },
    {
        'id': 3,
        'userId': 3,
        'bidCode': "2:1",
        'bidAmount': 110.0,
        'auctionId': 2,
        'timestamp': datetime.now() - timedelta(days=2)
    },
    {
        'id': 4,
        'userId': 4,
        'bidCode': "3:1",
        'bidAmount': 250.0,
        'auctionId': 3,
        'timestamp': datetime.now() - timedelta(hours=5)
    }
]

mock_gacha_collection_list = [
        {
            'id': 1,
            'gachaId': 1,
            'userId': 1,
            'timestamp': datetime.fromisoformat('2021-07-01T12:00:00'),
            'source': 'ROLL'
        },
        {
            'id': 2,
            'gachaId': 2,
            'userId': 2,
            'timestamp': datetime.fromisoformat('2021-07-01T12:01:00'),
            'source': 'AUCTION'
        },
        {
            'id': 3,
            'gachaId': 3,
            'userId': 3,
            'timestamp': datetime.fromisoformat('2021-07-01T12:02:00'),
            'source': 'ROLL'
        }
    ]


users = [
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