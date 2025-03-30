import pygame

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 20, 147)
BROWN = (139, 69, 19)
colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE, PINK, BROWN]
current_color = BLACK

# Переменные
drawing = False
mode = "pencil"  # Текущий режим рисования: карандаш, прямоугольник, круг, линия, квадрат, прямоугольный треугольник, равносторонний треугольник, ромб
start_pos = None
prev_pos = None
thickness = 2  # Толщина инструмента рисования

# Управление основным циклом
running = True
canvas = pygame.Surface((WIDTH, HEIGHT))  # Холст для рисования
canvas.fill(WHITE)  # Заполнение холста белым цветом

font = pygame.font.SysFont(None, 24)  # Шрифт для отображения текста


def draw_status():
    """
    Отображает текущий статус (режим, толщину и палитру цветов) на экране.
    """
    status_text = f"Mode: {mode} | Thickness: {thickness}"
    text_surface = font.render(status_text, True, BLACK)
    screen.blit(text_surface, (10, 10))

    # Отображение палитры цветов
    for i, color in enumerate(colors):
        rect_x = WIDTH - 300 + i * 30
        pygame.draw.rect(screen, color, (rect_x, 10, 20, 20))  # Отрисовка цветового блока
        pygame.draw.rect(screen, BLACK, (rect_x, 10, 20, 20), 1)  # Отрисовка рамки
        index_text = font.render(str(i), True, BLACK)
        screen.blit(index_text, (rect_x + 5, 35))  # Отображение индекса цвета
        if color == current_color:
            # Выделение выбранного цвета
            pygame.draw.rect(screen, BLACK, (rect_x - 2, 8, 24, 24), 2)


while running:
    screen.fill(WHITE)  # Очистка экрана
    screen.blit(canvas, (0, 0))  # Отрисовка холста
    draw_status()  # Обновление строки состояния

    # Обработка горячих клавиш для выбора цвета
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and pygame.K_0 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_0
                if index < len(colors):
                    current_color = colors[index]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Выход из программы
            running = False

        elif event.type == pygame.KEYDOWN:  # Обработка ввода с клавиатуры
            # Изменение режима рисования
            if event.key == pygame.K_1:
                mode = "pencil"
            elif event.key == pygame.K_2:
                mode = "rect"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "line"
            elif event.key == pygame.K_5:
                mode = "square"
            elif event.key == pygame.K_6:
                mode = "r_triangle"
            elif event.key == pygame.K_7:
                mode = "e_triangle"
            elif event.key == pygame.K_8:
                mode = "rhombus"
            elif event.key == pygame.K_c:  # Очистить холст
                canvas.fill(WHITE)
            elif event.key == pygame.K_UP:  # Увеличить толщину
                thickness += 1
            elif event.key == pygame.K_DOWN:  # Уменьшить толщину
                thickness = max(1, thickness - 1)
            elif event.key == pygame.K_s:  # Сохранить рисунок
                pygame.image.save(canvas, "drawing.png")
                print("Рисунок сохранен как drawing.png")

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Начать рисование
            if event.button == 1:  # ЛКМ
                drawing = True
                start_pos = event.pos
                prev_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:  # Закончить рисование
            if event.button == 1:  # ЛКМ
                drawing = False
                end_pos = event.pos
                # Рисование фигур на основе текущего режима
                if mode == "rect":
                    pygame.draw.rect(canvas, current_color, pygame.Rect(
                        start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), thickness)
                elif mode == "circle":
                    radius = int(
                        ((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(canvas, current_color,
                                       start_pos, radius, thickness)
                elif mode == "line":
                    pygame.draw.line(canvas, current_color,
                                     start_pos, end_pos, thickness)
                elif mode == "square":
                    side = min(abs(end_pos[0] - start_pos[0]),
                               abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(canvas, current_color, pygame.Rect(
                        start_pos, (side, side)), thickness)
                elif mode == "r_triangle":
                    pygame.draw.polygon(canvas, current_color, [
                                        start_pos, (start_pos[0], end_pos[1]), end_pos], thickness)
                elif mode == "e_triangle":
                    side_length = int(
                        ((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                    pygame.draw.polygon(canvas, current_color, [
                        start_pos,
                        (start_pos[0] + side_length, start_pos[1]),
                        (start_pos[0] + side_length // 2,
                         start_pos[1] - int(side_length * (3**0.5) / 2))
                    ], thickness)
                elif mode == "rhombus":
                    pygame.draw.polygon(canvas, current_color, [(start_pos[0], start_pos[1] - (end_pos[1] - start_pos[1]) // 2), (start_pos[0] - (end_pos[0] - start_pos[0]) // 2,
                                        start_pos[1]), (start_pos[0], start_pos[1] + (end_pos[1] - start_pos[1]) // 2), (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1])], thickness)

        elif event.type == pygame.MOUSEMOTION:  # Обработка рисования от руки
            if drawing and mode == "pencil":
                pygame.draw.line(canvas, current_color,
                                 prev_pos, event.pos, thickness)
                prev_pos = event.pos

    pygame.display.flip()  # Обновить экран

pygame.quit()
