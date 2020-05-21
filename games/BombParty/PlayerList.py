class PlayerList:
    
    def __init__(self):
        self._list = []
        self._index = 0
        
    #GETTERS
    def oui(self):
        return "oui"
    
    #SETTERS
    def appendPlayer(self, user):
        self._list.append(user)
        
    def removePlayer(self, user):
        self._list.remove(user)
        
    def increaseIndex(self, user):
        if self._index >= len(self._list - 1):
            self._index = 0
        else:
            self._index += 1