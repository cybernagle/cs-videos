import pygame
import pymunk

# 初始化pygame和pymunk
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0.0, -900.0)

# 创建圆形刚体
radius = 30
mass = 1
moment = pymunk.moment_for_circle(mass, 0, radius)
body = pymunk.Body(mass, moment)
body.position = (100, 300)
shape = pymunk.Circle(body, radius)
space.add(body, shape)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 更新物理世界
    dt = 1.0 / 60.0
    for _ in range(10):
        space.step(dt / 10.0)

    # 清屏
    screen.fill((255, 255, 255))

    # 绘制圆形
    pos = int(body.position.x), 400 - int(body.position.y)
    pygame.draw.circle(screen, (0, 0, 255), pos, radius)

    # 刷新屏幕
    pygame.display.flip()
    clock.tick(60)
