
def get_user(username):
    user = {
        'id': 1,
        "username":"user1",
        "password":"$2b$12$Mrnq5WRSYL2.P4ySDy5Lk.9qYDL1cE1HLPDQ5rVWGYvh1pj4T52Cy"#password1 hashed
    }
    if username == user['username']:
        return user
    else: 
        return None

def create_account(authData):
    return {"accountId":1}

def create_admin(userData):
    return {"accountId":1}

def create_user(userData):
    return {"userId":1}

def get_user_info(userId):
    user_info={
        'id': 1,
        'authId': 1,
        'ingameCurrency': 0,
        'profilePicture': "link to picture",
        'registrationDate': "01/12/2024",
        'status': "ACTIVE"
    }
    if userId == user_info['id']:
        return user_info
    else:
        return None

def get_salt():
    salt_str = "gc1FChp6ENV8XvvLS6KwwbVxQva3t8VL"
    return {"salt":salt_str.encode('UTF-8')}
