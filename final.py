import pygame
import pygame.sprite
import random
import math
import time
import keyboard
from pygame import Rect, key, K_LEFT, K_RIGHT, MOUSEBUTTONDOWN, QUIT

pygame.init()
pygame.mixer.init()
background = pygame.mixer.Sound('background.mp3')  #括弧為音檔名稱
background.set_volume(0.3)  #設定音量大小，參值0~1
background.play(-1)           #播放音效
addstar = pygame.mixer.Sound('score.mp3')
addstar.set_volume(0.3)
minusstuff = pygame.mixer.Sound('strike.mp3')
minusstuff.set_volume(0.6)
passmp3 = pygame.mixer.Sound('pass.mp3')
passmp3.set_volume(0.7)
ground = pygame.mixer.Sound('ontheground.mp3')
ground.set_volume(0.5)
fail = pygame.mixer.Sound('fail.mp3')
fail.set_volume(0.5)
clock = pygame.time.Clock()



#####畫布
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("成為磚家")
bg = (255, 255, 255)



#####全部載入圖片
i1 = pygame.image.load('p1.png')  # 黑色字
i1 = pygame.transform.scale(i1, (50, 50))
i1.convert()
i11 = pygame.image.load('p2.png')  # 紅色字
i11 = pygame.transform.scale(i11, (50, 50))
i11.convert()
i2 = pygame.image.load('first.png')  # 黑色字
i2.convert()
i22 = pygame.image.load('first2.png')  # 紅色字
i22.convert()
i3 = pygame.image.load('second.png')  # 黑色字
i3.convert()
i33 = pygame.image.load('second2.png')  # 紅色字
i33.convert()
i4 = pygame.image.load('third.png')  # 黑色字
i4.convert()
i44 = pygame.image.load('third2.png')  # 紅色字
i44.convert()
rulepic = pygame.image.load('intro.png')
rulepic.convert()
back = pygame.image.load('come.png')  # 黑色字
back.convert()
backk = pygame.image.load('come2.png')  # 紅色字
backk.convert()
aboutus = pygame.image.load('aboutUs.jpg')
aboutus = pygame.transform.scale(aboutus, (700, 421))
aboutus.convert()
superon = pygame.image.load('turn_on.png')
superon = pygame.transform.scale(superon, (60, 30))
superon.convert()
superoff = pygame.image.load('turn_ooff.png')
superoff = pygame.transform.scale(superoff, (60, 30))
superoff.convert()
i2s = pygame.image.load('firsts.png')
i2s = pygame.transform.scale(i2s, (130, 130))
i2s.convert()
i3s = pygame.image.load('seconds.png')
i3s = pygame.transform.scale(i3s, (130, 130))
i3s.convert()
i4s = pygame.image.load('thirds.png')
i4s = pygame.transform.scale(i4s, (130, 130))
i4s.convert()



#####文字
font = pygame.font.SysFont('Constantia', 30)
text_col = (78, 81, 139)   #text color

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



#####磚塊顏色
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
#####板子顏色
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)



#####預設變數們
cols = 15
rows = 6
fps = 60
live_ball = False
game_over = 0
running = True
n1 = True
about = False
run1 = False
run2 = False 
run3 = False
failmusic = 0
supertime = 5
superclick = 0


#####磚塊
class wall():
    def __init__(self):
        self.width = 60
        self.height = 35

    def create_wall(self):
        self.blocks = []
        # define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height + 30
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)



#####板子
class paddle():
    def __init__(self):
        self.reset()
        self.lives = 3  # 生命值

    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

        # 檢查是否碰到掉落物
        for obj in falling_objects:
            if pygame.sprite.collide_rect(self, obj):
                    obj.kill()
                    minusstuff.play()
                    self.lives -= 1
                    if self.lives == 0:
                        global live_ball
                        global game_over
                        live_ball = False
                        game_over = -1
                        
                    #     # 遊戲結束
                    #     draw_text('YOU LOST!', font, text_col,320, screen_height // 2 + 50)
                        
        for obj in fallins:
            if pygame.sprite.collide_rect(self, obj):
                    obj.kill()
                    addstar.play()
                    self.lives += 1
                    
        
        if self.lives >3:
            self.lives =3
        
        if self.lives <=0:
            self.lives =0
            
                    
    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)
        # 繪製生命值
        for i in range(self.lives):
            pygame.draw.rect(screen, (255, 155, 5),
                             (screen_width - 50 - i*30, 5, 20, 20))

    def reset(self):
        # define paddle variables
        self.height = 20
        self.width = 150
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.rect2 = Rect(self.x, self.y, self.width-10, self.height)
        self.rect1 = Rect(self.x, self.y, self.width-20, self.height)
        self.direction = 0
        

def drawCircle():
    for d in range(supertime):
        green = (48,128,20)
        pygame.draw.circle(screen, green, (screen_width-500+d*30,18), 11)



#####球
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)
        self.collision_thresh = 6

    def move(self):

        # collision threshold
        # collision_thresh = 6

        # start off with the assumption that the wall has been destroyed completely
        wall_destroyed = 1
        row_count = 0
        wall_count = 0
        
        #wall_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision碰撞
                if self.rect.colliderect(item[0]):
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < self.collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < self.collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < self.collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < self.collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce the block's strength by doing damage to it
                    if run1 == True:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                    elif run3 == True or run2 == True:
                        if wall.blocks[row_count][item_count][1] > 1:
                            wall.blocks[row_count][item_count][1] -= 1
                        else:
                            wall.blocks[row_count][item_count][0] = (
                                0, 0, 0, 0)

                # check if block still exists, in whcih case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                if wall.blocks[row_count][item_count][0] == (0, 0, 0, 0):
                    wall_count += 1
                # increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wall_count == 84:
            self.game_over = 1
            passmp3.play()

        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1
            ground.play()
            

        # look for collission with paddle
        if self.rect.colliderect(player_paddle):
            # check if colliding from the top
            if abs(self.rect.bottom - player_paddle.rect.top) <= self.collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x +
                           self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x +
                           self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 5
        self.speed_y = -5
        self.speed_max = 6
        self.game_over = 0

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_width()/4), int(self.image.get_height()/4)))  # 缩小图片大小
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0  # 初始化掉落物的初始纵坐标
        self.speed = 3  # 速度

    def update(self):
        self.rect.y += self.speed  # 更新掉落物的纵坐标，使其向下移动
        if self.rect.y > screen_height:
            self.kill()  # 如果掉落物移出屏幕，将其从精灵组中移除



#####呼叫class
wall = wall()
wall.create_wall()
player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width // 2),
                  player_paddle.y - player_paddle.height)
allsprite = pygame.sprite.Group()
falling_objects = pygame.sprite.Group()
fallins = pygame.sprite.Group()



#####執行
while running:
    screen.fill(bg)
    clock.tick(fps)
    

    #####初始畫面
    if n1:
        screen.blit(rulepic, (100, 30))
        buttons = pygame.mouse.get_pressed()  # 偵測滑鼠是否在字上
        x1, y1 = pygame.mouse.get_pos()
        x2, y2 = pygame.mouse.get_pos()
        x3, y3 = pygame.mouse.get_pos()
        x4, y4 = pygame.mouse.get_pos()
        if x2 >= 120 and x2 <= 280 and y2 >= 430 and y2 <= 480:
            screen.blit(i22, (50, 304))  # 紅色字
            screen.blit(i3, (250, 300.5))
            screen.blit(i4, (453, 299))
            screen.blit(i1, (730, 15))
            if buttons[0]:
                n1 = False
                run1 = True
                run2 = False
                run3 = False
                about = False
        elif x3 >= 320 and x3 <= 480 and y3 >= 430 and y3 <= 480:
            screen.blit(i33, (250, 302.5))  # 紅色字
            screen.blit(i2, (50, 303))
            screen.blit(i4, (453, 299))
            screen.blit(i1, (730, 15))
            if buttons[0]:
                n1 = False
                run2 = True
                run1 = False
                run3 = False
                about = False
        elif x4 >= 520 and x4 <= 680 and y4 >= 430 and y4 <= 480:
            screen.blit(i44, (450, 300))  # 紅色字
            screen.blit(i2, (50, 303))
            screen.blit(i3, (250, 300.5))
            screen.blit(i1, (730, 15))
            if buttons[0]:
                n1 = False
                run3 = True
                run1 = False
                run2 = False
                about = False
        elif x1 >= 730 and x1 <= 780 and y1 >= 15 and y1 <= 70:
            screen.blit(i11, (730, 15))  # 紅色字
            screen.blit(i2, (50, 303))
            screen.blit(i3, (250, 300.5))
            screen.blit(i4, (453, 299))
            if buttons[0]:
                about = True
                n1 = False
                run3 = False
                run1 = False
                run2 = False
        else:  # 黑色字
            screen.blit(i2, (50, 303))
            screen.blit(i3, (250, 300.5))
            screen.blit(i4, (453, 299))
            screen.blit(i1, (730, 15))
        pygame.display.update()

        


    #####關於我們
    if about:
        screen.blit(aboutus,(50,70))
        buttons = pygame.mouse.get_pressed()  # 偵測滑鼠是否在字上
        x5, y5 = pygame.mouse.get_pos()
        if x5 >= 30 and x5 <= 50 and y5 >= 10 and y5 <= 30:
            screen.blit(backk, (25, 1))  # 紅色字
            if buttons[0]:
                n1 =True
                about = False
        else:  # 黑色字
            screen.blit(back, (25, 3))
        pygame.display.update()


    ###第一關
    if run1:
        screen.blit(i2s,(50,-50))
        buttons = pygame.mouse.get_pressed()  # 偵測滑鼠是否在字上
        x5, y5 = pygame.mouse.get_pos()
        if x5 >= 30 and x5 <= 50 and y5 >= 10 and y5 <= 30:
            screen.blit(backk, (25, 1))  # 紅色字
            if buttons[0]:
                wall.create_wall()
                player_paddle.lives=3
                live_ball = False
                n1 = True
                run1 = False
        else:  # 黑色字
            screen.blit(back, (25, 3))

        wall.draw_wall()
        player_paddle.draw()
        ball.draw()
        
        if live_ball:
            # draw paddle
            player_paddle.move()
            # draw ball
            game_over = ball.move()
            if game_over != 0:
                live_ball = False
            player_paddle.move()
            allsprite.draw(screen)  # 繪製所有角色
            

        if not live_ball:
            if game_over == 0:  # 剛開始
                draw_text('CLICK ANYWHERE', font,
                        text_col, 270, screen_height // 2 + 100)
                player_paddle.draw()
            elif game_over == 1:  # 贏了
                draw_text('YOU WON!', font, text_col, 320, screen_height // 2 + 50)
                background.stop()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        n1 = True
                        background.play()
                        wall.create_wall()
                        player_paddle.lives=3
                        ball.reset(player_paddle.x + (player_paddle.width // 2),
                                player_paddle.y - player_paddle.height)
                        player_paddle.reset()
                        game_over = 0
                        run1 = False
            elif game_over == -1:  # 開始後掉落    
                if player_paddle.lives >1 :        
                    player_paddle.lives -= 1
                    game_over = 0
                    
                else:
                    player_paddle.lives -= 1
                    if player_paddle.lives <0:
                        player_paddle.lives =0
        if  player_paddle.lives == 0:
            draw_text('YOU LOST!', font, text_col,320, screen_height // 2 + 50)
            if failmusic == 0:
                background.stop()
                fail.play(0)
                failmusic = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives > 0:
                live_ball = True
                ball.reset(player_paddle.x + (player_paddle.width // 2),
                        player_paddle.y - player_paddle.height)
                player_paddle.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives == 0:
                run1 = False
                n1 = True
                player_paddle.lives=3
                wall.create_wall()
                ball.reset(player_paddle.x + (player_paddle.width // 2),
                        player_paddle.y - player_paddle.height)
                player_paddle.reset()
                failmusic = 0
                background.play()

    #####第二關
    if run2 == True:
        screen.blit(i3s,(50,-50))
        buttons = pygame.mouse.get_pressed()  # 偵測滑鼠是否在字上
        x5, y5 = pygame.mouse.get_pos()
        if x5 >= 30 and x5 <= 50 and y5 >= 10 and y5 <= 30:
            screen.blit(backk, (25, 1))  # 紅色字
            if buttons[0]:
                wall.create_wall()
                player_paddle.lives=3
                live_ball = False
                n1 =True
                run2 = False
        else:  # 黑色字
            screen.blit(back, (25, 3))

        # draw all objects
        wall.draw_wall()
        player_paddle.draw()
        ball.draw()

        if live_ball:
            # draw paddle
            player_paddle.move()
            # draw ball
            game_over = ball.move()
            if game_over != 0:
                live_ball = False
            # randomly add falling object
            if random.random() < 0.003:
                num = random.randint(1, 3)
                n = str(num)
                falling_object = FallingObject('random_drop_'+n+'.png')
                falling_objects.add(falling_object)
            player_paddle.move()
            falling_objects.update()
            falling_objects.draw(screen)
            allsprite.draw(screen)  # 繪製所有角色
        
        if not live_ball:
            if game_over == 0:  # 剛開始
                draw_text('CLICK ANYWHERE', font,
                        text_col, 270, screen_height // 2 + 100)
            elif game_over == 1:  # 贏了
                draw_text('YOU WON!', font, text_col, 320, screen_height // 2 + 50)
                background.stop()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        n1 = True
                        background.play()
                        wall.create_wall()
                        player_paddle.lives=3
                        ball.reset(player_paddle.x + (player_paddle.width // 2),
                                player_paddle.y - player_paddle.height)
                        player_paddle.reset()
                        game_over = 0
                        run2 = False
            elif game_over == -1:  # 開始後掉落    
                if player_paddle.lives >1 :        
                    player_paddle.lives -= 1
                    game_over = 0
                else:
                    player_paddle.lives -= 1
                    if player_paddle.lives <0:
                        player_paddle.lives =0
        if  player_paddle.lives == 0:
            draw_text('YOU LOST!', font, text_col,320, screen_height // 2 + 50)
            if failmusic == 0:
                background.stop()
                fail.play(0)
                failmusic = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives > 0 :
                    live_ball = True
                    ball.reset(player_paddle.x + (player_paddle.width // 2),
                            player_paddle.y - player_paddle.height)
                    player_paddle.reset()
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives == 0:
                run2 = False
                n1 = True
                wall.create_wall()
                player_paddle.lives=3
                ball.reset(player_paddle.x + (player_paddle.width // 2),
                        player_paddle.y - player_paddle.height)
                player_paddle.reset()
                failmusic = 0
                background.play()

        pygame.display.update()

    #####第三關
    if run3 == True:
        drawCircle()
        screen.blit(i4s,(50,-50))
        hotkey1 = "space"
        def action1():
            ball.collision_thresh=5
        buttons = pygame.mouse.get_pressed()  # 偵測滑鼠是否在字上
        x5, y5 = pygame.mouse.get_pos()
        if x5 >= 30 and x5 <= 50 and y5 >= 10 and y5 <= 30:
            screen.blit(backk, (25, 1))  # 紅色字
            if buttons[0]:
                wall.create_wall()
                player_paddle.lives=3
                live_ball = False
                n1 =True
                run3 = False
        else:  # 黑色字
            screen.blit(back, (25, 3))

        # draw all objects
        wall.draw_wall()
        player_paddle.draw()
        ball.draw()
        screen.blit(superoff,(180,0))

        if live_ball:
            # draw paddle
            player_paddle.move()
            # draw ball
            game_over = ball.move()
            if game_over != 0:
                live_ball = False
            # randomly add falling object
            if random.random() < 0.005:
                num = random.randint(1, 3)
                n = str(num)
                falling_object = FallingObject('random_drop_'+n+'.png')
                falling_objects.add(falling_object)

            if random.random() < 0.003:
                num = random.randint(1, 3)
                n = str(num)
                fallin = FallingObject('star.png')
                fallins.add(fallin)

            # 檢查是否有觸發特定功能的按鍵被按下
            if supertime > 0:
                if keyboard.is_pressed(hotkey1):
                    action1()
                    screen.blit(superon,(180,0))
                    superclick = 1
                if not keyboard.is_pressed(hotkey1):
                    ball.collision_thresh = 6
                    if superclick == 1:
                        superclick = 0
                        supertime -= 1

            player_paddle.move()    
            falling_objects.update()
            falling_objects.draw(screen)
            fallins.update()
            fallins.draw(screen)
            allsprite.draw(screen)  # 繪製所有角色

        if not live_ball:
            if game_over == 0:  # 剛開始
                draw_text('CLICK ANYWHERE', font,
                        text_col, 270, screen_height // 2 + 100)
            elif game_over == 1:  # 贏了
                draw_text('YOU WON!', font, text_col, 320, screen_height // 2 + 50)
                background.stop()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        n1 = True
                        background.play()
                        wall.create_wall()
                        player_paddle.lives=3
                        ball.reset(player_paddle.x + (player_paddle.width // 2),
                                player_paddle.y - player_paddle.height)
                        player_paddle.reset()
                        game_over = 0
                        run3 = False

            elif game_over == -1:  # 開始後掉落    
                if player_paddle.lives >1 :        
                    player_paddle.lives -= 1
                    game_over = 0
                else:
                    player_paddle.lives -= 1
                    if player_paddle.lives <0:
                        player_paddle.lives =0
                
        if  player_paddle.lives == 0:
            draw_text('YOU LOST!', font, text_col,320, screen_height // 2 + 50)
            if failmusic == 0:
                background.stop()
                fail.play(0)
                failmusic = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives > 0 :
                    live_ball = True
                    ball.reset(player_paddle.x + (player_paddle.width // 2),
                            player_paddle.y - player_paddle.height)
                    player_paddle.reset()

                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and player_paddle.lives == 0:
                n1 = True
                wall.create_wall()
                player_paddle.lives=3
                ball.reset(player_paddle.x + (player_paddle.width // 2),
                        player_paddle.y - player_paddle.height)
                player_paddle.reset()
                failmusic = 0
                background.play()
                run3 = False
                supertime = 5

        pygame.display.update()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()

pygame.quit()
