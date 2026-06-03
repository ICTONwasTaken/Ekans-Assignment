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
    snake = [(200, 200)] * 5
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
head_surf.fill("Blue")

text_font = pygame.font.Font(None, 50)
sub_font = pygame.font.Font(None, 20)

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

# States: "menu", "playing", "gameover"
state = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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

        # Self collision
        elif (head_x, head_y) in snake[1:]:
            state = "gameover"

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

            screen.fill("black")
            for x, y in snake:
                pygame.draw.rect(screen, "White", (x, y, 20, 20))
            screen.blit(head_surf, head_rect)
            screen.blit(fruit_surf, fruit_rect)

    elif state == "menu":
        screen.fill("black")
        screen.blit(menu_surface, menu_rect)
        screen.blit(start_surface, start_rect)
        pygame.mouse.set_visible(True)

    elif state == "gameover":
        screen.fill("black")
        screen.blit(over_surface, over_rect)
        screen.blit(retry_surface, retry_rect)
        pygame.mouse.set_visible(True)

    pygame.display.update()
    clock.tick(10)