from pygame import *
from random import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('game shooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# mixer.music.set_volume(0.2)

font.init()
font1 = font.Font(None, 24)
font2 = font.Font(None, 60)
miss = 0
poin = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_w, size_h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_w, size_h))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 15, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            miss += 1
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player('rocket.png', 300, 430, 65, 65, 5)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width-80), 0, 65, 65, randint(1, 2))
    monsters.add(monster)

fps = time.Clock()
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        missed = font1.render('missed: ' + str(miss), 1, (255, 255, 0))
        window.blit(missed, (5, 5))
        score = font1.render('score: ' + str(poin), 1, (255, 255, 0))
        window.blit(score, (5, 20))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            poin += 1
            monster = Enemy('ufo.png', randint(80, win_width-80), 0, 65, 65, randint(1, 2))
            monsters.add(monster)
        if miss >= 7:
            lose = font2.render('YOU LOSE', True, (200, 0, 0))
            window.blit(lose, (300, 200))
            finish = True
        if poin >= 10:
            win = font2.render('YOU WIN', True, (0, 200, 0))
            window.blit(win, (300, 200))
            finish = True
        display.update()
        fps.tick(60)