class player:
    
    def __init__(self, user):
        self._user = user
        self._hp = 100
        self._inventory = []
    
    #GETTERS
    def getUser(self):
        return self._user
    
    def getHp(self):
        return self._hp
    
    def getInventory(self):
        return self._inventory
    
    def full(self):
        return self._inventory >= 2
    #SETTERS
    def setHp(self, hp):
        self._hp = hp

    #ACTIONS        
    def eat(self, item):
        self._hp += item.getDmg()
        if self._hp > 100:
            self._hp = 100
        self._inventory.remove(item)

    def addInventory(self, item):
        self._inventory.append(item)

    def removeInventory(self, position):
        self._inventory.pop(position)