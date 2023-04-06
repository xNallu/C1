import pygame
import random 
import button
import sys
import time
import os
from pygame import mixer

#Mostly fix for VSC not importing assets.
absFilePath = os.path.abspath(__file__)
os.chdir( os.path.dirname(absFilePath) )


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Paddy")

#FPS speed
clock = pygame.time.Clock()
fps = 60

#game window 
bottom_panel = 70
stat_panel = 200

screen_width = 700 + stat_panel
screen_height =  400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

#fonts
font = pygame.font.SysFont("Times New  Roman", 26)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
orange = (226, 150, 62)
black = (0, 0, 0)

#game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 80
potion_effect = 15
attack = False
potion = False
clicked = False
game_over = 0



#loading images
#background img
background_img = pygame.image.load("images/background/background.png").convert_alpha()
mainmenu_img = pygame.image.load("images/background/mainmenu.png").convert_alpha()
difficulty_img = pygame.image.load("images/background/difficultymenu.png").convert_alpha()
optionsmenu_img = pygame.image.load("images/background/optionsmenu.png").convert_alpha()
#panel image
panel_img = pygame.image.load("images/panel/panel.png").convert_alpha()
statpanel_img = pygame.image.load("images/panel/statpanel.png").convert_alpha()
#button images
potion_img = pygame.image.load("images/icons/potion.png").convert_alpha()
restart_img = pygame.image.load("images/icons/restart.png").convert_alpha()
play_img = pygame.image.load("images/icons/play.png").convert_alpha()
options_img = pygame.image.load("images/icons/options.png").convert_alpha()
quit_img = pygame.image.load("images/icons/quit.png").convert_alpha()
back_img = pygame.image.load("images/icons/back.png").convert_alpha()
#load win and lose image
victory_img = pygame.image.load("images/icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("images/icons/defeat.png").convert_alpha()
#sword cursor
sword_img = pygame.image.load("images/icons/cursor.png").convert_alpha()

#Sounds and music 
clicksound = pygame.mixer.Sound("images/sounds/click.mp3")
mmusic = pygame.mixer.music.load("images/sounds/mmusic.ogg")


gmusic1 = pygame.mixer.Sound("images/sounds/gmusic1.ogg")
gmusic2 = pygame.mixer.Sound("images/sounds/gmusic2.ogg")
gmusic3 = pygame.mixer.Sound("images/sounds/gmusic3.ogg")
gmusic4 = pygame.mixer.Sound("images/sounds/gmusic4.ogg")
gmusics = [gmusic1, gmusic2, gmusic3, gmusic4]
selected_gmusic = random.choice(gmusics)

#func for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#func for drawing bg
def draw_bg():
    screen.blit(background_img, (0, 0))

#func for drawing mainmenu
def mainmenu_bg():
    screen.blit(mainmenu_img, (0, 0))

#func for drawing difficulty menu
def difficulty_bg():
    screen.blit(difficulty_img, (0, 0))

#func for drawing options menu
def optionsmenu_bg():
    screen.blit(optionsmenu_img, (0, 0))

#func for drawing panel
def draw_panel():
    # draw panel rect
    screen.blit(panel_img, (0, 360))
    #hero hp
    draw_text(f"{hero.name} HP: {hero.hp}",font, red, 100, screen_height - bottom_panel - 20)
    #Skeleton hp
    for count, i in enumerate(skeleton_list):
        draw_text(f"{i.name} HP: {i.hp}",font, red, 450, (screen_height - bottom_panel - 20) + count * 30)

#func for stat panel
def draw_statpanel():
    screen.blit(statpanel_img, (700, 0))

    draw_text("STATS",font, black, 760, 25)
    draw_text("Attack: 5-15",font, orange, 732, 50)
    draw_text(f"{hero.name} XP: {hero.xp}",font, orange, 732, 70)



#Classes
# fighter class
# Properties for fighters
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions,xp):
        self.name = name

        #Stats
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.xp = xp

        #Health pots
        self.start_potions = potions
        self.potions = potions

        #Spawns fighter as alive
        self.alive = True

        #Empty animation_list // what frame of anim
        self.animation_list = []
        self.frame_index = 0

        # What animation set to use
        # 0:idle 1:attack 2:take hit 3: dead
        self.action = 0

        #clock for anim
        self.update_time = pygame.time.get_ticks()


        #IDLE ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for filename in os.listdir(f"images/{self.name}/idle/"):
            if filename.endswith(".png"):
        #idle Image loading and scale // scaling size by * 2
                img = pygame.image.load(f"images/{self.name}/idle/{filename}")
                img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
                temp_list.append(img)
        self.animation_list.append(temp_list)

        #ATTACK ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for filename in os.listdir(f"images/{self.name}/attack/"):
            if filename.endswith(".png"):
        #attack Image loading and scale // scaling size by * 2
                img = pygame.image.load(f"images/{self.name}/attack/{filename}")
                img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
                temp_list.append(img)
        self.animation_list.append(temp_list)

        #Take hit ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for filename in os.listdir(f"images/{self.name}/takehit/"):
            if filename.endswith(".png"):
        #take hit Image loading and scale // scaling size by * 2
                img = pygame.image.load(f"images/{self.name}/takehit/{filename}")
                img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
                temp_list.append(img)
        self.animation_list.append(temp_list)

        #death ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for filename in os.listdir(f"images/{self.name}/death/"):
            if filename.endswith(".png"):
        #death Image loading and scale // scaling size by * 2
                img = pygame.image.load(f"images/{self.name}/death/{filename}")
                img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
                temp_list.append(img)
        self.animation_list.append(temp_list)



        self.image = self.animation_list[self.action][self.frame_index]
        
        #pos
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        #Animation speed
        animation_cooldown = 150
        #handle animation and updating img
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last anim update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation img count at max, reset anim
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:   
                self.idle()



    # Animations for actions
    # func for resetting anim back to idle after action
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #deal dmg to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt anim
        target.hurt()


        #Sword hit sounds
        sword1 = pygame.mixer.Sound("images/sounds/sword1.mp3")
        sword2 = pygame.mixer.Sound("images/sounds/sword2.mp3")
        sounds = [sword1, sword2]
        selected_sound = random.choice(sounds)
        selected_sound.play()


        
        #check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
            self.xp += 10
                   
        #damage text
        damage_text = DamageText(target.rect.centerx, target.rect.y - 10, str(damage), red)
        damage_text_group.add(damage_text)

        #set variable to attack anim
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        #Reset xp
        #self.xp = 0
        self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(self.image, self.rect)

#healthbar
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp



    def draw(self, hp):
        #update with new hp
        self.hp = hp
        #calculate hp bar ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 100, 15))
        pygame.draw.rect(screen, green, (self.x, self.y, 100 * ratio, 15))

#damage text
class DamageText(pygame.sprite.Sprite):
     def __init__(self, x, y, damage, colour):
          pygame.sprite.Sprite.__init__(self)
          self.image = font.render(damage, True, colour)
          self.rect = self.image.get_rect()
          self.rect.center = (x + 11, y)
          self.counter = 0

     def update(self):
        #move dmg text up
        self.rect.y -= 1
        #delete text after a few s
        self.counter += 1
        if self.counter > 40:
            self.kill()

     
#button
class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
                                
				self.clicked = True
                                
                


		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return 



damage_text_group = pygame.sprite.Group()

# INSTANCES
#Making the fighter instances
#POS/IMG/HP/STRENGTH/HPPOTS/XP


hero = Fighter(150, 240, "Hero", 30, 10, 3,0)

skeleton1 = Fighter(400, 270, "Skeleton", 20, 5, 0,0)
skeleton2 = Fighter(540, 260, "Skeleton", 20, 5, 0,0)

# Skeleton instances
skeleton_list = []
skeleton_list.append(skeleton1)
skeleton_list.append(skeleton2)

# Hp bar instances
hero_health_bar = HealthBar(95, 150, hero.hp, hero.max_hp)
skeleton1_health_bar = HealthBar(370, 150, skeleton1.hp, skeleton1.max_hp)
skeleton2_health_bar = HealthBar(505, 140, skeleton2.hp, skeleton2.max_hp)


### BUTTONS
#button instances
potion_button = button.Button(screen, 29, 393, potion_img, 50, 50)
restart_button = button.Button(screen, 315, 80, restart_img, 120, 30)

#menu buttons
play_button = button.Button(screen, 332, 85, play_img, 240, 64)
options_button = button.Button(screen, 332, 198, options_img, 240, 64)
quit_button = button.Button(screen, 332, 301, quit_img, 240, 64)
back_button = button.Button(screen, 0, 0, back_img, 150, 34)

#difficulty play buttons
normal_button = button.Button(screen, 118, 352, play_img, 195, 64)



#Game state manager
# 1.Mmenu 2.Difficulty 3.Options 4.Mgame
mode = "Mmenu"

#Music for main menu
if mode == "Mmenu":
    pygame.mixer.music.play(loops = -1, fade_ms= 10000)
    pygame.mixer.music.set_volume(0.3)

mainloop = True
# MAIN Loop
while mainloop == True:
    if mode == "Mmenu":
        clock.tick(fps)

        #drawing menu
        mainmenu_bg()

        #Draws play button
        if play_button.draw():
            mode = "Difficulty"

            #plays clicksound
            clicksound.play()

        #Draws option button
        if options_button.draw():
            mode = "Options"

            #plays clicksound
            clicksound.play()

        #Draws quit button
        if quit_button.draw():

            #plays clicksound and wait before exit
            clicksound.play()
            time.sleep(0.1)

            mainloop = False

        # event checker loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

    # DIFFICULTY SCREEN LOOP
    elif mode == "Difficulty":

        clock.tick(fps)

        #drawing difficulty select screen
        difficulty_bg()

        #Draws play button
        if normal_button.draw():
            mode = "Mgame"

            #plays clicksound
            clicksound.play()
            #Stops menu music
            pygame.mixer.music.stop()
            selected_gmusic.play()

        #Draws back button
        if back_button.draw():
            mode = "Mmenu"

            #plays clicksound
            clicksound.play()

        # event checker loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

    # OPTIONS SCREEN LOOP
    elif mode == "Options":

        clock.tick(fps)

        #drawing options menu
        optionsmenu_bg()

        #Draws back button
        if back_button.draw():
            mode ="Mmenu"

             #plays clicksound
            clicksound.play()
            
            # event checker loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


    # MAIN GAME LOOP
    while mode == "Mgame":
        
        #setting fps to game
        clock.tick(fps)

        #draw bg
        draw_bg()
        #draw panel
        draw_panel()
        #draw statpanel
        draw_statpanel()
        #draw healthbars
        hero_health_bar.draw(hero.hp)
        skeleton1_health_bar.draw(skeleton1.hp)
        skeleton2_health_bar.draw(skeleton2.hp)

        #draw fighters
        hero.update()
        hero.draw()
        for skeleton in skeleton_list:
            skeleton.draw()
            skeleton.update()

        #draw dmg text
        damage_text_group.update()
        damage_text_group.draw(screen)



        #control player actions
        #reset action variables
        attack = False
        potion = False
        target = None
        #make sure mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, skeleton in enumerate(skeleton_list):
            if skeleton.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword instead of cursor
                screen.blit(sword_img, pos)
                if clicked == True and skeleton.alive == True:
                    attack = True
                    target = skeleton_list[count]


        #Draw potion button
        if potion_button.draw():
            potion = True

        #how many pots
        draw_text(str(hero.potions), font, red, 68, 382)

        if game_over == 0:
            #player action
            if hero.alive == True:
                if current_fighter == 1:


                    
                    #drawing arrow for turn - left middle right and drawing the shaft of the arrow
                    pygame.draw.polygon(screen, orange,[(115, 100), (145, 130), (175, 100)])
                    rect_width = 15
                    rect_height = 50
                    rect_x = 115 + (175 - 115 - rect_width) / 2
                    rect_y = 100 - rect_height
                    pygame.draw.rect(screen, orange, (rect_x, rect_y, rect_width, rect_height))

                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # look for player action
                        #attack
                        if attack == True and target != None:
                            hero.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        #potion
                        if potion == True:
                            if hero.potions > 0:
                                # check if pot heal exceeds max hp
                                if hero.max_hp - hero.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = hero.max_hp - hero.hp
                                hero.hp += heal_amount
                                hero.potions -= 1

                                #potion sound
                                potionsound = pygame.mixer.Sound("images/sounds/bottle.ogg")
                                potionsound.play()

                                damage_text = DamageText(hero.rect.centerx, hero.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)

                                current_fighter += 1
                                action_cooldown = 0    
            else:
                game_over = -1


            #enemy action
            for count, skeleton in  enumerate(skeleton_list):
                if current_fighter == 2 + count:
                    if skeleton.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            #attack
                            skeleton.attack(hero)
                            current_fighter += 1
                            action_cooldown = 0

                    else:
                        current_fighter += 1

            #if all fighters done their turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1


        #check if all enemies are dead
        alive_skeletons = 0 
        for skeleton in skeleton_list:
            if skeleton.alive == True:
                alive_skeletons += 1
        
        if alive_skeletons == 0:
            game_over = 1

        
        #check if game is over and display image
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (230, 10))

                # IF WANT ENDLESS
                #for skeleton in skeleton_list:
                #    skeleton.reset()
                #current_fighter = 1
                #action_cooldown
                #alive_skeletons = 2
                #game_over = 0

            if game_over == -1:
                screen.blit(defeat_img, (250, 10))
            if restart_button.draw():
                hero.reset()
                for skeleton in skeleton_list:
                    skeleton.reset()
                current_fighter = 1
                action_cooldown
                game_over = 0



    # event checker loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

    # Return to mmenu if press esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode = "Mmenu"
                    time.sleep(0.1)
                    #resumes menu music again
                    pygame.mixer.stop()
                    pygame.mixer.music.play(loops = -1, fade_ms= 10000)
                    pygame.mixer.music.set_volume(0.3)

        pygame.display.update()

pygame.quit()


