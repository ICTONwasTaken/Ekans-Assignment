import pygame
from sys import exit
import random

pygame.init()
axis_y = 400
axis_x = 400

#Preliminary
screen = pygame.display.set_mode((axis_x,axis_y))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

snake = [
    (200, 200),  # head
    (200, 200),
    (200, 200),
    (200, 200),
    (200, 200)
]
fruit_position = [random.randrange(1, (axis_x//10)) * 10, 
                  random.randrange(1, (axis_y//10)) * 10]

fruit_surf = pygame.Surface((20, 20))
fruit_surf.fill('Pink')
fruit_rect = fruit_surf.get_rect(center = ((fruit_position)))

text_font = pygame.font.Font(None, 50)
sub_font = pygame.font.Font(None, 20)

text_surface = text_font.render('EKANS!', False, 'White')
text_rect = text_surface.get_rect(center = ((200, 200)))

sub_surface = sub_font.render('Press Space to Begin', False, 'White')
sub_rect = sub_surface.get_rect(center = ((200, 230)))

fruit_spawn = True

movement = "right"
direction = "right"

speed = 20
head_x = 0
head_y = 0

head_surf = pygame.Surface((20, 20))
head_surf.fill("Blue")
head_rect = head_surf.get_rect(center = ((head_x, head_y)))

game_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN:
                        pygame.quit()  
                        exit()
                    case pygame.K_UP:
                        direction = "up"
                    case pygame.K_DOWN:
                        direction = "down"
                    case pygame.K_RIGHT:
                        direction = "right"
                    case pygame.K_LEFT:
                        direction = "left"
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

    if game_active:
        head_x, head_y = snake[0]

        if direction == "right":
            head_x += 20
        elif direction == "left":
            head_x -= 20
        elif direction == "up":
            head_y -= 20
        elif direction == "down":
            head_y += 20

        if head_rect.y < 0:
            game_active = False

        
        snake.insert(0, (head_x, head_y))
        snake.pop()
        head_rect = pygame.Rect(head_x, head_y, 20, 20)

        screen.fill("black")
        for x, y in snake:
            pygame.draw.rect(screen, "White", (x, y, 20, 20))

        if fruit_rect.colliderect(head_rect):
            snake.append(snake[-1])  # grow snake (not fruit_rect)
            fruit_rect = pygame.Rect(
                random.randrange(0, axis_x // 20) * 20,
                random.randrange(0, axis_y // 20) * 20,
                20, 20
            )
        screen.blit(head_surf, head_rect)
        screen.blit(fruit_surf, fruit_rect)
    else:
        screen.fill("black")
        screen.blit(text_surface, text_rect)
        screen.blit(sub_surface, sub_rect)
        snake = [(200, 200)] * 5
        direction = "right"

    pygame.display.update()
    clock.tick(10)