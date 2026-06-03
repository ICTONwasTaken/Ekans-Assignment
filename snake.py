import pygame
from sys import exit #gets exit method from sys module

pygame.init() #initializes the pygame
screen = pygame.display.set_mode((800,400))
# ^                    ^          ^   ^
#name of window                width height
#                 Make window

pygame.display.set_caption('Snake Game') #changes top right

clock = pygame.time.Clock() #creates a clock object for FPS

while True: #keeps the window open while true, otherwise it immediately closes
    for event in pygame.event.get(): #loops through all possible events in the pygame
        if event.type == pygame.QUIT: #checks if the close button was clicked
            pygame.quit()              #if so, then close. This method is essentially opposite of pygame.init
            exit()   #could use break to stop the loop, but this is more secure. This closes any kind of code open entirely. Thus closing the while True loop


    

    pygame.display.update() #updates display surface
    clock.tick(60) #tells pygame that this while loop should NOT run faster than 60x per second. Ensures that faster computers don't have quicker gameplay, so they have maximum frame rate.
