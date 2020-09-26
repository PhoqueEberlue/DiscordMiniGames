import discord
from games.Slapz.item import Item


class Player:

    def __init__(self, user: discord.user) -> None:
        self._user = user
        self._hp = 100
        self._inventory = []

    # GETTERS
    def getUser(self) -> discord.user:
        return self._user

    def getHp(self) -> int:
        return self._hp

    def getInventory(self) -> list[Item]:
        return self._inventory

    def full(self) -> bool:
        return len(self._inventory) >= 2

    # SETTERS
    def setHp(self, hp: int) -> None:
        self._hp = hp

    # ACTIONS
    def eat(self) -> None:
        if len(self._inventory) == 0:
            pass
        else:
            self._hp += self._inventory[0].getDmg()
            if self._hp > 100:
                self._hp = 100
            self._inventory.remove(self._inventory[0])

    def attack(self, opponent: 'Player') -> int:
        hp = opponent.getHp() - self._inventory[0].getDmg()
        opponent.setHp(hp)
        return hp

    def addInventory(self, item: Item) -> None:
        self._inventory.append(item)

    def removeInventory(self, position: int) -> None:
        self._inventory.pop(position)

    def __repr__(self) -> str:
        return f'{self._user.mention}'
