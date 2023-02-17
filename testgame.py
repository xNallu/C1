import pygame
import sys
from pygame.locals import *


#Setting up screen size
pygame.init()
pygame.display.set_caption("Setting up game")
screen = pygame.display.set_mode((1000, 700))
 
#Font
font = pygame.font.SysFont("cambria", 50)

#Function that can get called to add text to an object 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Variable that stores the click check
click = False
 
# Main container function that holds the buttons and game functions
def main_menu():
    while True:


        # Background / main menu text
        background = pygame.image.load("background.png").convert()
        background = pygame.transform.scale(background, (1000, 700))
        screen.blit(background, (0, 0))

        #Get mouse position
        mx, my = pygame.mouse.get_pos()
        
        #Drawing the main menu text
        draw_text("MAIN MENU", font, (116,113,113), screen, 370, 40)

        #creating buttons x,y w,h
        button_1 = pygame.Rect(405, 200, 200, 50)
        button_2 = pygame.Rect(405, 300, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                quit_game()


        #Drawing rectangles for the buttons
        pygame.draw.rect(screen, (232, 232, 232), button_1)
        pygame.draw.rect(screen, (232, 232, 232), button_2)
 
        #writing text on top of buttons
        draw_text('Start', font, (116,113,113), screen, 455, 193)
        draw_text('Quit', font, (116,113,113), screen, 455, 292)




        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.flip()
 
#Function that gets called when you click "start" button
def game():
    
    running = True
    while running:
        screen.fill((0,0,0))
       
        import game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

#function that gets called when you click "quit" button
def quit_game():
    pygame.quit()
    sys.exit()

 
main_menu()
