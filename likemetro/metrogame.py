from pygame import *
from random import randint
from time import time as timer
mixer.init()
fire_sound = mixer.Sound("bulletsound.mp3") 


wn = display.set_mode((640*1.5,243*1.5))
clock = time.Clock()
display.set_caption("Шутер")
font.init()
font1 = font.Font(None,36)
background = transform.scale(image.load("metro1.png"),(640*1.5,243*1.5))
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_x,pl_y,size_x,size_y,pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_speed
        self.size_x = size_x
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 63:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - self.size_x:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("abullet.png", self.rect.centerx+42, self.rect.top+20,15,20, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    
    
    def update(self):
        global lose

        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(75,620)
            self.speed = randint(1,5)

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
            self.rect.x += self.speed
            if self.rect.x > 640*1.5:
                self.kill()

            
game = True
finish = False
num_bul = 6
cur_bul = 0
hero = Player("hero.png", 100,150,132,132,5)
enemy1 = Enemy("enemy1.png", 650,150,132,132,5)
enemy1_show = 1
enemy1_hp = 10
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if cur_bul <= num_bul and fire_bul == False:
                    fire_sound.play()
                    rocket.fire()
                    cur_bul +=1
                elif  cur_bul >= num_bul and fire_bul == False:
                    fire_bul = True
                    hero.fire()
                    last_time = timer()

        
    if not finish:
        wn.blit(background,(0,0))
        hero.reset()
        hero.update()
        if enemy1_show:
            enemy1.reset()
        bullets.draw(wn)
        bullets.update()

        if fire_bul == True:
                now_time = timer()
                if now_time - last_time < 2:
                    reload = font1.render("RELOAD: ", 1,(160,25,2))
                    wn.blit(reload,(250,10))
                else:
                    fire_bul = False
                    cur_bul = 0




        collides_enemy = sprite.spritecollide(enemy1,bullets,True)
        if collides_enemy:
            enemy1_show = 0
    
    clock.tick(FPS)
    display.update()