import pygame
from sys import exit
from random import randrange

#initializes game
pygame.init()

#display thigns
axis_y = 400
axis_x = 400
screen = pygame.display.set_mode((axis_x, axis_y))
pygame.display.set_caption('Snake Game')

#fps limiter
clock = pygame.time.Clock()


def die():
    global highscore, state, fruit_growing
    state = "gameover"
    fruit_growing = False
    if score > highscore:
        highscore = score

def spawn_fruit():
    global fruit_rect
    fruit_rect = pygame.Rect(
        randrange(0, axis_x // 20) * 20,
        randrange(0, axis_y // 20) * 20,
        20, 20
        )

#resets the game
def reset_game():
    global snake, direction, fruit_rect
    #starting snake
    snake = [(200, 200), (180, 200), (160, 200), (140, 200), (120, 200)]
    direction = "right"
    #where fruit will spawn
    spawn_fruit()

    return snake, direction, fruit_rect

def start_game():
    global fruit_scale, score, state, timer
    score = 0
    state = "playing"
    pygame.mouse.set_visible(False)
    timer = 10
    
def fruit_animate():
    global fruit_growing, fruit_scale
    if fruit_growing:
        if fruit_scale < 1.1:
            fruit_scale += 0.5
        else:
            fruit_scale -= 0.1
            if fruit_scale <= 1.0:
                fruit_scale = 1.0
                fruit_growing = False

def controls():
    global direction, direction_changed
    match event.key:
        case pygame.K_RETURN:
            pygame.quit()
            exit()
        case pygame.K_UP:
            if direction != "down" and direction_changed == False: #!= ensures the snake doesn't go towards itself
                direction = "up"
                direction_changed = True
                boop_sound.play()
        case pygame.K_DOWN:
            if direction != "up" and direction_changed == False:
                direction = "down"
                direction_changed = True
                boop_sound.play()
        case pygame.K_RIGHT:
            if direction != "left" and direction_changed == False:
                direction = "right"
                direction_changed = True
                boop_sound.play()
        case pygame.K_LEFT:
            if direction != "right" and direction_changed == False:
                direction = "left"
                direction_changed = True
                boop_sound.play()

def intro():
    screen.fill("black")

    intro_surface = sub_font.render('There once was a snake... he had a dream of becoming large!', False, 'White')
    intro_rect = intro_surface.get_rect(center=(200, 200))
    
    screen.blit(intro_surface, intro_rect)

def menu():
    screen.fill("black")

    menu_surface = text_font.render('EKANS!', False, 'White')
    menu_rect = menu_surface.get_rect(center=(200, 190))
    start_surface = sub_font.render('Press Anything to Begin', False, 'White')
    start_rect = start_surface.get_rect(center=(200, 225))

    screen.blit(menu_surface, menu_rect)
    screen.blit(start_surface, start_rect)

def gameover():
    screen.fill("black")
    over_surface = text_font.render('Game Over', False, 'White')
    over_rect = over_surface.get_rect(center=(200, 190))
    retry_surface = sub_font.render('Press Anything to Retry', False, 'White')
    retry_rect = retry_surface.get_rect(center=(200, 225))

    screen.blit(over_surface, over_rect)
    screen.blit(retry_surface, retry_rect)

    score_final_surface = score_font.render(f'You grew to {score}cm!', False, 'White')
    score_final_rect = score_final_surface.get_rect(center=(200, 150))

    score_high_surface = score_font.render(f'Highscore: {highscore}cm', False, 'White')
    score_high_rect = score_final_surface.get_rect(center=(210, 100))

    screen.blit(score_final_surface, score_final_rect)
    screen.blit(score_high_surface, score_high_rect)


def movement():
    global head_x, head_y
    if direction == "right":
        head_x += 20
    elif direction == "left":
        head_x -= 20
    elif direction == "up":
        head_y -= 20
    elif direction == "down":
        head_y += 20


#initialize variables here before the game starts so that nothing breaks
snake, direction, fruit_rect = reset_game()

#the fruit
fruit_surf = pygame.Surface((20, 20))
fruit_surf.fill('Pink')

head_surf = pygame.Surface((20, 20))
head_surf.fill("White")

#buncha fonts
text_font = pygame.font.Font(None, 50)
sub_font = pygame.font.Font(None, 20)
score_font = pygame.font.Font(None, 30)

#scoring
score = 0
highscore = 0

default_timer = 10
timer = default_timer

#sound
gameover_sound = pygame.mixer.Sound('graphics/gameover.mp3')
boop_sound = pygame.mixer.Sound('graphics/boop.mp3')
beep_sound = pygame.mixer.Sound('graphics/beepbeep.mp3')
good_sound = pygame.mixer.Sound('graphics/good.mp3')


#states = "menu", "playing", "gameover", "intro"
state = "intro"

#animation things
fruit_scale = 0.1
fruit_growing = True
flash_timer = 0

direction_changed = False

while True:
    for event in pygame.event.get():
        print(fruit_growing)
        print(fruit_scale)
        #if player touches x, close games
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and state == "intro":
            state = "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and state == "menu":
                pygame.quit()
                exit()
            elif event.key == pygame.K_ESCAPE and state == "gameover":
                state = "menu"
                beep_sound.play()
            elif event.key == pygame.K_ESCAPE and state == "playing":
                state = "menu"
                beep_sound.play()


        #basic controls
        if event.type == pygame.KEYDOWN:
            if state == "playing":
                controls()

            #play the game
            else:
                if state == "intro":
                    state = "menu"
                    beep_sound.play()
                elif state == "menu" or state == "gameover":
                    start_game()
                    reset_game()
                    beep_sound.play()


    if state == "playing":
        direction_changed = False
        #sets these two to what's inside index 0 of snake
        head_x, head_y = snake[0]

        #if direction state is something, move it along the specific axis
        movement()

        #Wall collision
        if head_x < 0 or head_x >= axis_x or head_y < 0 or head_y >= axis_y:
            die()
            gameover_sound.play()
            print("You hit a wall!")
            

        #Self collision - checks if head x and y is the same as a part of the snake. If so, they are colliding. snake[1:] is a slice, takes everything from index 1 to the length
        elif (head_x, head_y) in snake[1:]:
            die()
            gameover_sound.play()
            print("You hit yourself!")
    

        else: #if none of the above is happening, insert a snake box at the start of the list, and remove the last
            snake.insert(0, (head_x, head_y))
            snake.pop()
            head_rect = pygame.Rect(head_x, head_y, 20, 20)

            if fruit_rect.colliderect(head_rect): #if the fruit collides with the rectangle of the head, append from the bottom
                snake.append(snake[-1])
                spawn_fruit()
                
                good_sound.play()
                score += 10
                fruit_scale = 0.1
                fruit_growing = True
                flash_timer = 3
                timer = default_timer

            #Grow fruit scale each frame until full size
            fruit_animate()
                        
            #change fruit rectangle and store it in scaled fruit
            scaled_fruit = pygame.transform.rotozoom(fruit_surf, 0, fruit_scale) #surface, rotation, scale
            scaled_rect = scaled_fruit.get_rect(center=fruit_rect.center)
        

            screen.fill("black") #reset screen

            if score >= 5000:
                timer -= 0.2
                timer_surface = sub_font.render(f'Time: {timer:.1f}', False, 'White')
                timer_rect = timer_surface.get_rect(topleft=(200, 10))
                screen.blit(timer_surface, timer_rect)
                if timer <= 0:
                    state = "gameover"
                    if score > highscore:
                        highscore = score

            #create snake
            screen.blit(head_surf, head_rect)
            if flash_timer > 0:
                flash_timer -= 1
                for x, y in snake:
                    pygame.draw.rect(screen, "#3cff00", (x, y, 20, 20))
            else:
                for x, y in snake:
                    pygame.draw.rect(screen, 'White', (x, y, 20, 20))
            screen.blit(scaled_fruit, scaled_rect)
            
            score_game_surface = sub_font.render(f'Length: {score}cm', False, 'White')
            score_game_rect = score_game_surface.get_rect(topleft=(10, 10))
            screen.blit(score_game_surface, score_game_rect)

    elif state == "menu":
        menu()
        pygame.mouse.set_visible(True)

    elif state == "gameover":
        gameover()
        pygame.mouse.set_visible(True)
    
    elif state == "intro":
        intro()

    pygame.display.update()
    clock.tick(10)