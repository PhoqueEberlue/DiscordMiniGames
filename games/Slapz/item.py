class Item:
    def __init__(self, name, dmg, effect, lootprob):
        self._name = name
        self._dmg = dmg
        self._effect = effect
        self._lootprob = lootprob

    #GETTERS  
    def getName(self):
        return self._name
    
    def getDmg(self):
        return self._dmg
    
    def getEffect(self):
        return self._effect
    
    def getLootProb(self):
        return self._lootprob
    
    #SETTERS
    def setDmg(self, dmg):
        self._dmg = dmg

    def __repr__(self):
        return f'{self._name}, {self._dmg}, {self._effect} |'

