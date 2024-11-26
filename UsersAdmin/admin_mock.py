
def getPlayer(user_id):
    user={
        'id': 1,
        'authId': 123,
        'ingameCurrency': 1000,
        'profilePicture': "slika.jpg",
        "registrationDate": "Thu, 21 Nov 2024 21:41:09 GMT",
        'status': "ACTIVE"
    }
    if(user_id==user['id']):
        return {"status":200,"data":user}
    else:
        return {"status":404,"data":None}


def getPlayers():
    user1={
        'id': 1,
        'authId': 123,
        'ingameCurrency': 1000,
        'profilePicture': "slika.jpg",
        "registrationDate": "Thu, 21 Nov 2024 21:41:09 GMT",
        'status': "ACTIVE"
    }
    user2={
        'id': 2,
        'authId': 456,
        'ingameCurrency': 2000.0,
        'profilePicture': "slika1241.jpg",
        "registrationDate": "Thu, 21 Nov 2024 21:11:09 GMT",
        'status': "BANNED"
    }
    user3={
        'id': 3,
        'authId': 789,
        'ingameCurrency': 3100.12,
        'profilePicture': "slika.j241pg",
        "registrationDate": "Thu, 21 Nov 2024 21:41:01 GMT",
        'status': "ACTIVE"
    }
    users = [user1, user2, user3]
    return {"data":users,"status":200}

def updatePlayer():
    return {"status":200,"data":"message"}

def banPlayer(user_id):
    if user_id==1:
        return {"status":200,"data":"User successfully deleted"}
    else:
        return {"status":404,"data":"Player not found"}