import pygame
from sys import exit #gets exit method from sys module

pygame.init() #initializes the pygame
screen = pygame.display.set_mode((800,400))
# ^                    ^          ^   ^
#name of window                width height
#                 Make window

#Display/Display Surface = the game window, can only have 1
#Surface = an image on the display, can have as many as you want

pygame.display.set_caption('Snake Game') #changes top right
clock = pygame.time.Clock() #creates a clock object for FPS

test_surface = pygame.Surface((100, 200)) #creates a surface in pygame. Inside needs a tuple with width and height
test_surface.fill('Red') #adds color to a defined surface

while True: #keeps the window open while true, otherwise it immediately closes
    for event in pygame.event.get(): #loops through all possible events in the pygame
        if event.type == pygame.QUIT: #checks if the close button was clicked
            pygame.quit()              #if so, then close. This method is essentially opposite of pygame.init
            exit()   #could use break to stop the loop, but this is more secure. This closes any kind of code open entirely. Thus closing the while True loop

    screen.blit(test_surface, (200,0)) #blit = block image transfer, fancy way of saying put a surface on another surface. The parenthesis establishes where it is located like a coordinate system
                                #^Increase 1st to go right, increase the 2nd to go down

    pygame.display.update() #updates display surface
    clock.tick(60) #tells pygame that this while loop should NOT run faster than 60x per second. Ensures that faster computers don't have quicker gameplay, so they have maximum frame rate.
