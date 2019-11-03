from PIL import Image, ImageDraw, ImageFont
import random
from string import ascii_letters as lets
import os

def create_captcha_string(hardness):
    s = ""
    for _ in range(random.randint(4,6) if hardness < 4 else random.randint(5, 7)):
        s += random.choice(lets)
    return s

def make_image_with_string(string, hardness):
    color = (random.randint(80, 255),random.randint(80, 255),random.randint(80, 255))
    img = Image.new("RGBA", (800, 300), color)
    draw = ImageDraw.Draw(img)
    for _ in range(round(random.randint(80, 200) * (hardness / 2))):
        i = random.randint(5, 20) * (hardness / 2)
        pos = (random.randint(0, 780), random.randint(0, 780))
        operations = [
            (draw.rectangle, ([pos, (pos[0] - i, pos[1] - i)], (0,0,0))),
            (draw.polygon, ([pos, (pos[0]-i, pos[1]-(i/2)), (pos[0]-(i/2), pos[1]-i)], (0,0,0))),
            (draw.ellipse, ([pos, (pos[0] + i, pos[1] + i)], (0,0,0)))
            ]
        do = random.choice(operations)
        do[0](*do[1])
    fnt = ImageFont.truetype('Font.ttf', random.randint(100, 150))
    draw.text((random.randint(30, 450 if len(string) > 6 else 350),random.randint(20,150)), string, font=fnt, fill=(0,0,0))
    return img, color

def gen_captcha(hardness):
    randstring = create_captcha_string(hardness)
    img, color = make_image_with_string(randstring, hardness)
    filename = os.path.join(os.getcwd(), "captcha.png")
    img.save(filepath)
    return randstring, filepath, color

