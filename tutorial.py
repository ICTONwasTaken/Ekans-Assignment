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

test_font = pygame.font.Font(None, 50) #font type, and font size. None means default


test_surface = pygame.Surface((1000, 100)) #creates a surface in pygame. Inside needs a tuple with width and height
test_surface.fill('White') #adds color to a defined surface

rock_surface = pygame.image.load('graphics/rock.png')
rock_rect = rock_surface.get_rect(bottomright = (700, 200))

guy_surface = pygame.image.load('graphics/man1.png') #uses an image
guy_x_pos = 0 #a variable for starting position

guy_rect = guy_surface.get_rect(topleft = ((0, 100))) #creates a rectangle, that you can use for a bunch of stuff
    #gets guy  makes rectangle    where do you want it? (topleft is a positional variable. Can also use midleft, midbottom. The parenthesis establishes where it is).

text_surface = test_font.render('thingy', False, 'Green') #('text you wanna display', anti-aliasing [smooths edges in text], color)

while True: #keeps the window open while true, otherwise it immediately closes
    for event in pygame.event.get(): #loops through all possible events in the pygame
        if event.type == pygame.QUIT: #checks if the close button was clicked
            pygame.quit()              #if so, then close. This method is essentially opposite of pygame.init
            exit()   #could use break to stop the loop, but this is more secure. This closes any kind of code open entirely. Thus closing the while True loop
    
    screen.fill("black")   #makes the entire screen black, to clear the screen

    screen.blit(test_surface, (0,300)) #blit = block image transfer, fancy way of saying put a surface on another surface. The parenthesis establishes where it is located like a coordinate system
                                #^Increase 1st to go right, increase the 2nd to go down
    
    
    rock_rect.left -= 4 #every frame update, moves rock to the left
    guy_rect.left += 1
    if rock_rect.right < -90: #if rpck's position is greater than 800, set back to 0
        rock_rect = 700

    screen.blit(rock_surface, rock_rect)
    screen.blit(guy_surface, guy_rect) #uses guy_rect as a position
    #remember that pygame draws everything in the order of code, top to bottom

    screen.blit(text_surface,(0,0))

    pygame.display.update() #updates display surface
    clock.tick(60) #tells pygame that this while loop should NOT run faster than 60x per second. Ensures that faster computers don't have quicker gameplay, so they have maximum frame rate.
