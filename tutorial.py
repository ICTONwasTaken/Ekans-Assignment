import pygame
from sys import exit #gets exit method from sys module
from random import randint

def obstacle_movement(obstacle_list):
    if obstacle_list:
        new_list = []

        for obstacle_type, obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_type == "rock":
                screen.blit(rock_surface, obstacle_rect)
            else:
                screen.blit(drill_surface, obstacle_rect)
            
            print(obstacle_list)

            if obstacle_rect.x > -100:
                new_list.append((obstacle_type, obstacle_rect))

        return new_list
    else: 
        return [] #returns an empty list so everything works

def collisions(player, obstacles):
    if obstacles:
        for obstacly_type, obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def animations():
    global guy_surface, player_index
    if guy_rect.bottom < 300:
        guy_surface = guy_jump
    else:
        player_index += 0.1
        if player_index >= len(guy_walk):
            player_index = 0
        guy_surface = guy_walk[int(player_index)]
    #walking animation

    #jump

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

drill_surface = pygame.image.load('graphics/drill.png')


obstacle_rect_list = []

guy_surface = pygame.image.load('graphics/man1.png') #uses an image

guy_walk_1 = pygame.image.load('graphics/man1-1.png')
guy_walk_2 = pygame.image.load('graphics/man1-2.png')
guy_walk = [guy_walk_1, guy_walk_2]
player_index = 0
guy_jump = pygame.image.load('graphics/manjump.png')

guy_surface = guy_walk[player_index]
guy_rect = guy_surface.get_rect(topleft = ((0, 100))) #creates a rectangle, that you can use for a bunch of stuff
    #gets guy  makes rectangle    where do you want it? (topleft is a positional variable. Can also use midleft, midbottom. The parenthesis establishes where it is).

text_surface = test_font.render('thingy', False, 'Green') #('text you wanna display', anti-aliasing [smooths edges in text], color)

score_surface = test_font.render('Score', False, (64,64,64)) #uses rgb colors
score_rect = score_surface.get_rect (center = (400, 50))

player_gravity = 0
guy_stand = pygame.image.load('graphics/man2.png')
guy_stand = pygame.transform.rotozoom(guy_stand, 400, 2)
guy_stand_rect = guy_stand.get_rect(center = (400, 200))

game_active = False

#timer
obstacle_timer = pygame.USEREVENT + 1 #+1 because some events are already reserved for pygame itself, the +1 resolves it
pygame.time.set_timer(obstacle_timer, 1300) #this triggers the event. Sets the event to be triggered, and how often it is to be triggered in milliseconds

while True: #keeps the window open while true, otherwise it immediately closes
    for event in pygame.event.get(): #loops through all possible events in the pygame
        if event.type == pygame.QUIT: #checks if the close button was clicked
            pygame.quit()              #if so, then close. This method is essentially opposite of pygame.init
            exit()   #could use break to stop the loop, but this is more secure. This closes any kind of code open entirely. Thus closing the while True loop
        #if event.type == pygame.MOUSEBUTTONUP: #checks if mouse button released
            #print('mouse up')
        #if event.type == pygame.MOUSEMOTION: #gets the position of the mouse, and prints out when the mouse moves. But NOT while it simply hovers
            #print(event.pos)
            #if guy_rect.collidepoint(event.pos):
                #print(f'collision')

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: #checks if mouse button clicked
                if guy_rect.collidepoint(event.pos):
                    print(f'Ya jumped boii')
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and guy_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(("rock", rock_surface.get_rect(bottomright = (randint(900,950), 300))))
            else:
                obstacle_rect_list.append(("drill",drill_surface.get_rect(bottomright = (randint(900,950), 200))))

    if game_active:
        screen.fill("black")   #makes the entire screen black, to clear the screen
        screen.blit(test_surface, (0,300)) #blit = block image transfer, fancy way of saying put a surface on another surface. The parenthesis establishes where it is located like a coordinate system
                                    #^Increase 1st to go right, increase the 2nd to go down

        #rock_rect.x -= 15 #moves the rock by the x axis
        #if rock_rect.right <= 0: #checks where it is on the right
            #rock_rect.left = 800 #sets it back to the left

        #screen.blit(rock_surface, rock_rect)



        player_gravity += 1
        guy_rect.y += player_gravity
        if guy_rect.bottom >= 300:
            guy_rect.bottom = 300
        animations()
        screen.blit(guy_surface, guy_rect) #uses guy_rect as a position
        #remember that pygame draws everything in the order of code, top to bottom

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(guy_rect, obstacle_rect_list)
        #draws a shape, for now a rectangle. And you need to add (the display, color, where it will be, outerwidth)
        
        pygame.draw.rect(screen,'#c0e8ec',score_rect) #so that the inside will be filled
        pygame.draw.rect(screen,'#c0e8ec',score_rect,10)

        #pygame.draw.ellipse(screen,'Brown',pygame.Rect(500, 200, 100, 100)) #makes a circle
        #pygame.draw.line(screen,'Gold',(0,0),(800,400),10) #makes a line going from the bottom left to the bottom right
        
        screen.blit(score_surface, score_rect)
        screen.blit(text_surface,(0,0))
    else:
        screen.fill('Yellow')
        screen.blit(guy_stand, guy_stand_rect)
        obstacle_rect_list.clear()
        guy_rect.midbottom = (80,300)
        player_gravity = 0

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
