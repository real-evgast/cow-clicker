import pygame
import random
import json
from cryptography.fernet import Fernet

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1000, 800))

key = "jAc607-Du0yJUVqdxXNkrP1x8NDxAcb_MOClmwL6Pzw="
cipher_suite = Fernet(key)

def load_enc(path, mode, save = None):
    global cipher_text, save_enc, enc_file
    if mode == "r":
        with open(path, 'rb') as enc_file: #mode: "rb"
            cipher_text = enc_file.read()

        json_data_bytes = cipher_suite.decrypt(cipher_text)
        data = json.loads(json_data_bytes.decode('utf-8'))
        return data

    elif mode == "w":
        save_enc = json.dumps(save).encode('utf-8')
        cipher_text = cipher_suite.encrypt(save_enc)

        with open(path, 'wb') as enc_file:
            enc_file.write(cipher_text)

def load_json(path, mode):
    if mode == 'r':
        with open(path, 'r') as file:
            data = json.load(file)
        return data

def refactor_str():
    global level, money, click
    level = int(save['level'])
    money = int(save['money'])
    click = int(save['click'])

save = load_enc('saves/save.enc', 'r')
refactor_str()

icon = pygame.image.load('image/icon.png')

level_1 = pygame.image.load('image/level_1.png')
level_2 = pygame.image.load('image/level_2.png')
level_3 = pygame.image.load('image/level_3.png')
level_4 = pygame.image.load('image/level_4.png')
level_5 = pygame.image.load('image/level_5.png')
level_6 = pygame.image.load('image/level_6.png')
powerful = pygame.image.load('image/powerful.png')

shop = pygame.image.load('image/shop.png')
board_money = pygame.image.load('image/board_money.png')
click_lvl_up = pygame.image.load('image/click_lvl_up.png')
cow_lvl_ip = pygame.image.load('image/cow_lvl_up.png')
syringe_ = pygame.image.load('image/syringe.png')
info = pygame.image.load('image/info.png')

background = pygame.image.load('image/фон.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("cow clicker")

prices_cow = [200, 500, 1000, 2000, 5000, '']

prices_click = [50, 100,  300,  500, 1000,  3000,  5000,  7000,  10000,  15000] # 1,5; 2; 2,5; 3; 4; 5; 7; 8; 9; 15
clicks =       [1,    2,    3,    4,    5,     7,     8,     9,     10,     15]

font_constructor = pygame.font.Font('font/Jura-Medium.ttf', 60)

font_info = pygame.font.Font('font/Jura-Medium.ttf', 40)

font_money = font_constructor.render(str(money), False, 'white')
font_cow = font_constructor.render(str(prices_cow[level - 1]), False, 'white')
font_click = font_constructor.render(str(prices_click[click - 1]), False, 'white')

info_level = font_info.render("lvl cow = " + str(level), False, 'white')
info_click = font_info.render("lvl click = " + str(click), False, 'white')

syringe = 0
secret = 0

def int_level():
    global level, what_level
    if level == 1:
        what_level = level_1

    elif level == 2:
        what_level = level_2

    elif level == 3:
        what_level = level_3

    elif level == 4:
        what_level = level_4

    elif level == 5:
        what_level = level_5

    else:
        what_level = level_1
        level = 1

    if secret == 6 or level == 6:
        what_level = level_6
        level = 6

    if syringe == 2:
        what_level = powerful

def restart_sprite():
    global font_money, font_cow, info_level, info_click
    font_money = font_constructor.render(str(money), False, 'white')
    font_cow = font_constructor.render(str(prices_cow[level - 1]), False, 'white')
    info_click = font_info.render("lvl click = " + str(click), False, 'white')
    info_level = font_info.render("lvl cow = " + str(level), False, 'white')

    int_level()

running = True
int_level()

auto_lvl_up_ = 0

cor = [0, 0]
def randomizer():
    global syringe
    randoms = random.randint(-30, 10)
    if randoms > 0 and syringe == 0:
        syringe = 1
        cor[0] = random.randint(300, 600)
        cor[1] = random.randint(500, 800)
    else:
        syringe = 0

tick = 0



while running:
    clock.tick(60)
    tick += 1
    if tick == 1800 and syringe == 0:
        randomizer()
        tick = 0

    elif tick == 1800 and syringe == 2:
        syringe = 0
        tick = 0
        int_level()
        info_click = font_info.render("lvl click = " + str(click), False, 'white')

    if level == 5:
        font_cow = font_constructor.render("", False, 'white')

    if click == 10:
        font_click = font_constructor.render("", False, 'white')

    screen.blit(background, (0, 0))
    screen.blit(what_level, (0, 0))
    screen.blit(info, (270, -25))

    screen.blit(board_money, (670, 0))
    screen.blit(shop, (-20, 230))
    screen.blit(cow_lvl_ip, (20, 440))
    screen.blit(click_lvl_up, (20, 590))

    screen.blit(font_money, (800, 26))
    screen.blit(font_cow, (330, 470))
    screen.blit(font_click, (330, 620))

    screen.blit(info_level, (340, 80))
    screen.blit(info_click, (340, 120))

    if syringe == 1:
        screen.blit(syringe_, (cor[0], cor[1]))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if 0 < pos[0] < 300 and pos[1] < 300:
                if syringe == 2:
                    money += clicks[click - 1] * 2

                else:
                    money += clicks[click - 1]

                font_money = font_constructor.render(str(money), False, 'white')

            elif 20 < pos[0] < 306 and 440 < pos[1] < 570:
                try:
                    if money >= prices_cow[level - 1] and level != 6:
                        if level < 5:
                            money = money - prices_cow[level - 1]
                            font_money = font_constructor.render(str(money), False, 'white')
                            level += 1
                            font_cow = font_constructor.render(str(prices_cow[level - 1]), False, 'white')
                            info_level = font_info.render("lvl cow = " + str(level), False, 'white')
                            int_level()
                except TypeError:
                    None

                if level == 5:
                    font_cow = font_constructor.render("", False, 'white')
                    secret += 1
                    int_level()

            elif 20 < pos[0] < 316 and 590 < pos[1] < 708:
                if prices_click[click - 1] < money or prices_click[click - 1] == money:
                    if click < 10:
                        money = money - prices_click[click - 1]
                        click += 1
                        font_money = font_constructor.render(str(money), False, 'white')
                        font_click = font_constructor.render(str(prices_click[click - 1]), False, 'white')
                        info_click = font_info.render("lvl click = " + str(click), False, 'white')

                    if click == 10:
                        font_click = font_constructor.render("", False, 'white')


            elif 20 < pos[0] < 466 and 740 < pos[1] < 858:
                auto_lvl_up_ = 1

            elif cor[0] < pos[0] < cor[0] + 130 and cor[1] < pos[1] < cor[1] + 130 and syringe == 1:
                syringe = 2
                int_level()
                info_click = font_info.render("lvl click = " + str(click) + " x 2!!!", False, 'white')

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                save = load_json('saves/save.json', 'r')
                refactor_str()
                restart_sprite()



save['level'] = str(level)
save['money'] = str(money)
save['click'] = str(click)

# with open('saves/save.json', 'w') as file:
#     json.dump(save, file, ensure_ascii = False, indent = 4)

save_enc = json.dumps(save).encode('utf-8')
cipher_text = cipher_suite.encrypt(save_enc)

with open('saves/save.enc', 'wb') as enc_file:
    enc_file.write(cipher_text)
pygame.quit()