class item:
    def __init__(self, name, dmg, effect):
        self._name = name
        self._dmg = dmg
        self._effect = effect
    
    #GETTERS  
    def getName(self):
        return self._name
    
    def getDmg(self):
        return self._dmg
    
    def getEffect(self):
        return self._effect
    
    #SETTERS
    def setDmg(self, dmg):
        self._dmg = dmg