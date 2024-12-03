
def get_user(username):
    user = {
        'id': 1,
        "username":"user1",
        "password":"password1"
    }
    if username == user['username']:
        return {"status":200,"data":user}
    else: 
        return {"status":404,"data":None}

def create_account(authData):
    return {"status":200, "data":1}

def create_user(userData):
    return {"status":200, "data":1}
