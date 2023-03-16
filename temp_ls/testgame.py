import pygame
import random 
import button
from pygame import mixer

pygame.init()
pygame.display.set_caption("Raging Rampage")

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
#panel image
panel_img = pygame.image.load("images/panel/panel.png").convert_alpha()
statpanel_img = pygame.image.load("images/panel/statpanel.png").convert_alpha()
#button image
potion_img = pygame.image.load("images/icons/potion.png").convert_alpha()
restart_img = pygame.image.load("images/icons/restart.png").convert_alpha()
#load win and lose image
victory_img = pygame.image.load("images/icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("images/icons/defeat.png").convert_alpha()
#sword cursor
sword_img = pygame.image.load("images/icons/cursor.png").convert_alpha()

#func for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#func for drawing bg
def draw_bg():
    screen.blit(background_img, (0, 0))

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
        for i in range(4):
        #Idle Image loading and scale // scaling size by * 2
            img = pygame.image.load(f"images/{self.name}/idle/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #ATTACK ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for i in range(4):
        #Idle Image loading and scale // scaling size by * 2
            img = pygame.image.load(f"images/{self.name}/attack/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Take hit ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for i in range(3):
        #Idle Image loading and scale // scaling size by * 2
            img = pygame.image.load(f"images/{self.name}/takehit/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() *2, img.get_height() * 2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #death ANIMATION
        #temp list for all images
        temp_list = []
        #How many pictures there is in one animation
        for i in range(5):
        #Idle Image loading and scale // scaling size by * 2
            img = pygame.image.load(f"images/{self.name}/death/{i}.png")
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
        pygame.mixer.init()
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
        self.xp = 0
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
          self.rect.center = (x, y)
          self.counter = 0

     def update(self):
        #move dmg text up
        self.rect.y -= 1
        #delete text after a few s
        self.counter += 1
        if self.counter > 30:
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

#button instances
potion_button = button.Button(screen, 29, 393, potion_img, 50, 50)
restart_button = button.Button(screen, 315, 80, restart_img, 120, 30)

maingame = True
while maingame:

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
    #make sure mouse is visdible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, skeleton in enumerate(skeleton_list):
        if skeleton.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword instead of cursor
            screen.blit(sword_img, pos)
            if clicked == True:
                attack = True
                target = skeleton_list[count]


    if potion_button.draw():
        potion = True


    #how many pots
    draw_text(str(hero.potions), font, red, 68, 382)

    if game_over == 0:
        #player action
        if hero.alive == True:
            if current_fighter == 1:
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
            maingame = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
