#Step2, Load background and cargo

# 1.1 - Import library
import pygame
import random
import math
import time
pygame.init()
width, height = 740, 480
screen=pygame.display.set_mode((width, height))
keep_going = True

score=0
life=3
game_over=False


#3.1 initial the value of Key and position
key_up=key_down=key_left=key_right = False
player_pos=[130,100] #change the position to list

player = pygame.image.load("images/player.png")

#2.1 load more images
background = pygame.image.load("images/sky.jpg")
background = pygame.transform.scale(background, (width, height))
cargo = pygame.image.load("images/airballoon.png")


bullets=[]
bullet = pygame.image.load("images/bullet.png")

#5 initial enemies
enemyImg = pygame.image.load("images/enemy2.png")
enemyImg=pygame.transform.scale(enemyImg, (100, 33)).convert_alpha()  #use the convert_alpha() method after loading so that the image has per pixel transparency.
enemys=[[640,100]]
enemySpeed=-0.8
enemyMaxnumber=5 #how many enemies in the screen same time

#7 initial load explosion animaton images
explosions=[] # store explosion location and img index [(x,y),i,t] 
explosion_anim=[] #store img for animation
BLACK = (0, 0, 0)
explosion_time=60

RED=(255,0,0)

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(pygame.font.match_font('typewriter'), size)
    text_surface = font.render(text, True, RED)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

for i in range(9):
    filename = 'Explosion0{}.png'.format(i)
    img = pygame.image.load("images/"+ filename).convert()  # convert will create a copy that will draw more quickly on the screen.
    img.set_colorkey(BLACK)
    img= pygame.transform.scale(img, (75, 75))
    explosion_anim.append(img)
    
    
#8 initial load sound
shooting_sound = pygame.mixer.Sound('sounds/pew.wav')
pygame.mixer.music.load('sounds/BG.ogg')
pygame.mixer.music.play(-1) ## makes the gameplay sound in an endless loop

# 1.4 - use loop to keep the game running 

    
while keep_going:

    screen.fill(0)
    
    #2.2 load the background
    screen.blit(background,(0,0))
    
    # if you image is small, you need use double loop to fill the background
    #for x in range( int(width/background.get_width())+1):
    #    for y in range(int(height/background.get_height())+1):
    #        screen.blit(background,(x*100,y*100))
    
    # 2.3 load the cargo
    screen.blit(cargo,(0,30))
    screen.blit(cargo,(0,135))
    screen.blit(cargo,(0,240))
    screen.blit(cargo,(0,345))

    
#step 9 draw life and score on    
    game_over=life<1 #step9 make game over if life small then 1
    draw_text(screen, "Score: "+str(score), 30, width -100, 10)
    draw_text(screen, "Life: "+str(life), 30, width/2, 10)
    if(game_over):
        draw_text(screen, "Game Over", 100, width/2, height/2 -40)
        
        
#3.2 set player position use player_pos

    if(not game_over):
        screen.blit(player, player_pos)    
#4 - Draw bullet
    
    for bulletPos in bullets:
        enemy_index=0
        bulletPos[0]=bulletPos[0]+2
        screen.blit(bullet,bulletPos)

        #remove bullet if out the screen
        if bulletPos[0]<-64 or bulletPos[0]>640 or bulletPos[1]<-64 or bulletPos[1]>480:
            bullets.pop(enemy_index)  #remove from list
        enemy_index+=1


     #5 Draw enemies random time and only keep 5 enemies in screen
    if(random.randint(1,100)<3 and len(enemys)<enemyMaxnumber): 
        enemys.append([640, random.randint(50,430)])
        print("enemys length"+str(len(enemys)))

    enemy_index=0
    for enemyPos in enemys:               
        enemyPos[0]+=enemySpeed
        if enemyPos[0]<50:
            enemys.pop(enemy_index)
        screen.blit(enemyImg, enemyPos)
        
    # 6 Check for collistions
        enemyRect=pygame.Rect(enemyImg.get_rect())
        enemyRect.left=enemyPos[0]
        enemyRect.top=enemyPos[1]
        bullet_index=0
        for bulletPos in bullets:
            bulletRect=pygame.Rect(bullet.get_rect()) # get rect of bullet image size
            bulletRect.left=bulletPos[0]
            bulletRect.top=bulletPos[1]            
            if bulletRect.colliderect(enemyRect):
                enemys.pop(enemy_index)
                bullets.pop(bullet_index)
                # step7 play explosion in the location of enemy
                explosions.append([enemyPos,0,explosion_time])
                score+=1
                                
           
            bullet_index+=1

        if(not game_over):
            playerRect=pygame.Rect(player.get_rect())
            playerRect.left=player_pos[0]
            playerRect.top=player_pos[1]
            if(playerRect.colliderect(enemyRect)):
                explosions.append([player_pos,0,explosion_time])
                enemys.pop(enemy_index)
                life-=1
        #end step 9
    # end step 6           
        enemy_index+=1
        
#end step 5

    #step 7 plan explosion animation    
    for explosion in explosions:
        if(explosion[1]<9):
            screen.blit(explosion_anim[explosion[1]],explosion[0])
            explosion[2]=explosion[2]-1
            if(explosion[2]<0):     
                explosion[1]=explosion[1]+1
                explosion[2]=explosion_time
                
        else:
            explosions.pop(0) # the first one is always first completed 
    #end step7

    #1.7 - update the screen
    pygame.display.flip() #faster the .update()
    # 1.8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type==pygame.QUIT:
            keep_going = False
#3.3 monitor the key down and up
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_w:
                key_up=True
            elif event.key==pygame.K_a:
                key_left=True
            elif event.key==pygame.K_s:
                key_down=True
            elif event.key==pygame.K_d:
                key_right=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                key_up=False
            elif event.key==pygame.K_a:
                key_left=False
            elif event.key==pygame.K_s:
                key_down=False
            elif event.key==pygame.K_d:
                key_right=False


# use mouse down to fire         
        if event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
            bullets.append([player_pos[0],player_pos[1]])
            shooting_sound.play()
            

#3.4 - Move player base on the key status
    if key_up and player_pos[1]>0:
        player_pos[1]-=1
    elif key_down and player_pos[1]<height-30:
        player_pos[1]+=1
    if key_left and player_pos[0]>0:
        player_pos[0]-=1
    elif key_right and player_pos[0]<width-100:
        player_pos[0]+=1




        

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            keep_going = False

    if (game_over):
        time.sleep(5)
        pygame.quit()


pygame.quit()
exit(0) 
