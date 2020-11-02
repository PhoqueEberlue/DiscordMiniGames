from typing import List
from typing import Union


class Item:
    def __init__(self, name: str, dmg: Union[int, List[int]], effect: str, lootprob: float) -> None:
        self._name = name
        self._dmg = dmg
        self._effect = effect
        self._lootprob = lootprob

    # GETTERS
    def getName(self) -> str:
        return self._name

    # items can have a fixed amount of dmg or a list of two int. Items inside players inventory will be dmg = random.choice(dmg[0], dmg[1])
    def getDmg(self) -> Union[int, List[int]]:
        return self._dmg

    def getEffect(self) -> str:
        return self._effect

    def getLootProb(self) -> float:
        return self._lootprob

    # SETTERS
    def setDmg(self, dmg: int) -> None:
        self._dmg = dmg

    def __repr__(self) -> str:
        return f'{self._name}, {self._dmg}, {self._effect}'

