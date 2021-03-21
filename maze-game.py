import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import csv
'''
Variables
'''
ALPHA=(0, 0, 0)
BLUE  = (25, 25, 200)
RED = (255, 0, 0)
BLACK = (23, 23, 23)
PURPLE = (150, 0, 150)
WHITE = (254, 254, 254)
GREEN = (0,128,0,1)
BROWN = (165, 42, 42, 1)
GREEN_BROWN = (165,128,42,1)
ORANGE= (156,45,0,4)
LIGHT_GREEN = (42, 159,0,45)
worldx = 1280
worldy = 704
tx=64
ty=64
steps=10
fps   = 50 # frame rate
ani   = 4   # animation cycles
'''
Mazes
'''
maze1=[[1]*20,
      [1]+[0]*14+[1]+[0]*3+[1],
       [1,1,0,1,0,2,1,0,1,1,1,0,1,1,1,1,1,1,2,1],
       [1,0,0,1,0,0,1,0,0,2,0,0,2,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1],
       [0,0,0,0,0,2,0,0,1,0,1,0,1,0,0,1,0,1,0,1],
       [1,1,1,0,1,1,1,2,1,0,1,0,2,1,0,1,0,1,0,1],
       [1,2,1,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1],
       [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,2],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

maze2=[[1]*20,
[1,0,0,0,2,0,1,0,0,0,2,0,0,0,0,0,0,2,0,1],
[1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
[1,0,1,0,0,0,1,2,0,1,0,0,0,0,2,1,1,1,0,0],
[1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,2,0,1],
[0,0,0,0,0,1,1,1,2,1,1,1,1,1,1,1,1,1,0,1],
[1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,0,0,1],
[1,0,1,1,1,1,1,1,0,1,0,0,2,0,1,0,1,0,1,1],
[1,0,2,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0,0,1],
[1]*20]
'''
Objects
'''
class Player (pygame.sprite.Sprite):
    def __init__ (self, x, y, imgfile="Elf1.png",lvl=1):
        (sizex, sizey)=(40,40)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('Images',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
      # img.convert_alpha()     # optimise alpha
        #img.set_colorkey(ALPHA) # set alpha
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        self.movex=0
        self.movey=0
        self.score=lvl*10
        self.collectedchest=False
        self.levelcomplete=False
        
    def control(self,x,y):
        self.movex += x
        self.movey += y
        
    def update(self,wall_list,chest_list,coin_list):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x < 0:
            self.rect.x =0
        if self.rect.x > worldx-tx:
            if self.collectedchest:
                self.levelcomplete=True
            else:
                self.rect.x =worldx-tx
        collidelist=pygame.sprite.spritecollide(self,wall_list,False)
        for wall in collidelist:
            self.rect.x-=self.movex
            self.rect.y-=self.movey
        collidelist=pygame.sprite.spritecollide(self,chest_list,False)
        for chest in collidelist:
            self.collectedchest=True
            self.score+=100
            chest.disappear()
        collidelist=pygame.sprite.spritecollide(self,coin_list,False)
        for coin in collidelist:
            self.score+=10
            coin.disappear()
            
class Wall(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.x=x
        self.y=y
        self.visible=False
        self.show()
        
    def show(self):
        if self.visible:
            self.rect.x=self.x
            self.rect.y=self.y
        else:
            self.rect.x=-100
            self.rect.y=-100
                    
    def update (self,playerx,playery):
        if abs(playerx-self.x)<2*tx and abs(playery-self.y)<2*ty:
            self.visible=True
        else:
            self.visible=False
        self.show()
        
        
class Chest(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def disappear(self):     
        self.image = pygame.transform.scale(self.image,(int(tx/2),int(ty/2)))
        self.rect  = self.image.get_rect()
        self.rect.x=150
        self.rect.y=10
    
class Coin(pygame.sprite.Sprite):
    
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def disappear(self):
        self.rect.x=worldx+100
        self.rect.y=worldy+100
    '''
    Setup
    '''

class platform_game():
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.world    = pygame.display.set_mode([worldx,worldy])

    def setup(self,lvl=1):
        self.lvl=1
        if lvl==1:
            px=0
            py=int(5*ty)
            self.colour=GREEN_BROWN
            chestx=11*tx
            chesty=3*ty
            maze=maze1
        if lvl==2:
            px=0
            py=5*ty
            self.colour=BLACK
            chestx=10*tx
            chesty=6*ty
            maze=maze2
        self.player=Player(px, py)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        img = pygame.image.load(os.path.join('Images','wall.png'))
        img = pygame.transform.scale(img,(tx,ty))
        img.convert_alpha()     # optimise alpha
        img.set_colorkey(ALPHA) # set alpha
        self.wall_list=pygame.sprite.Group()
        self.coin_list=pygame.sprite.Group()
        cimg = pygame.image.load(os.path.join('Images','Coin.png'))
        cimg = pygame.transform.scale(cimg,(int(tx/2),int(ty/2)))
        cimg.convert_alpha()     # optimise alpha
        cimg.set_colorkey(ALPHA) # set alpha
        for i,row in enumerate(maze):
            for j,pos in enumerate(row):
                x=j*tx
                y=i*ty
                if pos==1:
                    wall=Wall(x,y,img)
                    self.wall_list.add(wall)
                elif pos==2:
                    coin=Coin(x,y,cimg)
                    self.coin_list.add(coin)
        img = pygame.image.load(os.path.join('Images','ChestRed.png'))
        img = pygame.transform.scale(img,(tx,ty))
        img.convert_alpha()     # optimise alpha
        img.set_colorkey(ALPHA) # set alpha
        self.chest_list=pygame.sprite.Group()
        chest=Chest(chestx,chesty,img)
        self.chest_list.add(chest)
    
    
    def playgame(self):
        main=True
        while main == True:
            if self.player.levelcomplete:
                pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
            if self.player.score<0:
                pygame.event.post(pygame.event.Event(pygame.QUIT,{}))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("gameover, your score is " +str(int(self.player.score)))
                    pygame.quit(); sys.exit()
                    main = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(-steps,0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(steps,0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0,-steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0,steps)
                    if event.key == ord('q'):
                        pygame.quit()
                        sys.exit()
                        main=False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(steps,0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(-steps,0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0,steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0,-steps)
            self.world.fill(self.colour)
            self.player_list.update(self.wall_list,self.chest_list,self.coin_list)
            self.player_list.draw(self.world) # draw player
            self.wall_list.update(self.player.rect.x, self.player.rect.y)
            self.wall_list.draw(self.world)
            self.chest_list.draw(self.world)
            self.coin_list.draw(self.world)
            largeFont=pygame.font.SysFont("arial",25)
            text=largeFont.render("coins: "+str(int(self.player.score)),1,WHITE)
            self.world.blit(text,(10,10))
            
            pygame.display.flip()
            self.clock.tick(fps)
            self.player.score-=1/fps

lvl=2
mygame=platform_game()
mygame.setup(lvl=lvl)
mygame.playgame()