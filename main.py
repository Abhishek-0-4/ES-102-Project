import pygame
import constants as const
import random
import math
from pygame import mixer

#Intialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((const.screen_width , const.screen_height))
#background music
mixer.music.load('StartScreenBack-less-sound.mp3')

mixer.music.play(-1)

#other sounds
hit_sound=mixer.Sound('hit.wav')
applause_sound=mixer.Sound('applause3.mp3')
point_sound=mixer.Sound('sfx_point.wav')
applause="play"
point='play'



#set the logo/icon
logo= pygame.image.load('air-hockey.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Paddle Bounce')

#blue paddle
blue_image=pygame.image.load('blue_tile.png')
def blue_paddle(x,y):
    screen.blit(blue_image,(x,y))
BX=const.BstartX # blue paddle x coordinate
BY=const.BstartY # blue paddle x coordinate

#red paddle
red_image=pygame.image.load('red_tile.png')
def red_paddle(x,y):
    screen.blit(red_image,(x,y))
RX=const.RstartX  # red paddle x coordinate
RY=const.RstartY  # red paddle y coordinate


#speed change variables
BY_change=0
RY_change=0
paddle_speed=const.original_paddle_speed


#puck
puck_image=pygame.image.load('button.png')
def puck(x,y):
    screen.blit(puck_image, (x,y))
PX=const.centreX # puck x coordinate
PY=const.centreY # puck y coordinate
PX_change=0
PY_change=0
puck_state = 'waiting to start'


#collision checker
collision=0
def hasCollidedwithblue(PX,PY,BX,BY):
    #front collision
    if PX<=const.blue_width and (BY - 2*const.puck_radius) <= PY <= BY + const.blue_height:
        return True

def hasCollidedwithred(PX,PY,RX,RY):
    #front collision
    if PX>= const.screen_width - const.red_width - 2*const.puck_radius and RY - 2*const.puck_radius <= PY <= RY + const.red_height:
        return True

#all the required fonts
score_font = pygame.font.SysFont('frelesansbold.ttf', 32)
point_font = pygame.font.SysFont('frelesansbold.ttf', 64)
dialogue_font = pygame.font.SysFont('frelesansbold.ttf', 16)
medium_dialogue_font = pygame.font.SysFont('frelesansbold.ttf', 22)
big_dialogue_font = pygame.font.SysFont('frelesansbold.ttf', 28)

score_blue=0
score_red=0

game_state='initiating'
game_mode=''
crazy_count=0
movement='normal'




def point_blue(x,y):
    blue_point= point_font.render("Blue +1", True, (0,0,255))
    screen.blit(blue_point, (x,y))

def point_red(x,y):
    red_point= point_font.render("Red +1", True, (255,0,0))
    screen.blit(red_point, (x,y))

running=True
while running:

    screen.fill((243, 231, 180)) #green background
    # screen.blit(background, (const.backgroundX,const.backgroundY))

    pygame.draw.rect(screen, (237,28,36), pygame.Rect(0, 0, 10, 10000))
    pygame.draw.rect(screen, (0,162,232), pygame.Rect(const.screen_width-10, 0, 10, 10000))


#quit game when cross button is pressed
    for event in pygame.event.get():



#choosing the game mode in the opening window:
        if event.type==pygame.KEYDOWN and game_state== 'initiating':
            if event.key==pygame.K_n:
                game_mode="Normal"
                game_state='waiting to start'


        if event.type==pygame.KEYDOWN and game_state== 'initiating':
            if event.key==pygame.K_c:
                game_mode="Crazy"
                game_state='waiting to start'


#reset entire game when space bar is pressed
        if event.type==pygame.KEYDOWN and game_state== 'ended':
            if event.key==pygame.K_SPACE:
                PX=const.centreX
                PY=const.centreY
                score_red=0
                score_blue=0
                puck_state = 'waiting to start'
                game_state = 'initiating'
                applause='play'

#initiating the puck when space bar is pressed:
        if event.type==pygame.KEYDOWN and puck_state == 'waiting to start' and game_state == 'waiting to start':
            if event.key==pygame.K_SPACE:
                PX_change = random.choice([(random.uniform(const.puck_speed/2,const.puck_speed)),(random.uniform(const.puck_speed,const.puck_speed/2))])
                PY_change = random.choice([math.sqrt(math.pow(const.puck_speed,2)-math.pow(PX_change,2)) , -math.sqrt(math.pow(const.puck_speed,2)- math.pow(PX_change, 2))])
                puck_state='moving'
                game_state='running'
                paddle_speed=const.original_paddle_speed
                collision=0
                point="play"

#reset puck position when point is scored by pressing space
        if event.type==pygame.KEYDOWN and puck_state == 'just ended':
            if event.key==pygame.K_SPACE:
                PX=const.centreX
                PY=const.centreY
                puck_state = 'waiting to start'
                game_state = 'waiting to start'


# paddle movement for normal mode
        if game_mode=='Normal':
    # Moving the red paddle with up and down arrow keys
            if event.type == pygame.KEYDOWN and puck_state!='just ended':
                if event.key == pygame.K_UP:
                    RY_change = -paddle_speed
                if event.key == pygame.K_DOWN:
                    RY_change = paddle_speed
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        RY_change = 0

    # Moving the blue paddle with w and s keys
            if event.type == pygame.KEYDOWN and puck_state!='just ended':
                if event.key == pygame.K_w:
                        BY_change = -paddle_speed
                if event.key == pygame.K_s:
                        BY_change = paddle_speed
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        BY_change = 0
# paddle movement for crazy mode
        if game_mode=='Crazy':
# Moving the paddle for noramal:
            if movement=='normal':
            # Moving the red paddle for normal
                if event.type == pygame.KEYDOWN and puck_state!='just ended':
                    if event.key == pygame.K_UP:
                        RY_change = -paddle_speed
                    if event.key == pygame.K_DOWN:
                        RY_change = paddle_speed
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            RY_change = 0

        # Moving the blue paddle for normal
                if event.type == pygame.KEYDOWN and puck_state!='just ended':
                    if event.key == pygame.K_w:
                            BY_change = -paddle_speed
                    if event.key == pygame.K_s:
                            BY_change = paddle_speed
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w or event.key == pygame.K_s:
                            BY_change = 0
# Moving the paddle for crazy
            if movement=='crazy':

        # Moving the red paddle for crazy (reverse the keys. up arrow key moves the paddle down and vica versa)
                if event.type == pygame.KEYDOWN and puck_state!='just ended':
                    if event.key == pygame.K_UP:
                        RY_change = paddle_speed
                    if event.key == pygame.K_DOWN:
                        RY_change = -paddle_speed
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            RY_change = 0

        # Moving the blue paddle for crazy (reverse the keys. up arrow key moves the paddle down and vica versa)
                if event.type == pygame.KEYDOWN and puck_state!='just ended':
                    if event.key == pygame.K_w:
                            BY_change = paddle_speed
                    if event.key == pygame.K_s:
                            BY_change = -paddle_speed
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w or event.key == pygame.K_s:
                            BY_change = 0


#quit game when cross button is pressed
        if event.type == pygame.QUIT:
            running = False

##############################################################################

#implementing blue paddle movement and boundary checking
    BY=BY+BY_change
    if BY<0:
        BY=0
    if BY>270:
        BY=270
    blue_paddle(BX,BY)

#implementing red paddle movement and boundary checking
    RY=RY+RY_change
    if RY<0:
        RY=0
    if RY>270:
        RY=270
    red_paddle(RX,RY)

#implementing puck movementand boundary checking
    PX=PX + PX_change
    PY=PY + PY_change
    if PY > const.screen_height - 35 or PY<3:
        PY_change= -PY_change
        hit_sound.play()
    puck(PX,PY)

#scoring points
    if PX < const.blue_width - 20 and game_state!='ended':
        if puck_state!='just ended':
            score_red=score_red + 1
        PY_change=0
        PX_change=0
        puck_state='just ended'
        RY_change=0
        BY_change=0
        point_red(325, 200)
        dialogue=dialogue_font.render("Press Space to Continue", True, (0,0,0))
        screen.blit(dialogue, (345,260))
        if point=="play":
            point_sound.play()
            point='stop'

    if PX > const.screen_width - const.red_width - 2*const.puck_radius + 20 and game_state!='ended':
        if puck_state!='just ended':
            score_blue = score_blue + 1
        PY_change=0
        PX_change=0
        puck_state='just ended'
        RY_change=0
        BY_change=0
        point_blue(325, 200)
        dialogue=dialogue_font.render("Press Space to Continue", True, (0,0,0))
        screen.blit(dialogue, (340,260))
        if point=="play":
            point_sound.play()
            point='stop'


#bounce back in case of collision
    if hasCollidedwithblue(PX,PY,BX,BY):
        PX = const.blue_width
        PX_change = -PX_change
        collision=collision+1  #note the increase in the number of collisions
        crazy_count=crazy_count+1
        hit_sound.play()

    if hasCollidedwithred(PX,PY,RX,RY):
        PX = const.screen_width - const.red_width - 2*const.puck_radius
        PX_change= -PX_change
        collision=collision+1  #note the increase in the number of collisions
        crazy_count=crazy_count+1
        hit_sound.play()

#increase puck speed after a certain number of collisions
    if collision==5:
        collision=0
        PX_change=PX_change*1.2  #increase component of puck speed
        PY_change=PY_change*1.2  #increase component of puck speed
        paddle_speed=paddle_speed*1.2 #increasing the paddle speeds

#game ends when either player gets to 5 points
    if score_blue==5:
        winner= point_font.render("BLUE WINS!!", True, (0,162,232))
        screen.blit(winner, (260, 200))
        dialogue=dialogue_font.render("Press Space to Start New Game", True, (0,0,0))
        screen.blit(dialogue, (325,260))

        game_state='ended'
        if applause=="play":
            applause_sound.play()
            applause='stop'


    if score_red==5:
        winner= point_font.render("RED WINS!!", True, (255, 0, 0))
        screen.blit(winner, (250, 200))
        dialogue=dialogue_font.render("Press Space to Start New Game", True, (0,0,0))
        screen.blit(dialogue, (325,260))

        game_state='ended'
        if applause=="play":
            applause_sound.play()
            applause='stop'


    if game_state=='initiating':
        dialogue1=big_dialogue_font.render("Press 'C' for Crazy Mode", True, (0,0,0))
        screen.blit(dialogue1, (285,270))
        dialogue2=big_dialogue_font.render("Press 'N' for Normal Mode", True, (0,0,0))
        screen.blit(dialogue2, (280,300))
        dialogue3=dialogue_font.render("In crazy mode, the up-down movement of the paddle will randomly INVERT. Beware!", True, (0,0,0))
        screen.blit(dialogue3, (180,400))
        dialogue4=medium_dialogue_font.render("'w' for up", True, (0,0,0))
        screen.blit(dialogue4, (50,205))
        dialogue5=medium_dialogue_font.render("'s' for down", True, (0,0,0))
        screen.blit(dialogue5, (50,225))
        dialogue6=medium_dialogue_font.render("'up-arrow' for up", True, (0,0,0))
        screen.blit(dialogue6, (600,205))
        dialogue7=medium_dialogue_font.render("'down-arrow' for down", True, (0,0,0))
        screen.blit(dialogue7, (600,225))

    if puck_state == 'waiting to start' and game_state == 'waiting to start':
        dialogue8=dialogue_font.render("Press Space to Start", True, (0,0,0))
        screen.blit(dialogue8, (355,260))


# switching between crazy and normal movements randomly
    if game_mode=="Crazy":
        decider=random.randint(4,8)
        if crazy_count==decider and movement=='normal':
            movement='crazy'
            crazy_count=0
        if crazy_count==decider and movement=='crazy':
            movement='normal'
            crazy_count=0

# displaying game mode at the top
    if game_state!="initiating":
        score=score_font.render(game_mode + ' Mode', True, (0,0,0))
        screen.blit(score, (340,400))







#update score in the loop
    score=score_font.render(str(score_blue) + " : " + str(score_red), True, (0,0,0))
    screen.blit(score, (385,10))

#keep updating the screen
    pygame.display.update()
