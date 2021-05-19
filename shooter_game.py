# shooter_game
from pygame import *
from random import randint 
class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,play_speed, w, h):
        super().__init__()
        self.image=transform.scale(image.load(img),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=play_speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d]:
            self.rect.x+=self.speed
        if keys_pressed[K_a]:
            self.rect.x-=self.speed
    def fire(self):
        bullet=Bullet("bullet.png",self.rect.x,self.rect.y,3,20,20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >=500:
            x=randint(0,600)
            self.rect.x=x
            self.rect.y=0
            lost=lost+1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >=500:
            x=randint(0,600)
            self.rect.x=x
            self.rect.y=0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <=0:
            self.kill()
score=0
lost=0
window = display.set_mode((700,500))
display.set_caption("Лабиринт")
background= transform.scale(image.load("galaxy.jpg"),(700,500))
#создай 2 спрайта и размести их на сцене
bullets = sprite.Group()
monsters = sprite.Group()
asteroids=sprite.Group()
i=0
for i in range(8):
    x=randint(0,650)
    speed=randint(1,3)
    m=Enemy("ufo.png",x,0,speed,50,50)
    monsters.add(m)
for i in range(3):
    x=randint(0,600)
    speed=randint(1,2)
    asteroid=Enemy("asteroid.png",x,0,speed,50,50)
    asteroids.add(asteroid)
game = True
clock=time.Clock()
FPS=60
mixer.init()
firerock=mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()
hero=Player("rocket.png",50,430,10,50,70)
font.init()
font=font.SysFont("Arial",50)
lose=font.render('ТЫ ПРОИГРАЛ',True,(255,215,0))
winr=font.render('ТЫ ВЫЙГРАЛ',True,(255,215,0))
finish=False
while game:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                firerock.play()
                hero.fire()
    if finish != True:
        window.blit(background,(0,0))
        hero.move()
        monsters.update()
        bullets.update()
        asteroids.update()

        hero.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        win=font.render('счет :'+str(score),1,(255,255,255))
        text_lose=font.render('пропущено :'+str(lost),1,(255,255,255))
        window.blit(text_lose,(0,0))
        window.blit(win,(0,50))
        if lost >=10:
            finish = True
            window.blit(lose,(250,200))
        if sprite.groupcollide(bullets,asteroids,True,False):
            finish=False
        if sprite.spritecollide(hero,asteroids,False):
            finish=True
            window.blit(lose,(250,200))
        if sprite.groupcollide(monsters,bullets,True,True):
            finish = False
            x=randint(0,700)
            speed=randint(1,3)
            m=Enemy("ufo.png",x,0,speed,50,50)
            monsters.add(m)
            score = score + 1
            if score >= 10:
                finish = True
                window.blit(winr,(250,200))
        if sprite.spritecollide(hero,monsters,False):
            finish = True
            window.blit(lose,(250,200))
    display.update()
