from pygame import *
from random import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x , player_y, weight, height,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (weight ,height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    
    def reset(self):
        window.blit(self.image,(self.rect.x , self.rect.y))

stechikfr = 0 
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed 
        if keys_pressed[K_s] and self.rect.y < 500:
            self.rect.y += self.speed  
    def fire(self):
        bullet = Bullet('ammo_milit.png', self.rect.centerx ,self.rect.top,  15 , 20, 3)
        bullets.add(bullet)
        fire.play()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = randint(0 , 450)
            vrag.fire()
    def fire(self):
        bulletvrag = Bulletvrag('ammo_police.png', self.rect.centerx, self.rect.top, 15,20, -3)
        bulletsvrag.add(bulletvrag)
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.y < 0:
            self.kill()
class Bulletvrag(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()
font.init()
font1 = font.SysFont('Arial' , 36)
font2 = font.SysFont('Arial' , 80)
win = font2.render(
    'YOU WIN!', True , (255 , 255 ,0)
)
lose = font2.render(
    'YOU LOSE!' , True , (255 , 0 , 0)
)
vragi = sprite.Group()
bulletsvrag = sprite.Group()
military = Player('milit.png', 5 ,420 ,65 , 65, 1)
window = display.set_mode((700,500))
for i in range(1 , 6):
    vrag= Enemy('police.png' , 575 ,randint(0 , 595) ,90 , 70, 2)
    vragi.add(vrag)
bullets = sprite.Group()
display.set_caption("Project D")
fon = transform.scale(image.load("back.jpg"), (700,500))
game = True
finish = False
mixer.init()
fire = mixer.Sound('militsound.ogg')
mixer.music.load('musik.ogg')
mixer.music.play()
clock = time.Clock()
FPS = 300
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire != 30 and rel_time == False:
                    military.fire()
                    num_fire = num_fire + 1
                if num_fire >= 30 and rel_time == False:
                    start_time = timer()
                    rel_time = True
    if not finish:
        window.blit(fon , (0,0))
        text = font1.render("Счёт:" + str(stechikfr), 1, (255,255,255))
        window.blit(text, (10,20))
        collides = sprite.groupcollide(vragi , bullets , True , True)
        for c in collides:
            stechikfr = stechikfr + 1
            vrag = Enemy('police.png' , 575 ,randint(0 , 595) ,90 , 70, 2)
            vragi.add(vrag)
        if sprite.spritecollide(military , bulletsvrag , False):
            window.blit(lose , (200 , 200))
            finish = True
        if stechikfr > 10:
            window.blit(win , (200,200))
            finish = True
        if rel_time == True:
            now_time = timer()
            if now_time - start_time < 3:
                text12 = font1.render("ПОГОДИ ПЕРЕЗАРЯДКА" , 1 ,(255,0,0))
                window.blit(text12 ,(200, 450))
            else: 
                num_fire = 0
                rel_time = False
        military.reset()
        vragi.update()
        vragi.draw(window)
        military.update()
        bullets.update()
        bulletsvrag.update()
        bulletsvrag.draw(window)
        bullets.draw(window)
        display.update()
        clock.tick(FPS)
    else:
        finish = False
        stechikfr = 0
        stechiklvl = 0
        for b in bullets:
            b.kill()
        for m in vragi:
            m.kill()
        time.delay(15000)
        for i in range(1 , 6):
            vrag = Enemy('police.png' , 575 ,randint(0 , 595) ,90 , 70, 2)
            vragi.add(vrag)