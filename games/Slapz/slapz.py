import discord
from PIL import Image
import requests
import os.path
from os import path

class slapz:

    def __init__(self, players):
        self._players = players
        self._playerTurn = 0
    
    def main(self):
        pass

    def nextPlayer(self):
        if len(self._players) - 1 == self._playerTurn: 
            self._playerTurn = 0
        else:
            self._playerTurn += 1


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