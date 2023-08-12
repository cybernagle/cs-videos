import pygame
import pymunk

# 初始化pygame和pymunk
pygame.init()
screen = pygame.display.set_mode((600, 400))
space = pymunk.Space()
space.gravity = (0, 900)  # 设置重力加速度

# 创建地面
ground = pymunk.Segment(space.static_body, (0, 380), (600, 380), 0)
ground.friction = 1.0
space.add(ground)

# 创建物体
body = pymunk.Body(1, 100)  # 质量为1，弹性为100
body.position = (100, 300)  # 初始位置
shape = pymunk.Circle(body, 20)  # 创建圆形
space.add(body, shape)

# 施加向上的力
def jump():
    body.apply_impulse_at_local_point((0, -200))

# 渲染循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 按下空格键时施加力
                jump()

    screen.fill((255, 255, 255))  # 清空屏幕
    space.step(1/50.0)  # 更新物理模拟

    # 绘制物体
    position = body.position
    pygame.draw.circle(screen, (0, 0, 255), (int(position.x), int(position.y)), 20)

    # 刷新屏幕
    pygame.display.flip()
    clock.tick(50)

pygame.quit()

