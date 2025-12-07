import pygame
# import random
import json
from cryptography.fernet import Fernet


def load_enc(path, mode, save = None):
    key = "jAc607-Du0yJUVqdxXNkrP1x8NDxAcb_MOClmwL6Pzw="
    cipher_suite = Fernet(key)

    if mode == "r":
        try:
            with open(path, 'rb') as enc_file:
                cipher_text = enc_file.read()

            json_data_bytes = cipher_suite.decrypt(cipher_text)
            data = json.loads(json_data_bytes.decode('utf-8'))
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {'level': '1', 'money': '0', 'click': '0'}

    elif mode == 'w':
        save_enc = json.dumps(save).encode('utf-8')
        cipher_text = cipher_suite.encrypt(save_enc)

        with open(path, 'wb') as enc_file:
            enc_file.write(cipher_text)

def load_json(path, mode):
    if mode == 'r':
        with open(path, 'r') as file:
            data = json.load(file)
        return data

class Main:
    def __init__(self):
        self.load_game_data(load_enc('saves/save.enc', 'r'), 'int')
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Cow clicker")
        pygame.display.set_icon(pygame.image.load('images/icon.png'))

        self.prices_cow = [200, 500, 1000, 2000, 5000, 0]

        self.prices_click = [50, 100, 300, 500, 1000, 3000, 5000, 7000, 10000, 15000]  # 1,5; 2; 2,5; 3; 4; 5; 7; 8; 9; 15
        self.clicks = [1, 2, 3, 4, 5, 7, 8, 9, 10, 15]

        self.secret = 0
        self.running = True
        self.clock = pygame.time.Clock()

        self.load_assets()
        self.int_level()

    def load_assets(self):
        self.level_img = [
            pygame.image.load('images/level_1.png'),
            pygame.image.load('images/level_2.png'),
            pygame.image.load('images/level_3.png'),
            pygame.image.load('images/level_4.png'),
            pygame.image.load('images/level_5.png'),
            pygame.image.load('images/level_6.png'),
            pygame.image.load('images/powerful.png')
        ]

        self.shop = pygame.image.load('images/shop.png')
        self.board_money = pygame.image.load('images/board_money.png')
        self.click_lvl_up = pygame.image.load('images/click_lvl_up.png')
        self.cow_lvl_up = pygame.image.load('images/cow_lvl_up.png')
        self.info = pygame.image.load('images/info.png')
        self.flower = pygame.image.load('images/flower.png')
        self.background = pygame.image.load('images/background.png')

        self.font_constructor = pygame.font.Font('font/Jura-Medium.ttf', 60)
        self.font_info = pygame.font.Font('font/Jura-Medium.ttf', 40)

        self.font_money = self.font_constructor.render(str(self.money), False, 'white')
        self.font_cow = self.font_constructor.render(str(self.prices_cow[self.level - 1]), False, 'white')
        self.font_click = self.font_constructor.render(str(self.prices_click[self.click - 1]), False, 'white')

    def reload_font(self):
        self.font_money = self.font_constructor.render(str(self.money), False, 'white')
        self.font_cow = self.font_constructor.render(str(self.prices_cow[self.level - 1]), False, 'white')
        self.font_click = self.font_constructor.render(str(self.prices_click[self.click - 1]), False, 'white')


    def load_game_data(self, data, mode):
        if mode == 'int':
            self.level = int(data.get('level', 1))
            self.money = int(data.get('money', 0))
            self.click = int(data.get('click', 1))
        elif mode == 'str':
            save_data = {
                'level': str(self.level),
                'money': str(self.money),
                'click': str(self.click)
            }
            load_enc('saves/save.enc', 'w', save_data)

    def build_assets(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.what_level, (350, 250))
        self.screen.blit(self.board_money, (620, 0))
        self.screen.blit(self.info, (320, -20))
        self.screen.blit(self.flower, (-50, 50))

        self.screen.blit(self.shop, (700, 100))
        self.screen.blit(self.cow_lvl_up, (700, 250))
        self.screen.blit(self.click_lvl_up, (700, 510))

        self.screen.blit(self.font_money, (755, 24))
        self.screen.blit(self.font_cow, (770, 400))
        self.screen.blit(self.font_click, (770, 665))

        pygame.display.flip()

    def int_level(self):
        """ Определяет, какую картинку коровы показывать. """
        if self.secret >= 15 or self.level >= 6:
            self.what_level= self.level_img[5]  # powerful
            self.level = 6
        elif 1 <= self.level <= 5:
            self.what_level = self.level_img[self.level - 1]
        else:
            self.what_level = self.level_img[0]
            self.level = 1

    def events (self):
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                self.running = False

            elif self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                self.pos = self.event.pos
                if 350 < self.pos[0] < 650 and 250 < self.pos[1] < 550:  # money
                    self.money += self.clicks[self.click - 1]
                    self.font_money = self.font_constructor.render(str(self.money), False, 'white')

                elif 700 < self.pos[0] < 996 and 250 < self.pos[1] < 485:
                    if self.money >= self.prices_cow[self.level - 1] and self.level < 5:
                        if self.level < 5:
                            self.money -= self.prices_cow[self.level - 1]
                            self.level += 1
                            self.int_level()
                            self.build_assets()

                    elif self.level == 5:
                        self.secret += 1
                        self.int_level()


                elif 700 < self.pos[0] < 996 and 510 < self.pos[1] < 745:
                    if self.money >= self.prices_click[self.click - 1] and self.click < 10:
                        self.money -= self.prices_click[self.click - 1]
                        self.click += 1
                        self.build_assets()

            elif self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_F2:
                    self.save = load_json('saves/save.json', 'r')
                    self.load_game_data(self.save, 'int')
                    self.reload_font()
                    self.build_assets()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.build_assets()
            self.events()
        self.load_game_data([self.level, self.money, self.click], 'str')
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()