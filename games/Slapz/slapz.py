import discord
from PIL import Image
import requests
import os.path
from os import path
from random import randint
from random import random
from random import choice
import json
from .item import item
from .player import player

class slapz:

    def __init__(self, players):
        self._players = players
        self._playerTurn = randint(0, len(self._players)-1)
        self._fightCoef = 0.2
        self._end = False
        self._items = self.loadItems()
    
    def loadItems(self):
        itemsClass = []
        temp = []
        with open("./data.items.json") as items:
            temp = items
        for i in items:
            if type(item["dmg"]) == list:
                itemsClass.append(item(item["name"], randint(item["dmg"][0],item["dmg"][1]), item["effect"], item["lootprob"]))
            else:
                itemsClass.append(item(item["name"], item["dmg"], item["effect"], item["lootprob"]))
        return itemsClass

    def nextPlayer(self):
        if len(self._players) - 1 == self._playerTurn: 
            self._playerTurn = 0
        else:
            self._playerTurn += 1
        return self._players[self._playerTurn]

    def Move(self, player):
        if random() > self._fightCoef:
            pass
            #fight
        else:
            if not player.full():
                player.addInventory(self.loot())
            else:
                pass
                #INVENTORY FULL
            #loot
    
    def loot(self):
        weights = ()
        for item in self._items:
            weights += (item.getLootProb(),)
        return choice(self._items, cum_weights=weights, k=1)[0]

    def getRandomUser(self):
        return choice(self._players)
    
    def endGame(self):
        self._end = True

    def getEnd(self):
        return self._end

    def characterGen(self):
        for user in self._players:
            UserId = user.id
            if not path.exists(f"{UserId}.png"):
                response = requests.get(f"{user.avatar_url}")
                file = open(f"{UserId}.webp", "wb")
                file.write(response.content)
                file.close()
                im = Image.open(f"{UserId}.webp").convert("RGBA")
                new_im = im.resize((128,128))
                bg = Image.open("./games/Slapz/img/background.png")
                bg.paste(new_im, (181,181), new_im)
                ch = Image.open("./games/Slapz/img/character.png")
                bg.paste(ch, (0,0), ch)
                bg.save(f"./games/Slapz/CharactersGenerations/{UserId}.png", "png")