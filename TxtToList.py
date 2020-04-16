import json

F = open("txt_files/liste_francais.txt", "r")
wordList = F.read().split("\n")
loweredList = []
for word in wordList:
    loweredList.append(word.lower())
recurence = {}
for word in loweredList:
    for i in range(len(word)):
        if i < len(word)-1:
            letters = str(word[i] + word[i+1])
            if letters in recurence.keys():
                recurence[letters] += 1
            else:
                recurence[letters] = 1
for word in loweredList:
    for i in range(len(word)):
        if i < len(word)-2:
            letters = str(word[i] + word[i+1] + word[i+2])
            if letters in recurence.keys():
                recurence[letters] += 1
            else:
                recurence[letters] = 1
delList = []
for letters, number in recurence.items():
    if number < 100 or "-" in letters:
        delList.append(letters)
for letters in delList:        
    del recurence[letters]
lettersList = []
for letters in recurence.keys():
    lettersList.append(letters)
with open('Dictionnaries.json', "r", encoding="utf-8") as read_file:
    Dictionnaries = json.load(read_file)
    Dictionnaries["fr"]["words"] = loweredList
    Dictionnaries["fr"]["letters"] = lettersList
with open('Dictionnaries.json', "w", encoding="utf-8") as write_file:
    json.dump(Dictionnaries, write_file)