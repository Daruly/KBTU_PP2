import pygame
import random
import time
from insert_data import insert_user_data, user_exist, current_data, updating_data,show_leaders
def taking_user_name():
    return input("Введите свое имя: ")

pygame.init()
user_name = taking_user_name()

# База
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Началки по дефолту
default_level = 1
default_length = 1
default_score = 0  

# При загрузке игры, если пользователь существует, загружаем сохранённое состояние
if user_exist(user_name):
    # курент дата передает скор сохранненая длина и уровень
    score, saved_length, level_num = current_data(user_name)
    length = saved_length
    print(f"Добро пожаловать, {user_name}! Продолжаем с уровня {level_num}, длиной {length} ну и счетом {score}")
else:#а если не было в игре, то задаем базу
    level_num = default_level
    length = default_length
    score = default_score
    insert_user_data(user_name, score, length, level_num)
    print(f"Привет, {user_name}! Ты начинаешь с 1 уровня.")

# При повторном входе позиция всегда в центре
center_x = WIDTH // 2
center_y = HEIGHT // 2

font_large = pygame.font.SysFont('Arial', 66, bold=True)
font_small = pygame.font.SysFont('Arial', 26, bold=True)
food_size = 10

# Словарь для контроля допустимых направлений (запрещаем разворот в самого себя)
dirs = {'W': True, 'S': True, 'D': True, 'A': True}

# Цвета
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,255,0)

# Для возобновления игры формируем змейку как горизонтальную линию,
# где голова находится в центре. Если длина больше 1, остальные сегменты располагаются слева.
snake_size = (40, 40)
snake = [(center_x - i * snake_size[0], center_y) for i in range(length)][::-1]  
# Начальное направление – вправо (dx=1, dy=0)
dx, dy = 1, 0

# Скорость змейки (интервал между перемещениями)
move_i = 0.3
move_t = 0

# юзерное событие для таймера еды (каждые 3 сек)
FOOD_TIMEOUT = pygame.USEREVENT + 1
pygame.time.set_timer(FOOD_TIMEOUT, 5000)

# Класс уровняей (препятствиями)
class Level():
    def __init__(self, level_num):
        self.blocks = []
        self.block_img = pygame.transform.scale(pygame.image.load('tnt.png'), (60, 60))
        self.level_num = level_num
        self.locate()
        
    def locate(self):
        levels = {
            2: [(500, 240), (250, 100), (900, 200)], # 4
            3: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170)], # 7
            4: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170), (410, 520), (350, 520), (410,580), (690,390)], # 11    
            5: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170), (410, 520), (350, 520), (410,580), (690,390),(120,140),(180,140),(180,80)],
            6: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170), (410, 520), (350, 520), (410,580), (690,390),(120,140),(180,140),(180,80), (930,170),(1080,40),(1080,100)],
            7: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170), (410, 520), (350, 520), (410,580), (690,390),(120,140),(180,140),(180,80), (930,170),(1080,40),(1080,100), (600,100), (660,100), (720,100),(540,160)],
            8: [(470, 250), (410, 250), (410, 300), (690, 450), (750, 450), (810,170), (870,170), (410, 520), (350, 520), (410,580), (690,390),(120,140),(180,140),(180,80), (930,170),(1080,40),(1080,100), (600,100), (660,100), (720,100),(540,160), (90,400),(90,340), (1000,400), (1000,340)]# 14
        }
        positions = levels.get(self.level_num, [])
        for pos in positions:
            rect = self.block_img.get_rect(topleft=pos)
            self.blocks.append(rect)
    
    def inc_speed(self):
        global move_i
        move_i = max(0.08, move_i - 0.05 * int(self.level_num))
    
    def draw(self):
        for block in self.blocks:
            screen.blit(self.block_img, block.topleft)



level = Level(level_num)
level.inc_speed()

# Функция спавна еды (позиция не должна пересекаться со змейкой или блоками)
def spawn_food():
    while True:
        food = (random.randint(0, WIDTH // snake_size[0] - 1) * snake_size[0],
                random.randint(0, HEIGHT // snake_size[1] - 1) * snake_size[1])
        if food not in snake and not any(block.collidepoint(food) for block in level.blocks):
            return food

# Спавним обычную и супер-еду
food_x, food_y = spawn_food()
superfood_x, superfood_y = spawn_food()

# Функция game_over – вызывается при столкновении (проигрыш)
def game_over():
    updating_data(user_name, 0, 1, 1)
    screen.blit(font_large.render("ПОКА", True, pygame.Color('orange')), (WIDTH // 2 - 100, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()

# Функция сохранения состояния при добровольном выходе
def save_and_exit():
    updating_data(user_name, score, length, level_num)
    pygame.quit()
    exit()

# Функция проверки столкновения змейки с блоками
def colision():
    snake_head = pygame.Rect(snake[-1][0], snake[-1][1], snake_size[0], snake_size[1])
    for block in level.blocks:
        if snake_head.colliderect(block):
            explosion = pygame.mixer.Sound("tnt-explosion.mp3")
            explosion.play()
            pygame.time.wait(2000)
            game_over()
def reset_snake():
    global snake, center_x, center_y, dx, dy, length
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    dx, dy = 1, 0
    snake = [(center_x, center_y)]

    
background = pygame.image.load('flowers.png')
snake_head_img = pygame.transform.scale(pygame.image.load('snake_head.png'), (40, 40))
snake_body_img = pygame.transform.scale(pygame.image.load('snake_body.png'), (40, 40))
# Картинки для еды
food_img = pygame.transform.scale(pygame.image.load('food.png'), (40, 40))
superfood_img = pygame.transform.scale(pygame.image.load('super_food.png'), (40, 40))
paused = False
escape_pressed = False
tab = False
tab_pressed = False
time.sleep(1)#что бы дать время
while True:
    screen.blit(background, (0,0))

    dt = clock.tick(144) / 1000  # разница во времени между кадрами

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_and_exit()
        if event.type == FOOD_TIMEOUT:
            food_x, food_y = spawn_food()
            superfood_x, superfood_y = spawn_food()
            pygame.time.set_timer(FOOD_TIMEOUT, 5000)
        if event.type == pygame.KEYDOWN: #вызвали паузу
            if event.key == pygame.K_ESCAPE:
                if not escape_pressed:
                    paused = not paused
                    escape_pressed = True
        if event.type == pygame.KEYUP: #отовызвали паузу
            if event.key == pygame.K_ESCAPE:
                escape_pressed = False
        if event.type == pygame.KEYDOWN: #вызвали tab
            if event.key == pygame.K_TAB:
                if not tab_pressed:
                    tab = not tab
                    tab_pressed = True
        if event.type == pygame.KEYUP: #отовызвали tab
            if event.key == pygame.K_TAB:
                tab_pressed = False
    def show_tab():
        nicknames = show_leaders()
        top_names, top_score = zip(*nicknames)
        screen.blit(font_small.render(f"LEADERS:", True, pygame.Color('purple')), (5,30))
        y_position = 60
        for name, score in nicknames:
            line_text = f"{name} {score}"
            rendered_line = font_small.render(line_text, True, pygame.Color("purple"))
            screen.blit(rendered_line, (5, y_position))
            y_position += rendered_line.get_height() + 5
    if not paused:
        if tab:
            show_tab()
        # Рисуем змейку
        for seg in snake[:-1]:
            screen.blit(snake_body_img, (seg[0], seg[1]))
        head = snake[-1]
        screen.blit(snake_head_img, (head[0], head[1]))
        # Рисуем еду

        screen.blit(food_img, (food_x, food_y))
        screen.blit(superfood_img, (superfood_x, superfood_y))

        #рендерим счетик
        screen.blit(font_small.render(f'Score {score}', True, pygame.Color('orange')), (5, 5))
        level.draw()
        
        move_t += dt
        if move_t > move_i:
            move_t = 0
            # Перемещаем голову змейки по направлению dx, dy
            center_x += dx * snake_size[0]
            center_y += dy * snake_size[1]
            snake.append((center_x, center_y))
            snake = snake[-length:]
        
        snake_rect = pygame.Rect(snake[-1][0], snake[-1][1], snake_size[0], snake_size[1])
        food_rect = pygame.Rect(food_x, food_y, snake_size[0], snake_size[1])
            #через колидерект        
        if snake_rect.colliderect(food_rect):
            food_x, food_y = spawn_food()
            length += 1
            score += 1
        
        # поверка поедания супер-еды
        superfood_rect = pygame.Rect(superfood_x, superfood_y, snake_size[0], snake_size[1])
        if snake_rect.colliderect(superfood_rect):
            superfood_x, superfood_y = spawn_food()
            length += 3
            score += 3
        
        #  набрал нужный скор для повышения уровня
        if score >= level_num * 15:
            reset_snake()
            level_num += 1
            updating_data(user_name, score,  length, level_num)
            level = Level(level_num)
            level.inc_speed()
            screen.fill(BLACK)
            screen.blit(font_large.render(f'LEVEL {level_num}', True, pygame.Color('yellow')), (WIDTH // 2 - 100, HEIGHT // 3))
            pygame.display.flip()
            pygame.time.wait(1000)
        
        # ударил себя или границы экрана == гг
        if (center_x < 0 or center_x > WIDTH - snake_size[0] or
            center_y < 0 or center_y > HEIGHT - snake_size[1] or
            len(snake) != len(set(snake))):
            game_over()
        
        # столкновения с блоками
        colision()
        
        # Управление направлением
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'D': True, 'A': True}
        elif pressed[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'D': True, 'A': True}
        elif pressed[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'D': True, 'A': False}
        elif pressed[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'D': False, 'A': True}
    else:
        screen.blit(font_large.render("PAUSE", True, pygame.Color('red')), (WIDTH // 2 - 100, HEIGHT // 3))
        show_tab()
    pygame.display.flip()