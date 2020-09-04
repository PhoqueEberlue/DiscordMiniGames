from PIL import Image


im = Image.open("0.webp").convert("RGBA")
new_im = im.resize((128,128))
new_im.save("0.png", "png")

bg = Image.open("./games/Slapz/img/background.png")
bg.paste(new_im, (180,180), new_im)
bg.save("iii.png", "png")

im = Image.open("iii.png")
ch = Image.open("./games/Slapz/img/character.png")
im.paste(ch, (0,0), ch)
im.save("iii.png", "png")
