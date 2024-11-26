from datetime import datetime

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

def updatePlayer():
    return {"status":200,"data":"message"}

def deletePlayer(user_id):
    if user_id==1:
        return {"status":200,"data":"User successfully deleted"}
    else:
        return {"status":404,"data":"Player not found"}
