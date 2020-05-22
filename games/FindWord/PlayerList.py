from random import randint
from games.FindWord.Player import Player

class PlayerList:
    
    def __init__(self):
        self._list = []
        self._index = 0
        
    #GETTERS
    def currentPlayer(self):
        return self._list[self._index]
    
    def isEnd(self):
        if len(self) == 1:
            return True
        else: 
            return False
        
    def getWinner(self):
        return self._list[0]
    
    #SETTERS
    def appendPlayer(self, player:Player):
        self._list.append(player)
        
    def removePlayer(self, user):
        self._list.remove(user)
        
    def increaseIndex(self):
        if self._index >= len(self._list) - 1:
            self._index = 0
        else:
            self._index += 1
            
    def setRandomIndex(self):
        self._index = randint(0, len(self._list) - 1)
            
    def __len__(self):
        return len(self._list)