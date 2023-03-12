import pygame
import random 
import button

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

#game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
potion_effect = 15
attack = False
potion = False
clicked = False



#loading images
#background img
background_img = pygame.image.load("images/background/background.png").convert_alpha()
#panel image
panel_img = pygame.image.load("images/panel/panel.png").convert_alpha()
#button image
potion_img = pygame.image.load("images/icons/potion.png").convert_alpha()
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
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #hero hp
    draw_text(f"{hero.name} HP: {hero.hp}",font, red, 100, screen_height - bottom_panel + 10)
    #Skeleton hp
    for count, i in enumerate(skeleton_list):
        draw_text(f"{i.name} HP: {i.hp}",font, red, 450, (screen_height - bottom_panel + 10) + count * 30)




# fighter class
# Properties for fighters
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name

        #Stats
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength

        #Health pots
        self.start_potions = potions
        self.potions = potions

        #Spawns fighter as alive
        self.alive = True

        #Empty animation_list // what frame of anim
        self.animation_list = []
        self.frame_index = 0

        # What animation set to use
        # 0:idle 1:attack 2:dead
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
            self.idle()


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
        #check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        #set variable to attack anim
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()




    def draw(self):
        screen.blit(self.image, self.rect)


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


# INSTANCES
#Making the fighter instances
#POS/IMG/HP/STRENGTH/HPPOTS
hero = Fighter(150, 240, "Hero", 30, 10, 3)
skeleton1 = Fighter(400, 270, "Skeleton", 20, 5, 1)
skeleton2 = Fighter(540, 260, "Skeleton", 20, 5, 1)

# Skeleton instances
skeleton_list = []
skeleton_list.append(skeleton1)
skeleton_list.append(skeleton2)

# Hp bar instances
hero_health_bar = HealthBar(95, 150, hero.hp, hero.max_hp)
skeleton1_health_bar = HealthBar(370, 150, skeleton1.hp, skeleton1.max_hp)
skeleton2_health_bar = HealthBar(505, 140, skeleton2.hp, skeleton2.max_hp)

#button instances
potion_button = button.Button(screen, 25, 380, potion_img, 60, 60)


maingame = True
while maingame:

    #setting fps to game
    clock.tick(fps)

    #draw bg
    draw_bg()
    #draw panel
    draw_panel()
    hero_health_bar.draw(hero.hp)
    skeleton1_health_bar.draw(skeleton1.hp)
    skeleton2_health_bar.draw(skeleton2.hp)

    #draw fighters
    hero.update()
    hero.draw()
    for skeleton in skeleton_list:
        skeleton.draw()
        skeleton.update()



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
    draw_text(str(hero.potions), font, red, 80, 425)

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
                        current_fighter += 1
                        action_cooldown = 0    



    #enemy action
    for count, skeleton in  enumerate(skeleton_list):
        if current_fighter == 2 + count:
            if skeleton.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #attak
                    skeleton.attack(hero)
                    current_fighter += 1
                    action_cooldown = 0

            else:
                current_fighter += 1

    #if all fighters done their turn then reset
    if current_fighter > total_fighters:
        current_fighter = 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            maingame = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
