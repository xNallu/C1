import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

#setting up pygame / making window size
pygame.init()
pygame.display.set_caption("Test Game")
WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

#Game fps (game speed)
FPS = 60
#Player char. speed
PLAYER_SPEED = 5

#Making image/images cover whole screen
#Gets image dimensions and then multiplies it to cover whole screen
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height, = image.get_rect()
    blocks = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            blocks.append(pos)
    return blocks, image

#Function for drawing all the things to the game
def draw(window, background, bg_image, player, objects, offset_x):

    for block in background:
        window.blit(bg_image, block)

    for obj in objects:
        obj.draw(window, offset_x)
    
    player.draw(window, offset_x)                   
    pygame.display.flip()

#Flips the sprite so it faces to the side it should face
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

#Loading each sprite individually in a sheet, and "alpha" for being able to load transparent
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [x for x in listdir(path) if isfile(join(path, x))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)

        else:
            all_sprites[image.replace(".png" "")] = sprites

    return all_sprites


# Gets the "block" image from the image file (ex this grass block starts at topleft = 96)
def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

    #Player character 
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    # Higher = stronger
    Gravity = 1
    
    #Loading sprite from the 2 dirs/ making them 32x32 pixels, true for left and right
    SPRITES = load_sprite_sheets("Character", "Testchar", 32, 32, True)

    #animation delay for new sprite (ex 5 frame 1 sprite)
    ANIMATION_DELAY = 3

    # Size / boundary boxes for interactions
    def __init__(self, x, y, width, height):

        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)

        #How fast player moves each frame / direction player is facing / animation frame / time fallling / jumps
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.timefalling = 0
        self.jump_count = 0

        #jump velocity upwards, x * negative grav
    def jump(self):
        self.y_vel = -self.Gravity * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


        #move functions base
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    #loop of velocity (making char move) / and also jumping/gravity
    def loop(self, fps):
        self.y_vel += min(1, (self.timefalling / fps) * self.Gravity)
        self.move(self.x_vel, self.y_vel)

        self.timefalling += 1
        self.update_sprite()

    # When the player lands stop y velocity and reset gravity timer
    def landed(self):
        self.timefalling = 0
        self.y_vel = 0
        self.jump_count = 0

    # Throws the player downwards if you hit a block
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    #Updating sprite facing direction
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"

        elif self.y_vel > self.Gravity * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    #Updating hitbox to match with sprite
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
        
    #Drawing character
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    #Base class for all object so collisions are the same
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    #Class for the blocks
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
    

    #Vertical collisions
def handle_vertical_collisions(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()

            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)
    return collided_objects


# checks if the player would collided with something in the moving direction
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    
    player.move(-dx, 0)
    player.update()
    return collided_object


    #Buttons for movement / and preventing move if collide with objects
def moves(player, objects):
    keys = pygame.key.get_pressed()

    #only move while holding key
    player.x_vel = 0

    collide_left = collide(player,objects, -PLAYER_SPEED * 2)
    collide_right = collide(player,objects, PLAYER_SPEED * 2)

    if keys [pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_SPEED)
    if keys [pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_SPEED)

        

    handle_vertical_collisions(player, objects, player.y_vel)

    #Main game
def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("gamebg.png")

    block_size = 96

    player = Player(100,100, 50, 50)

    #Floor
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]

    #Left Wall
    block = [*floor, Block(0, HEIGHT - block_size * 2, block_size)]
    block = block+[Block(0, HEIGHT - block_size * 3, block_size)]
    block = block+[Block(0, HEIGHT - block_size * 4, block_size)]


    #right wall
    block = block+[Block(block_size * 9.5, HEIGHT - block_size * 2, block_size)]

    #Scroll area variable //how much based on speed
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            
            # Jump in main loop so we cant hold the jump button and fly // able to add more jumps
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                   player.jump()

        player.loop(FPS)
        moves(player, block)
        #Drawing everything to the game
        draw(window, background, bg_image, player, block, offset_x)

        # Scrolling of the screen
        if ((player.rect.right - offset_x >+ WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel




    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

