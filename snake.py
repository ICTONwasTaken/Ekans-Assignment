import pygame
from sys import exit
import random

pygame.init()
axis_y = 400
axis_x = 400

screen = pygame.display.set_mode((axis_x, axis_y))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def reset_game():
    snake = [(200, 200), (180, 200), (160, 200), (140, 200), (120, 200)]
    direction = "right"
    fruit_rect = pygame.Rect(
        random.randrange(0, axis_x // 20) * 20,
        random.randrange(0, axis_y // 20) * 20,
        20, 20
    )
    return snake, direction, fruit_rect

snake, direction, fruit_rect = reset_game()

fruit_surf = pygame.Surface((20, 20))
fruit_surf.fill('Pink')

head_surf = pygame.Surface((20, 20))
head_surf.fill("White")

text_font = pygame.font.Font(None, 50)
sub_font = pygame.font.Font(None, 20)
score_font = pygame.font.Font(None, 30)

# Menu screen
menu_surface = text_font.render('EKANS!', False, 'White')
menu_rect = menu_surface.get_rect(center=(200, 190))
start_surface = sub_font.render('Press Space to Begin', False, 'White')
start_rect = start_surface.get_rect(center=(200, 225))

# Game over screen
over_surface = text_font.render('Game Over', False, 'White')
over_rect = over_surface.get_rect(center=(200, 190))
retry_surface = sub_font.render('Press Space to Retry', False, 'White')
retry_rect = retry_surface.get_rect(center=(200, 225))

#scoring
score = 0
highscore = 0

score_game_surface = sub_font.render(f'Length: {score}cm', False, 'White')
score_game_rect = score_game_surface.get_rect(topleft=(10, 10))

score_final_surface = score_font.render(f'You grew to {score}cm!', False, 'White')
score_final_rect = score_final_surface.get_rect(center=(200, 150))


# States: "menu", "playing", "gameover"
state = "menu"
fruit_scale = 0.1
fruit_growing = True
flash_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and state == "menu":
                pygame.quit()
                exit()
            elif event.key == pygame.K_ESCAPE and state == "gameover":
                state = "menu"
            elif event.key == pygame.K_ESCAPE and state == "playing":
                state = "menu"

        if event.type == pygame.KEYDOWN:
            if state == "playing":
                match event.key:
                    case pygame.K_RETURN:
                        pygame.quit()
                        exit()
                    case pygame.K_UP:
                        if direction != "down":
                            direction = "up"
                    case pygame.K_DOWN:
                        if direction != "up":
                            direction = "down"
                    case pygame.K_RIGHT:
                        if direction != "left":
                            direction = "right"
                    case pygame.K_LEFT:
                        if direction != "right":
                            direction = "left"
            elif state == "menu" or state == "gameover":
                if event.key == pygame.K_SPACE:
                    snake, direction, fruit_rect = reset_game()
                    fruit_scale = 0.1
                    score = 0
                    state = "playing"
                    pygame.mouse.set_visible(False)

    if state == "playing":
        head_x, head_y = snake[0]


        if direction == "right":
            head_x += 20
        elif direction == "left":
            head_x -= 20
        elif direction == "up":
            head_y -= 20
        elif direction == "down":
            head_y += 20

        # Wall collision
        if head_x < 0 or head_x >= axis_x or head_y < 0 or head_y >= axis_y:
            state = "gameover"
            if score > highscore:
                highscore = score
            collided = True

        # Self collision
        elif (head_x, head_y) in snake[1:]:
            state = "gameover"
            if score > highscore:
                highscore = score
            collided = True

        else:
            snake.insert(0, (head_x, head_y))
            snake.pop()
            head_rect = pygame.Rect(head_x, head_y, 20, 20)

            if fruit_rect.colliderect(head_rect):
                snake.append(snake[-1])
                fruit_rect = pygame.Rect(
                    random.randrange(0, axis_x // 20) * 20,
                    random.randrange(0, axis_y // 20) * 20,
                    20, 20
                )
                score += 10
                fruit_scale = 0.1
                fruit_growing = True
                flash_timer = 3

            # Grow fruit scale each frame until full size
            if fruit_growing:
                if fruit_scale < 1.1:
                    fruit_scale += 0.5
                else:
                    fruit_scale -= 0.1
                    if fruit_scale <= 1.0:
                        fruit_scale = 1.0
                        fruit_growing = False
                        

            scaled_fruit = pygame.transform.rotozoom(fruit_surf, 0, fruit_scale)
            scaled_rect = scaled_fruit.get_rect(center=fruit_rect.center)

            screen.fill("black")

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
        screen.fill("black")
        screen.blit(menu_surface, menu_rect)
        screen.blit(start_surface, start_rect)
        pygame.mouse.set_visible(True)
        fruit_growing = True

    elif state == "gameover":
        screen.fill("black")
        screen.blit(over_surface, over_rect)
        screen.blit(retry_surface, retry_rect)
        pygame.mouse.set_visible(True)
        fruit_growing = True

        score_final_surface = score_font.render(f'You grew to {score}cm!', False, 'White')
        score_final_rect = score_final_surface.get_rect(center=(200, 150))

        score_high_surface = score_font.render(f'Highscore: {highscore}cm', False, 'White')
        score_high_rect = score_final_surface.get_rect(center=(210, 100))

        screen.blit(score_final_surface, score_final_rect)
        screen.blit(score_high_surface, score_high_rect)

    pygame.display.update()
    clock.tick(10)