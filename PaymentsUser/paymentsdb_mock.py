def get_history(userId):
    history={
            'id': 1,
            'userId': 1,
            'realAmount': 50,
            'ingameAmount': 100,
            'timestamp': "21/11/2024"
    }

    if history== history['userId']:
        return {"status":200,"data":history}
    else: 
        return {"status":404,"data":None}

def create_purchase(payload):
    if payload: 
        return{"status":200, "userId":1} 
    else:
        return {"status":400, "userId":None}

def get_user(userId):
    user = {
        'id': 1,
        'status': "ACTIVE",
        'profilePicture': "picture1",
        'ingameAmount': 200
    }
    if userId == user['id']:
        return {"status":200,"data":user}
    else: 
        return {"status":404,"data":None}   

def decrease_balance(payload) 
     if payload: 
        return{"status":200, "userId":1} 
    else:
        return {"status":400, "userId":None} 

def increase_balance(payload) 
     if payload: 
        return{"status":200, "userId":1} 
    else:
        return {"status":400, "userId":None}          



    