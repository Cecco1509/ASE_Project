def get_history(userId):
    history={
            'id': 1,
            'userId': 1,
            'realAmount': 50,
            'ingameAmount': 100,
            'timestamp': "21/11/2024"
    }

    if userId== history['userId']:
        return {"status":200,"data":history}
    else: 
        return {"status":404,"data":None}
