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
rock_rect = rock_surface.get_rect(bottomright = (700, 300))

guy_surface = pygame.image.load('graphics/man1.png') #uses an image
guy_x_pos = 0 #a variable for starting position

guy_rect = guy_surface.get_rect(topleft = ((0, 100))) #creates a rectangle, that you can use for a bunch of stuff
    #gets guy  makes rectangle    where do you want it? (topleft is a positional variable. Can also use midleft, midbottom. The parenthesis establishes where it is).

text_surface = test_font.render('thingy', False, 'Green') #('text you wanna display', anti-aliasing [smooths edges in text], color)

score_surface = test_font.render('Score', False, (64,64,64)) #uses rgb colors
score_rect = score_surface.get_rect (center = (400, 50))

player_gravity = 0

while True: #keeps the window open while true, otherwise it immediately closes
    for event in pygame.event.get(): #loops through all possible events in the pygame
        if event.type == pygame.QUIT: #checks if the close button was clicked
            pygame.quit()              #if so, then close. This method is essentially opposite of pygame.init
            exit()   #could use break to stop the loop, but this is more secure. This closes any kind of code open entirely. Thus closing the while True loop
        if event.type == pygame.MOUSEBUTTONDOWN: #checks if mouse button clicked
            if guy_rect.collidepoint(event.pos):
                print(f'Ya jumped boii')

                player_gravity = -20
        #if event.type == pygame.MOUSEBUTTONUP: #checks if mouse button released
            #print('mouse up')
        #if event.type == pygame.MOUSEMOTION: #gets the position of the mouse, and prints out when the mouse moves. But NOT while it simply hovers
            #print(event.pos)
            #if guy_rect.collidepoint(event.pos):
                #print(f'collision')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and guy_rect.bottom >= 300:
                player_gravity = -20
        

    screen.fill("black")   #makes the entire screen black, to clear the screen

    screen.blit(test_surface, (0,300)) #blit = block image transfer, fancy way of saying put a surface on another surface. The parenthesis establishes where it is located like a coordinate system
                                #^Increase 1st to go right, increase the 2nd to go down

    rock_rect.x -= 4 #moves the rock by the x axis
    if rock_rect.right <= 0: #checks where it is on the right
        rock_rect.left = 800 #sets it back to the left

    screen.blit(rock_surface, rock_rect)

    player_gravity += 1
    guy_rect.y += player_gravity
    if guy_rect.bottom >= 300:
        guy_rect.bottom = 300
    screen.blit(guy_surface, guy_rect) #uses guy_rect as a position
    #remember that pygame draws everything in the order of code, top to bottom

    if rock_rect.colliderect(guy_rect):
        pygame.quit()
        exit()
    #draws a shape, for now a rectangle. And you need to add (the display, color, where it will be, outerwidth)
    
    pygame.draw.rect(screen,'#c0e8ec',score_rect) #so that the inside will be filled
    pygame.draw.rect(screen,'#c0e8ec',score_rect,10)

    #pygame.draw.ellipse(screen,'Brown',pygame.Rect(500, 200, 100, 100)) #makes a circle
    #pygame.draw.line(screen,'Gold',(0,0),(800,400),10) #makes a line going from the bottom left to the bottom right
    
    screen.blit(score_surface, score_rect)
    screen.blit(text_surface,(0,0))

    #if guy_rect.colliderect(rock_rect): #checks when the guy's rectangle collids with the rock's. If so, it will output a 1
        #print('collision')

    #mouse_pos = pygame.mouse.get_pos() #gets mouse position
    #if guy_rect.collidepoint((mouse_pos)): #hovering over the guy rectangle does the if statement
        #print('THIS!')

    #keyboard input
    #keys is a dictionary now
    #keys = pygame.key.get_pressed() #records ALL buttons and see what is pressed. If so, it will output a 1
    #if keys[pygame.K_SPACE]: #if space is pressed, print jump
        #print('jump')

    #OR



    #jumping + gravity
    #create floor

    pygame.display.update() #updates display surface
    clock.tick(60) #tells pygame that this while loop should NOT run faster than 60x per second. Ensures that faster computers don't have quicker gameplay, so they have maximum frame rate.
