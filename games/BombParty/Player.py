class player:
    
    def __init__(self, user):
        self._user = user
        self._life = 2
        
    #GETTERS
    def getUser(self):
        return self._user
    
    def getLife(self):
        return self._life
    
    #SETTERS
    def decreaseLife(self):
        self._life -= 1
        
    def increaseLife(self):
        self._life += 1