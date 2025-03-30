# Импорт библиотек
import pygame
import sys
from pygame.locals import *
import random
import time

# Инициализация Pygame
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Создание цветов
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Переменные для использования в программе
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Скорость движения врагов
SCORE = 0  # Очки

# Загрузка и воспроизведение фоновой музыки
pygame.mixer.music.load('./Lab_9/racer/Ace of Base - Happy Nation.mp3')
pygame.mixer.music.play(-1)

# Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("./Lab_9/racer/AnimatedStreet.png")

# Создание белого экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("RACER")


# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./Lab_9/racer/Enemy.png")  # Загрузка изображения врага
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Перемещение врага обратно вверх, если он выходит за пределы экрана
        if (self.rect.bottom > 600):
            SCORE += 1  # Увеличение очков
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            "./Lab_9/racer/Player1.png"), (100, 110))  # Загрузка изображения игрока
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)

    def move(self):
        klav = pygame.key.get_pressed()
        # Движение вверх, вниз, влево и вправо
        if klav[K_UP]:
            self.rect.move_ip(0, -9)
        if klav[K_DOWN]:
            self.rect.move_ip(0, 9)
        if klav[K_LEFT]:
            self.rect.move_ip(-9, 0)
        if klav[K_RIGHT]:
            self.rect.move_ip(9, 0)


# Класс для монет
class Coins (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./Lab_9/racer/coins.png")  # Загрузка изображения монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20),
                            random.randint(20, SCREEN_HEIGHT-20))

    def move(self):
        # Случайное перемещение монеты
        x = random.randint(20, SCREEN_WIDTH-20)
        y = random.randint(20, SCREEN_HEIGHT-20)
        self.rect.center = (x, y)


# Настройка спрайтов
P1 = Player()
E1 = Enemy()
C = Coins()

# Создание групп спрайтов
coins = pygame.sprite.Group()
coins.add(C)
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Добавление нового пользовательского события
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

# Игровой цикл
while True:

    # Обработка всех событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Увеличение скорости врагов
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отображение фона
    screen.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (10, 10))

    # Перемещение и перерисовка всех спрайтов
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)
    for entity in coins:
        screen.blit(entity.image, entity.rect)

    # Проверка столкновения игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./Lab_9/racer/crash.wav')  # Загрузка звука аварии
        pygame.mixer.music.play()
        time.sleep(1.5)
        screen.fill(WHITE)
        screen.blit(game_over, (30, 250))
        res_scores = font.render("Score: "+str(SCORE), True, BLACK)  # Показ финального счета
        screen.blit(res_scores, (20, 200))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(3)

        pygame.quit()
        sys.exit()

    # Проверка столкновения игрока с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        pygame.mixer.Sound('./Lab_9/racer/coinss.mp3').play()  # Воспроизведение звука монеты
        SCORE += 1  # Увеличение очков
        C.move()  # Перемещение монеты

    pygame.display.update()
    FramePerSec.tick(FPS)  # Задержка для поддержания FPS
