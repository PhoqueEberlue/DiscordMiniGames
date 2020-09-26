from PIL import Image
import requests
from os import path
from random import randint, choices, choice
from random import random
import json

from games.Slapz.player import Player
from .item import Item


def loadItems() -> list[Item]:
    itemsClass = []
    with open("./games/Slapz/data/items.json") as items:
        temp = json.load(items)
    for i in temp:
        itemsClass.append(Item(i["name"], i["dmg"], i["effects"], i["lootprob"]))
    return itemsClass


class Slapz:

    def __init__(self, players: list[Player]) -> None:
        self._players = players
        self._playerTurn = randint(0, len(self._players) - 1)
        self._fightCoef = 0.2
        self._counter = 0
        self._items = loadItems()

    def nextPlayer(self) -> Player:
        if len(self._players) - 1 == self._playerTurn:
            self._playerTurn = 0
        else:
            self._playerTurn += 1
        return self._players[self._playerTurn]

    def Move(self, player: Player) -> tuple:
        if random() < self._fightCoef:
            p = self._players.copy()
            p.remove(player)
            opponent = choice(p)
            return "fight", opponent
        else:
            if not player.full():
                item = self.loot()
                player.addInventory(item)
                return "loot", item
            else:
                return "full", None

    def fight(self, opponent: Player) -> None:
        pass

    def loot(self) -> Item:
        weights = ()
        for item in self._items:
            weights += (item.getLootProb(),)
        res = choices(self._items, cum_weights=weights, k=1)[0].copy()
        if isinstance(res.getDmg(), list):
            res.setDmg(randint(res.getDmg()[0], res.getDmg()[1]))
        return res

    def getRandomUser(self) -> Player:
        return choice(self._players)

    def updateCoef(self) -> None:
        if self._fightCoef < 1.0:
            self._counter += 1
            if self._counter > len(self._players) - 1:
                self._fightCoef += 0.05
                self._counter = 0

    def getEnd(self) -> bool:
        if len(self._players) <= 1:
            return True
        else:
            return False

    def removePlayer(self, player: Player) -> None:
        self._players.remove(player)

    def getWinner(self) -> Player:
        return self._players[0]

    def characterGen(self):
        for player in self._players:
            UserId = player.getUser().id
            if not path.exists(f"{UserId}.png"):
                response = requests.get(f"{player.avatar_url}")
                file = open(f"{UserId}.webp", "wb")
                file.write(response.content)
                file.close()
                im = Image.open(f"{UserId}.webp").convert("RGBA")
                new_im = im.resize((128, 128))
                bg = Image.open("./games/Slapz/img/background.png")
                bg.paste(new_im, (181, 181), new_im)
                ch = Image.open("./games/Slapz/img/character.png")
                bg.paste(ch, (0, 0), ch)
                bg.save(f"./games/Slapz/CharactersGenerations/{UserId}.png", "png")
