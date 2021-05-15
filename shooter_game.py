#Импорт библиотек
import os
from pygame import *
from random import randint
from time import time as time_t

#создание текста
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('GAME OVER', True, (180, 0, 0))
font2 = font.SysFont(None, 36)

"""def text_update(text, num, pos):
    text_img = font2.render(text + str(num), 1, WHITE_COLOR)
    window.blit(text_img, pos)
"""
img_back = "galaxy.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_exp = "explosion.png"
img_boss = "boss.png"

score = 0
lost = 0
goal = 25
max_lost = 7

limit_bull = 100        
limit_time = 0.5

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.2)
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
exp_sound = mixer.Sound("exp.ogg")




os.environ['SDL_VIDEO_CENTERED'] = "1"
init()
win_width = 1200
win_height = 800
display.set_caption("Space Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))




WHITE_COLOR = (255, 255, 255)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        fire_sound.play()
        bullet = Bullet(img_bullet, x=self.rect.centerx, y=self.rect.top,
                            size_x=15, size_y=20, speed=15)
        bullets.add(bullet) 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

class Exp(sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        size_x, size_y = 40, 25
        exp_sound.play()
        self.exp_img = [transform.scale(image.load(img_exp), (size_x, size_y)),
                         transform.scale(image.load(img_exp), (size_x + 10, size_y + 5)),
                         transform.scale(image.load(img_exp), (size_x + 20, size_y + 10)),
                         transform.scale(image.load(img_exp), (size_x + 30, size_y + 15)),
                         transform.scale(image.load(img_exp), (size_x + 40, size_y + 25)),
                         transform.scale(image.load(img_exp), (size_x + 50, size_y + 35))]
        self.image = self.exp_img[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.i = 1
        self.last_time = time_t()
    def update(self):
        if self.i < len(self.exp_img) and time_t() - self.last_time > 0.15:
            x, y = self.rect.centerx, self.rect.centery
            self.image = self.exp_img[self.i]
            self.rect = self.image.get_rect()
            self.rect.centerx, self.rect.centery = x, y
            self.i += 1
        elif self.i == len(self.exp_img):
            self.kill()


ship = Player(img_hero, x=5, y=win_height - 120, size_x=80, size_y=100, speed=15)
bullets = sprite.Group()
exps = sprite.Group()

monsters = sprite.Group()
for i in range(1, 8):
    monster = Enemy(img_enemy,
        x=randint(80, win_width - 80), y=-40, size_x=80, size_y=50, speed=randint(1, 3))
    monsters.add(monster)

run = True
finish = False

last_time = time_t()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE and not finish:
            if limit_bull > 0 and time_t() - last_time > limit_time:
                ship.fire()
                limit_bull -= 1
                last_time = time_t()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Счет: " + str(score), 1, WHITE_COLOR)
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, WHITE_COLOR)
        window.blit(text_lose, (10, 50))

        
        text_bull = font2.render("Патроны: " + str(limit_bull), 1, WHITE_COLOR)
        window.blit(text_bull, (10, 80))

        ship.update()
        monsters.update()
        bullets.update()
        exps.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        exps.draw(window)

        collides = sprite.groupcollide(monsters, bullets, False, True)
        for c in collides:
            score = score + 1
            exps.add(Exp(x=c.rect.centerx, y=c.rect.centery))
            c.rect.x = randint(80, win_width - 80)
            c.rect.y = -40
            c.speed = randint(1, 5)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (win_width//2 - 150, win_height//2 - 50))

        display.update()

    time.delay(50)