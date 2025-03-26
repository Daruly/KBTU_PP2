import pygame

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

RED = (125, 0, 0)
WHITE = (255, 255, 255)

x = WIDTH // 2
y = HEIGHT // 2
step = 20
radius = 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Возвращает последовательность логических значений, представляющих состояние каждой клавиши на клавиатуре.
    x = max(radius, min(WIDTH - radius, x + (keys[pygame.K_d] - keys[pygame.K_a]) * step))
    y = max(radius, min(HEIGHT - radius, y + (keys[pygame.K_s] - keys[pygame.K_w]) * step))

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)
    # заблокирует выполнение, пока не пройдет 1/60 секунды
    # с момента предыдущего вызова clock.tick.

pygame.quit()
