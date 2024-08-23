import pygame 
import random
import math

pygame.init()

#BGM
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.set_volume(0.1) 
pygame.mixer.music.play(loops=-1)#ループプレイ
#ヒット効果音
bao_sound = pygame.mixer.Sound('jz.mp3')

#1 背景表示
bg=pygame.image.load('bg.jpg')
bgpos=bg.get_rect() 
size=width,height=1024, 576 
screen=pygame.display.set_mode(size) 
pygame.display.set_caption("東洋大学用プログラム")

#スコア
score = 0
font = pygame.font.Font('freesansbold.ttf',32)

def show_score():
    text = f"Score: {score}"
    score_render = font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10))

#2 プレーヤー設定 
wanjia=pygame.image.load('wanjia.gif')#プレイヤーの初期位置
wanjiaX = 525
wanjiaY = 470
wanjiaStepX = 0#プレイヤーの移動速度
wanjiaStepY = 0
    
#敵
number_of_enemies = 8#敵の数

#エンドゲーム
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64)
def check_is_over():
    if is_over:
        text = "GAME OVER !"
        render = over_font.render(text,True,(255,0,0))
        screen.blit(render,(330,220))


#ピタゴラスの定理で計算される弾丸と敵との距離
def distance1(bx,by,ex,ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a*a + b*b)

#敵とプレイヤーとの距離
def distance2(cx,cy,ex,ey):
    c = cx - ex
    d = cy - ey
    return math.sqrt(c*c + d*d)


#敵クラス
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('enemy.png')
        self.x = random.randint(225,700)
        self.y = random.randint(100,200)
        self.stepx = random.randint(1,2)
        self.stepy = random.randint(1,2)
    #射撃時の位置を復元
    def reset(self):
        self.x = random.randint(225,700)
        self.y = random.randint(100,150)
        
    def bump(self):#敵がプレイヤーと衝突する
            global is_over
            for e in enemies:
                if (distance2(self.x,self.y,wanjiaX,wanjiaY)  < 30):
                    is_over = True
                    enemies.clear()
                    print("GAME OVER !")
                      
        
enemies = []
for i in range (number_of_enemies):
    enemies.append(Enemy())



#弾丸クラス
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = wanjiaX +29.5 #(wanjia-bullet)/2
        self.y = wanjiaY + 10
        self.step = 4 #弾丸の速さ
     #打つ
    def hit(self):
        global score
        for e in enemies:
            if(distance1(self.x,self.y,e.x,e.y) < 30):
                #アフターショット
                bao_sound.play()
                bullets.remove(self)
                e.reset()
                score += 1#ヒットボーナスポイント
                print(score)
             
bullets = [] #既存の弾丸を保存

#弾丸の表示と移動
def show_bullets():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y))
        b.hit()#敵に当たるか確認する
        b.y -= b.step
        
        #弾丸が範囲外にあるかどうかを判断し、範囲外にある場合は削除
        if b.y < 0:
            bullets.remove(b)


#敵を表示して動かす
def show_enemy():#範囲外を防ぐ
    for e in enemies:
        screen.blit(e.img,(e.x,e.y))
        e.bump()
        e.x += e.stepx
        e.y += e.stepy
        if(e.x > 978 or e.x < 0):
            e.stepx *= -1
        if(e.y> 512 or e.y < 0):
            e.stepy *= -1

def move_wanjia():
    global wanjiaX,wanjiaY
    wanjiaX += wanjiaStepX
    wanjiaY += wanjiaStepY

    if wanjiaX > 959:#範囲外を防ぐ
        wanjiaX = 959
    if wanjiaX < 0:
        wanjiaX = 0
    if wanjiaY > 497:
        wanjiaY = 497
    if wanjiaY < 0:
        wanjiaY=0

      
#メインループ
running = True
while running:
    screen.blit(bg,(0,0))
    show_score()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        #機体の左右の動きを制御するボタンを設定します
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                wanjiaStepX = 4
            elif event.key == pygame.K_LEFT:
                wanjiaStepX = -4
            elif event.key == pygame.K_SPACE:
                print('弾丸発射...')
                     #弾丸を作成する
                bullets.append(Bullet())
                
        if event.type == pygame.KEYUP:
            wanjiaStepX = 0
        #機体を上下に動かすためのボタンを設定します
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                wanjiaStepY = -4
            elif event.key == pygame.K_DOWN:
                wanjiaStepY = 4
        if event.type == pygame.KEYUP:
            wanjiaStepY = 0
        
    screen.blit(wanjia,(wanjiaX,wanjiaY))#プレイヤーの初期位置
    
    move_wanjia()
    show_enemy()
    show_bullets()
    check_is_over()
    pygame.display.update()
