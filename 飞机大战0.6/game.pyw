import pygame
import random
pygame.init()
class bg(pygame.sprite.Sprite):
    def __init__(self,image,y,sp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = -5
        self.rect.top = 0
        self.y_speed = sp
        self.y = y

    def move(self,screen):
        self.y += self.y_speed
        self.rect.top = (self.y+720)%1440-720
        screen.blit(self.image,self.rect)

class Aircraft_me(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [475,650]
        self.list = []

    def move(self,x,y,screen,aco_l):
        self.rect.centerx += x
        self.rect.centery += y
        if self.rect.centery > screen.get_height():
            self.rect.centery = screen.get_height()

        if self.rect.centerx > screen.get_width():
            self.rect.centerx = screen.get_width()

        if self.rect.centery < 0:
            self.rect.centery = 0

        if self.rect.centerx < 0:
            self.rect.centerx = 0

        for i in self.list:
            i.move(screen)
            for j in aco_l:
                i.touch(j)

        screen.blit(self.image,self.rect)

    def create(self):
        self.list.append(Zidan(5,"Missile.png",self.rect.center))

    def touch(self,point):
        return self.rect.collidepoint(point)

class Zidan(pygame.sprite.Sprite):
    def __init__(self,speed,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.y_speed = speed

    def move(self,screen):
        self.rect.centery -= self.y_speed
        screen.blit(self.image,self.rect)

    def touch(self,aco):
        global score
        if aco.rect.collidepoint(self.rect.center):
            aco.kill()
            score += 10

class Aircraft_other(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [random.randint(50,600),-100]

    def move(self,screen):
        global HP
        self.rect.centery += 3

        if self.rect.centery > screen.get_height():
            HP -= 10
            self.kill()

        screen.blit(self.image,self.rect)
    
    def get_point(self):
        return self.rect.center

    def kill(self):
        global aco_l
        aco_l.remove(self)

class Attack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rects = []
        self.images = []
        cnt = 0
        for i in range(1,13):
            image = pygame.image.load("./Attack/Attack"+str(i)+".png")
            image = pygame.transform.scale2x(image)
            for j in range(3):
                self.images.append(image)
                self.rects.append(image.get_rect())
                self.rects[cnt].center = [475,360]
                cnt += 1
        self.index = 0

    def next_page(self,screen):
        screen.blit(self.images[self.index%36],self.rects[self.index%36])
        self.index += 1
        return self.index % 36 == 0

screen = pygame.display.set_mode([950,720])
bg1 = bg("Space Fight.png",-720,4)
bg2 = bg("Space Fight.png",0,4)

ac = Aircraft_me("Aircraft.png")
acs = [0,0]
HP = 100
score = 0
type_attack = False
atk = Attack()

aco_l = []
bl = [True,]
for i in range(150):
    bl.append(False)

bgm1 = pygame.mixer.Sound("Movie.wav")
bgm1.play(-1)
bgm2 = pygame.mixer.Sound("win.wav")

clock = pygame.time.Clock()
count = 0

keep_going = True
keepgoing = True
while keepgoing and keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepgoing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                acs = [-3,0]
            if event.key == pygame.K_RIGHT:
                acs = [3,0]
            if event.key == pygame.K_UP:
                acs = [0,-3]
            if event.key == pygame.K_DOWN:
                acs = [0,3]
            if event.key == pygame.K_SPACE:
                ac.create()
            if event.key == pygame.K_1:
                if not type_attack and score >= 40:
                    score -= 40
                    type_attack = True

        if event.type == pygame.KEYUP:
            acs = [0,0]

    if random.choice(bl):
        aco = Aircraft_other("Aircraft2.png")
        aco_l.append(aco)
        if len(bl) > 20:
            bl.pop()
    count = 0
    
    bg1.move(screen)
    bg2.move(screen)

    ac.move(acs[0],acs[1],screen,aco_l)
    
    for i in aco_l:
        i.move(screen)
        count += ac.touch(i.get_point())
    keep_going = count == 0 and HP > 0

    if type_attack:
        type_attack = not atk.next_page(screen)
        for i in aco_l:
            i.kill()
            score += 5

    t_HP = "HP:" + str(HP)
    t_score = "Score:" + str(score)
    HP_font = pygame.font.Font(None,60)
    HP_surf = HP_font.render(t_HP,1,(255,255,255))
    score_font = pygame.font.Font(None,60)
    score_surf = score_font.render(t_score,1,(255,255,255))
    screen.blit(HP_surf,[0,0])
    screen.blit(score_surf,[screen.get_width()-score_surf.get_width(),0])

    pygame.display.update()

    clock.tick(250)
    count += 1

bgm1.stop()
if keep_going:
    pygame.quit()
    exit()
final_text1 = 'Game Over'
final_text2 = 'Your final score is: ' + str(score)
bgm2.play(-1)
keepgoing = True
r = random.randint(0,255)
rs = 1
g = random.randint(0,255)
gs = 1
b = random.randint(0,255)
bs = 1
while keepgoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepgoing = False
    screen.fill([r,g,b])
    ft1_font = pygame.font.Font(None,100)
    ft1_surf = ft1_font.render(final_text1,1,(255-r,255-b,255-g))
    ft2_font = pygame.font.Font(None,60)
    ft2_surf = ft2_font.render(final_text2,1,(255-r,255-b,255-g))
    screen.blit(ft1_surf,[screen.get_width()//2 - \
                          ft1_surf.get_width()//2,350])
    screen.blit(ft2_surf,[screen.get_width()//2 - \
                          ft2_surf.get_width()//2,450])
    pygame.display.update()
    if r > 230:
        rs = -2
    if g > 230:
        gs = -1
    if b > 230:
        bs = -3
    
    if r < 26:
        rs = 1
    if g < 26:
        gs = 2
    if b < 26:
        bs = 3
    r += rs
    g += gs
    b += bs
    clock.tick(50)
pygame.quit()
