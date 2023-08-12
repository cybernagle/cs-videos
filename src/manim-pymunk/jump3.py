import pygame
import pymunk

# Pygame initialisation
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Pymunk initialisation
space = pymunk.Space()
space.gravity = (0.0, -900.0)

def create_ball(space):
    mass = 1
    radius = 14
    moment = pymunk.moment_for_circle(mass, 0, radius)  
    body = pymunk.Body(mass, moment)
    body.position = 50, 300  # start position for the ball
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape

def draw_ball(ball):
    pos_x = int(ball.body.position.x)
    pos_y = int(ball.body.position.y)
    pygame.draw.circle(screen, (255, 0, 0), (pos_x, pos_y), int(ball.radius), 2)

balls = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            balls.append(create_ball(space))

    screen.fill((255, 255, 255))

    for ball in balls:
        draw_ball(ball)

    space.step(1/60.0)  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
