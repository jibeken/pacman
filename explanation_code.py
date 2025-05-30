Что такое Grid (Сетка) в Pacman?
Grid — это виртуальная сетка, которая делит игровое поле на одинаковые прямоугольные ячейки (клетки). В Pacman все объекты (стены, точки, Пакман, призраки) привязаны к этой сетке и двигаются строго по её линиям.

🔷 Как устроен Grid в вашем коде?
Из вашего фрагмента:

python
layout = LEVEL_LAYOUTS[level_index]          # Берём схему уровня (например, список строк)
cell_width = SCREEN_WIDTH // len(layout[0])  # Ширина 1 клетки
cell_height = SCREEN_HEIGHT // len(layout)   # Высота 1 клетки
LEVEL_LAYOUTS — это список уровней, где каждый уровень закодирован как список строк (например, ["#####", "#...#", "#####"]).

Символы (например, #, ., P) обозначают объекты:

# — стена

. — точка

P — стартовая позиция Пакмана

🔷 Пример Grid для Pacman
Допустим, у вас уровень задан так:

python
LEVEL_LAYOUTS = [
    [
        "#######",
        "#.....#",
        "#.###.#",
        "#.# #.#",
        "#######"
    ]
]
Это создаёт сетку 7x5 (7 клеток в ширину, 5 в высоту):

#######
#.....#
#.###.#
#.# #.#
#######
Каждая # — стена (занимает 1 клетку).

Каждая . — точка (также 1 клетку).

🔷 Как Grid используется в игре?
Размеры клеток

Если SCREEN_WIDTH = 700, а в уровне 7 столбцов, то:

python
cell_width = 700 // 7 = 100  # Ширина клетки = 100 пикселей
Координаты объектов вычисляются через номера клеток:

python
x = column_index * cell_width  # Горизонтальная позиция
y = row_index * cell_height    # Вертикальная позиция
Движение Пакмана и призраков

Они перемещаются на 1 клетку за шаг, а не на произвольное расстояние.

Проверка столкновений со стенами:

python
new_x = pacman.x + pacman.speed
new_col = new_x // cell_width  # Переводим пиксели в номер клетки
if layout[row][new_col] == "#":
    # Столкновение со стеной!
Размещение точек и стен

При загрузке уровня программа проходит по layout и расставляет объекты в центры клеток:

python
for row in range(len(layout)):
    for col in range(len(layout[row])):
        if layout[row][col] == ".":
            dot = Dot(col * cell_width + cell_width//2, 
                     row * cell_height + cell_height//2)
            self.dots.append(dot)
🔷 Зачем Grid в Pacman?
Простота управления

Движение «по клеткам» делает игру предсказуемой (как в шахматах).

Оптимизация коллизий

Проверять столкновения с сеткой проще, чем с произвольными формами.

Генерация уровней

Уровни легко редактировать через текстовые схемы.

🔷 Как визуализировать Grid?
Для отладки можно нарисовать сетку:

python
# Рисуем сетку (для отладки)
for x in range(0, SCREEN_WIDTH, cell_width):
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
for y in range(0, SCREEN_HEIGHT, cell_height):
    pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
Это поможет увидеть, правильно ли размещаются объекты.


# ==================== ИМПОРТЫ ====================
import math        # Библиотека для математических функций (sin, cos, sqrt и т.д.)
import pygame      # Библиотека для создания игр (рисование, звук, события)
import random      # Библиотека для случайных чисел
import sys         # Системная библиотека (для выхода из программы)

# ==================== ИНИЦИАЛИЗАЦИЯ PYGAME ====================
pygame.init()                    # Запускает все модули pygame
pygame.mixer.init()              # Запускает звуковую систему pygame

# ЗАГРУЗКА И ВОСПРОИЗВЕДЕНИЕ МУЗЫКИ
pygame.mixer_music.load("pac-man-1.mp3")  # Загружает музыкальный файл в память
pygame.mixer_music.play(1)                # Воспроизводит музыку 1 раз

# ОЖИДАНИЕ ОКОНЧАНИЯ ПЕРВОЙ МЕЛОДИИ
while pygame.mixer.music.get_busy():      # get_busy() возвращает True, если музыка играет
    pygame.time.Clock().tick(10)          # Ждёт 1/10 секунды (100 миллисекунд)

# ЗАГРУЗКА И ВОСПРОИЗВЕДЕНИЕ ВТОРОЙ МЕЛОДИИ
pygame.mixer_music.load("pac-man-2.mp3")  # Загружает вторую мелодию
pygame.mixer_music.play(2)                # Воспроизводит 2 раза

# ==================== КОНСТАНТЫ (НЕИЗМЕНЯЕМЫЕ ЗНАЧЕНИЯ) ====================
SCREEN_WIDTH = 800     # Ширина окна игры в пикселях
SCREEN_HEIGHT = 600    # Высота окна игры в пикселях
TILE_SIZE = 40         # Размер одной клетки лабиринта в пикселях
PACMAN_SPEED = 3       # Скорость движения Pac-Man (пикселей за кадр)
GHOST_SPEED = 2        # Скорость движения призраков (пикселей за кадр)
DOT_SIZE = 8           # Размер точек для сбора в пикселях
SCORE_PER_DOT = 10     # Количество очков за одну съеденную точку

# ЦВЕТА В ФОРМАТЕ RGB (Red, Green, Blue) - каждое значение от 0 до 255
BLACK = (0, 0, 0)           # Чёрный цвет (нет красного, зелёного, синего)
WHITE = (255, 255, 255)     # Белый цвет (максимум всех цветов)
YELLOW = (255, 255, 0)      # Жёлтый цвет (красный + зелёный, без синего)
RED = (255, 0, 0)           # Красный цвет (только красный)
PINK = (255, 192, 203)      # Розовый цвет
CYAN = (0, 255, 255)        # Голубой цвет (зелёный + синий)
ORANGE = (255, 165, 0)      # Оранжевый цвет
BLUE = (0, 0, 255)          # Синий цвет (только синий)
GREEN = (0, 255, 0)         # Зелёный цвет (только зелёный)
WALL_COLOR = (33, 33, 222)  # Цвет стен (тёмно-синий)

# СОЗДАНИЕ ОКНА ИГРЫ
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создаёт окно заданного размера
pygame.display.set_caption("Pac-Man")                           # Устанавливает заголовок окна
clock = pygame.time.Clock()                                      # Создаёт объект для контроля FPS

# СОСТОЯНИЯ ИГРЫ (как enum - перечисление)
MENU = 0              # Главное меню
PLAYING = 1           # Игра идёт
GAME_OVER = 2         # Игра окончена (проиграл)
WIN = 3               # Победа (прошёл все уровни)
LEVEL_COMPLETE = 4    # Уровень завершён

# ==================== КАРТЫ УРОВНЕЙ ====================
# Это двумерные массивы (списки списков), где каждая цифра означает тип клетки:
# 0 = пустое место (можно ходить)
# 1 = стена (нельзя проходить)
# 2 = точка (еда для Pac-Man)
# 3 = большая точка (power pellet - даёт силу)
# 4 = стартовая позиция Pac-Man
# 5 = стартовая позиция призрака 1
# 6 = стартовая позиция призрака 2
# 7 = стартовая позиция призрака 3
# 8 = стартовая позиция призрака 4

LEVEL_LAYOUTS = [
    # УРОВЕНЬ 1
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Верхняя стена
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],  # Ряд с точками
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],  # Стены и точки
        [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],  # Большие точки по углам
        # ... остальные строки уровня
    ],
    # УРОВЕНЬ 2 и УРОВЕНЬ 3 имеют похожую структуру
]

# ==================== КЛАСС СТЕНЫ ====================
class Wall:
    def __init__(self, x, y, width, height):
        """
        Конструктор класса Wall (стена)
        x, y - координаты левого верхнего угла
        width - ширина стены
        height - высота стены
        """
        # pygame.Rect создаёт прямоугольник для проверки столкновений
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        """
        Метод для рисования стены на экране
        """
        # pygame.draw.rect рисует прямоугольник
        # Параметры: (поверхность, цвет, прямоугольник)
        pygame.draw.rect(screen, WALL_COLOR, self.rect)

# ==================== КЛАСС PAC-MAN ====================
class PacMan:
    def __init__(self, x, y):
        """
        Конструктор Pac-Man
        x, y - начальные координаты
        """
        self.x = x                      # Позиция по горизонтали
        self.y = y                      # Позиция по вертикали
        self.radius = 15                # Радиус для столкновений
        self.direction = "right"        # Текущее направление движения
        self.next_direction = None      # Направление, куда хочет повернуть игрок
        self.speed = PACMAN_SPEED       # Скорость движения
        
        # ПЕРЕМЕННЫЕ ДЛЯ АНИМАЦИИ
        self.animation_frame = 0        # Текущий кадр анимации
        self.animation_speed = 0.2      # Скорость смены кадров
        self.mouth_open = True          # Открыт ли рот

        # ЗАГРУЗКА ИЗОБРАЖЕНИЙ
        # .convert_alpha() оптимизирует изображение для быстрого рисования
        self.image_open = pygame.image.load('pacman.png').convert_alpha()
        self.image_closed = pygame.image.load('pacman_closed.png').convert_alpha()

        # ИЗМЕНЕНИЕ РАЗМЕРА ИЗОБРАЖЕНИЙ
        # pygame.transform.scale изменяет размер изображения
        self.image_open = pygame.transform.scale(self.image_open, (30, 30))
        self.image_closed = pygame.transform.scale(self.image_closed, (30, 30))

        # СОХРАНЕНИЕ ОРИГИНАЛОВ ДЛЯ ПОВОРОТА
        # .copy() создаёт копию изображения
        self.original_open = self.image_open.copy()
        self.original_closed = self.image_closed.copy()

        # ПЕРЕМЕННЫЕ ДЛЯ ПЛАВНОГО ПОВОРОТА
        self.smooth_rotation = 0        # Текущий угол поворота
        self.rotation_speed = 5         # Скорость поворота

    def update(self, walls):
        """
        Метод обновления Pac-Man (вызывается каждый кадр)
        walls - список всех стен для проверки столкновений
        """
        
        # ========== АНИМАЦИЯ РОТА ==========
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2:    # Цикл анимации: 0-1-2-0-1-2...
            self.animation_frame = 0
        
        # Рот открыт в первой половине цикла (0-1), закрыт во второй (1-2)
        self.mouth_open = self.animation_frame < 1

        # ========== ПЛАВНЫЙ ПОВОРОТ ==========
        # Словарь соответствия направлений и углов поворота
        target_rotation = {
            "right": 0,      # Вправо - 0 градусов
            "left": 180,     # Влево - 180 градусов
            "up": 90,        # Вверх - 90 градусов
            "down": 270      # Вниз - 270 градусов
        }.get(self.direction, 0)  # .get() возвращает значение или 0 по умолчанию

        # Обработка перехода через 360/0 градусов
        if abs(self.smooth_rotation - target_rotation) > 180:
            if self.smooth_rotation < target_rotation:
                self.smooth_rotation += 360
            else:
                self.smooth_rotation -= 360

        # Плавная интерполяция к целевому углу (20% от разности каждый кадр)
        self.smooth_rotation += (target_rotation - self.smooth_rotation) * 0.2

        # ========== СОХРАНЕНИЕ СТАРОЙ ПОЗИЦИИ ==========
        old_x, old_y = self.x, self.y

        # ========== ПРОВЕРКА ПОВОРОТА ==========
        if self.next_direction and self.next_direction != self.direction:
            # Тестируем движение в новом направлении
            test_x, test_y = self.x, self.y
            
            # Вычисляем тестовую позицию
            if self.next_direction == "right":
                test_x += self.speed
            elif self.next_direction == "left":
                test_x -= self.speed
            elif self.next_direction == "up":
                test_y -= self.speed
            elif self.next_direction == "down":
                test_y += self.speed

            # Создаём тестовый прямоугольник для проверки столкновений
            test_rect = self.get_rect_at(test_x, test_y)
            can_turn = True
            
            # Проверяем столкновение со всеми стенами
            for wall in walls:
                if test_rect.colliderect(wall.rect):  # colliderect проверяет пересечение прямоугольников
                    can_turn = False
                    break  # Выходим из цикла при первом столкновении

            # Если можем повернуть, меняем направление
            if can_turn:
                self.direction = self.next_direction

        # ========== ДВИЖЕНИЕ ==========
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # ========== ПРОВЕРКА СТОЛКНОВЕНИЙ СО СТЕНАМИ ==========
        pacman_rect = self.get_rect()
        collision = False
        
        for wall in walls:
            if pacman_rect.colliderect(wall.rect):
                collision = True
                break

        # Если столкнулись, возвращаемся на старое место
        if collision:
            self.x, self.y = old_x, old_y
            # Ищем любое доступное направление
            self.direction = self.get_valid_direction(walls)
            self.next_direction = None

        # ========== ТЕЛЕПОРТАЦИЯ (ВЫХОД ЗА ГРАНИЦЫ ЭКРАНА) ==========
        if self.x < 0:                    # Вышли слева
            self.x = SCREEN_WIDTH         # Появляемся справа
        elif self.x > SCREEN_WIDTH:       # Вышли справа
            self.x = 0                    # Появляемся слева
        if self.y < 0:                    # Вышли сверху
            self.y = SCREEN_HEIGHT        # Появляемся снизу
        elif self.y > SCREEN_HEIGHT:      # Вышли снизу
            self.y = 0                    # Появляемся сверху

    def draw(self):
        """
        Метод рисования Pac-Man на экране
        """
        # Выбираем изображение в зависимости от состояния рта
        if self.mouth_open:
            base_image = self.original_open
        else:
            base_image = self.original_closed

        # Поворачиваем изображение на нужный угол
        rotated_image = pygame.transform.rotate(base_image, self.smooth_rotation)
        
        # Получаем прямоугольник для центрирования изображения
        rect = rotated_image.get_rect(center=(self.x, self.y))
        
        # Рисуем изображение на экране
        # screen.blit() копирует изображение на поверхность экрана
        screen.blit(rotated_image, rect.topleft)

    def get_rect(self):
        """
        Возвращает прямоугольник для проверки столкновений
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

    def get_rect_at(self, x, y):
        """
        Возвращает прямоугольник для заданной позиции
        Используется для тестирования столкновений
        """
        return pygame.Rect(x - self.radius, y - self.radius,
                          self.radius * 2, self.radius * 2)

    def get_valid_direction(self, walls):
        """
        Находит любое доступное направление движения
        Используется когда Pac-Man застрял
        """
        directions = ["right", "left", "up", "down"]
        
        for dir in directions:
            # Тестируем каждое направление
            test_x, test_y = self.x, self.y
            
            if dir == "right":
                test_x += self.speed
            elif dir == "left":
                test_x -= self.speed
            elif dir == "up":
                test_y -= self.speed
            elif dir == "down":
                test_y += self.speed

            test_rect = self.get_rect_at(test_x, test_y)
            collision = False
            
            # Проверяем столкновения
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    collision = True
                    break

            # Если направление свободно, возвращаем его
            if not collision:
                return dir

        # Если все направления заблокированы, остаёмся на месте
        return self.direction

# ==================== КЛАСС ПРИЗРАКА ====================
class Ghost:
    def __init__(self, x, y, color):
        """
        Конструктор призрака
        x, y - начальные координаты
        color - цвет призрака
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius = 15
        # random.choice выбирает случайный элемент из списка
        self.direction = random.choice(["right", "left", "up", "down"])
        self.speed = GHOST_SPEED
        self.change_direction_counter = 0  # Счётчик для смены направления

        # Загрузка и масштабирование изображения призрака
        self.image = pygame.image.load('ghost.webp')
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self, pacman, walls):
        """
        Обновление призрака (ИИ + движение)
        pacman - объект Pac-Man для преследования
        walls - список стен
        """
        self.change_direction_counter += 1
        
        # Каждые 60 кадров (примерно 1 секунда при 60 FPS) меняем стратегию
        if self.change_direction_counter >= 60:
            # random.random() возвращает случайное число от 0.0 до 1.0
            if random.random() < 0.7:  # 70% вероятность
                # ========== ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ ==========
                # Вычисляем расстояние до Pac-Man
                dx = pacman.x - self.x  # Разность по X
                dy = pacman.y - self.y  # Разность по Y

                # Выбираем направление к Pac-Man
                # abs() возвращает абсолютное значение (модуль числа)
                if abs(dx) > abs(dy):  # Если горизонтальное расстояние больше
                    # Двигаемся по горизонтали
                    self.direction = "right" if dx > 0 else "left"
                else:  # Если вертикальное расстояние больше
                    # Двигаемся по вертикали
                    self.direction = "down" if dy > 0 else "up"
            else:  # 30% вероятность
                # Случайное направление для непредсказуемости
                self.direction = random.choice(["right", "left", "up", "down"])

            self.change_direction_counter = 0  # Сбрасываем счётчик

        # ========== ДВИЖЕНИЕ ==========
        old_x, old_y = self.x, self.y  # Сохраняем старую позицию

        # Двигаемся в текущем направлении
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # ========== ПРОВЕРКА СТОЛКНОВЕНИЙ ==========
        ghost_rect = self.get_rect()
        for wall in walls:
            if ghost_rect.colliderect(wall.rect):
                # Если столкнулись со стеной, возвращаемся и меняем направление
                self.x, self.y = old_x, old_y
                self.direction = random.choice(["right", "left", "up", "down"])
                break

        # ========== ТЕЛЕПОРТАЦИЯ ==========
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        """
        Рисование призрака
        """
        # Рисуем изображение призрака, центрируя его по координатам
        screen.blit(self.image, (self.x - 15, self.y - 15))

    def get_rect(self):
        """
        Прямоугольник для столкновений
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# ==================== КЛАСС БОЛЬШОЙ ТОЧКИ ====================
class PowerPellet:
    def __init__(self, x, y):
        """
        Конструктор большой точки (power pellet)
        """
        self.x = x
        self.y = y
        self.radius = DOT_SIZE
        self.collected = False          # Собрана ли точка
        self.animation_counter = 0      # Счётчик для анимации

    def update(self):
        """
        Обновление анимации большой точки
        """
        self.animation_counter += 1
        if self.animation_counter >= 30:  # Сброс счётчика каждые 30 кадров
            self.animation_counter = 0

    def draw(self):
        """
        Рисование большой точки с пульсирующей анимацией
        """
        if not self.collected:
            # math.sin создаёт синусоидальную волну для пульсации
            # abs() делает все значения положительными
            size_mod = abs(math.sin(self.animation_counter * 0.1)) * 2
            
            # pygame.draw.circle рисует круг
            # Параметры: (поверхность, цвет, центр, радиус)
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius + size_mod)

    def get_rect(self):
        """
        Прямоугольник для проверки сбора
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# ==================== КЛАСС ОБЫЧНОЙ ТОЧКИ ====================
class Dot:
    def __init__(self, x, y):
        """
        Конструктор обычной точки
        """
        self.x = x
        self.y = y
        self.radius = DOT_SIZE // 2     # // - целочисленное деление
        self.collected = False

        # Загрузка изображения точки
        self.image = pygame.image.load('dot.png')
        self.image = pygame.transform.scale(self.image, (DOT_SIZE, DOT_SIZE))

    def draw(self):
        """
        Рисование точки
        """
        if not self.collected:
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def get_rect(self):
        """
        Прямоугольник для проверки сбора
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

# ==================== ГЛАВНЫЙ КЛАСС ИГРЫ ====================
class Game:
    def __init__(self):
        """
        Конструктор игры
        """
        self.reset()  # Инициализируем все переменные

    def reset(self):
        """
        Сброс игры к начальному состоянию
        """
        self.state = MENU               # Текущее состояние игры
        self.level = 0                  # Текущий уровень (начинаем с 0)
        self.pacman = None              # Объект Pac-Man
        self.ghosts = []                # Список призраков
        self.dots = []                  # Список обычных точек
        self.power_pellets = []         # Список больших точек
        self.walls = []                 # Список стен
        self.score = 0                  # Счёт игрока
        self.lives = 3                  # Количество жизней
        self.load_level(self.level)     # Загружаем первый уровень

    def load_level(self, level_index):
        """
        Загрузка уровня по индексу
        level_index - номер уровня в массиве LEVEL_LAYOUTS
        """
        # Проверяем, есть ли ещё уровни
        if level_index >= len(LEVEL_LAYOUTS):
            self.state = WIN  # Если уровни закончились - победа
            return

        # Очищаем все списки объектов
        self.dots = []
        self.power_pellets = []
        self.walls = []
        self.ghosts = []

        # Получаем карту текущего уровня
        layout = LEVEL_LAYOUTS[level_index]
        
        # Вычисляем размер одной клетки
        cell_width = SCREEN_WIDTH // len(layout[0])   # // - целочисленное деление
        cell_height = SCREEN_HEIGHT // len(layout)

        # Переменные для запоминания позиций
        pacman_pos = None
        ghost_positions = []

        # ========== ПАРСИНГ КАРТЫ ==========
        # enumerate() возвращает индекс и значение для каждого элемента
        for y, row in enumerate(layout):        # y - номер строки, row - сама строка
            for x, cell in enumerate(row):      # x - номер столбца, cell - значение клетки
                # Вычисляем центр клетки
                cell_x = x * cell_width + cell_width // 2
                cell_y = y * cell_height + cell_height // 2

                if cell == 1:  # Стена
                    # Создаём стену на всю клетку
                    self.walls.append(Wall(x * cell_width, y * cell_height, 
                                         cell_width, cell_height))
                elif cell == 2:  # Обычная точка
                    self.dots.append(Dot(cell_x, cell_y))
                elif cell == 3:  # Большая точка
                    self.power_pellets.append(PowerPellet(cell_x, cell_y))
                elif cell == 4:  # Стартовая позиция Pac-Man
                    pacman_pos = (cell_x, cell_y)
                elif cell >= 5 and cell <= 8:  # Стартовые позиции призраков
                    # cell - 5 даёт индекс призрака (0, 1, 2, 3)
                    ghost_positions.append((cell_x, cell_y, cell - 5))

        # ========== СОЗДАНИЕ PAC-MAN ==========
        if pacman_pos:  # Если нашли позицию на карте
            self.pacman = PacMan(pacman_pos[0], pacman_pos[1])
        else:  # Если не нашли, ставим в центр экрана
            self.pacman = PacMan(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # ========== СОЗДАНИЕ ПРИЗРАКОВ ==========
        ghost_colors = [RED, PINK, CYAN, ORANGE]  # Цвета для 4 призраков
        
        for pos in ghost_positions:
            # pos[0] = x, pos[1] = y, pos[2] = индекс цвета
            self.ghosts.append(Ghost(pos[0], pos[1], ghost_colors[pos[2]]))

        # Если на карте не указаны призраки, создаём стандартных
        if not self.ghosts:  # Если список пустой
            self.ghosts = [
                Ghost(100, 100, RED),
                Ghost(SCREEN_WIDTH - 100, 100, PINK),
                Ghost(100, SCREEN_HEIGHT - 100, CYAN),
                Ghost(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, ORANGE)
            ]

    def handle_events(self):
        """
        Обработка событий (нажатия клавиш, закрытие окна)
        """
        # pygame.event.get() возвращает список всех событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажали крестик закрытия окна
                pygame.quit()  # Закрываем pygame
                sys.exit()     # Выходим из программы

            if event.type == pygame.KEYDOWN:  # Нажали клавишу
                if self.state == MENU:  # В главном меню
                    if event.key == pygame.K_SPACE:  # Нажали пробел
                        self.state = PLAYING
                        
                elif self.state == GAME_OVER or self.state == WIN:  # Игра окончена
                    if event.key == pygame.K_SPACE:  # Пробел для перезапуска
                        self.reset()
                        
                elif self.state == LEVEL_COMPLETE:  # Уровень завершён
                    if event.key == pygame.K_SPACE:  # Пробел для следующего уровня
                        self.level += 1
                        self.load_level(self.level)
                        self.state = PLAYING
                        
                elif self.state == PLAYING:  # Во время игры
                    # УПРАВЛЕНИЕ PAC-MAN
                    if event.key == pygame.K_RIGHT:    # Стрелка вправо
                        self.pacman.next_direction = "right"
                    elif event.key == pygame.K_LEFT:   # Стрелка влево
                        self.pacman.next_direction = "left"
                    elif event.key == pygame.K_UP:     # Стрелка вверх
                        self.pacman.next_direction = "up"
                    elif event.key == pygame.K_DOWN:   # Стрелка вниз
                        self.pacman.next_direction = "down"

    def update(self):
        """
        Обновление логики игры (вызывается каждый кадр)
        """
        if self.state == PLAYING:  # Только если игра идёт
            
            # ========== ОБНОВЛЕНИЕ PAC-MAN ==========
            self.pacman.update(self.walls)

            # ========== ОБНОВЛЕНИЕ ПРИЗРАКОВ ==========
            for ghost in self.ghosts:
                ghost.update(self.pacman, self.walls)

                # ПРОВЕРКА СТОЛКНОВЕНИЯ PAC-MAN С ПРИЗРАКОМ
                if self.pacman.get_rect().colliderect(ghost.get_rect()):
                    self.lives -= 1  # Отнимаем жизнь
                    if self.lives <= 0:  # Если жизни закончились
                        self.state = GAME_OVER
                    else:
                        # Перезагружаем уровень (сброс позиций)
                        self.load_level(self.level)
                        break  # Выходим из цикла призраков

            # ========== СБОР ОБЫЧНЫХ ТОЧЕК ==========
            for dot in self.dots:
                # Проверяем: точка не собрана И Pac-Man касается её
                if not dot.collected and self.pacman.get_rect().colliderect(dot.get_rect()):
                    dot.collected = True           # Помечаем как собранную
                    self.score += SCORE_PER_DOT    # Добавляем очки

            # ========== СБОР БОЛЬШИХ ТОЧЕК ==========
            for pellet in self.power_pellets:
                if not pellet.collected and self.pacman.get_rect().colliderect(pellet.get_rect()):
                    pellet.collected = True
                    self.score += SCORE_PER_DOT * 5  # Больше очков за большую точку
                    # TODO: Здесь можно добавить уязвимость призраков

            # ========== ПРОВЕРКА ЗАВЕРШЕНИЯ УРОВНЯ ==========
            # all() возвращает True, если все элементы True
            all_dots_collected = all(dot.collected for dot in self.dots)
            all_pellets_collected = all(pellet.collected for pellet in self.power_pellets)
            
            if all_dots_collected and all_pellets_collected:
                if self.level < len(LEVEL_LAYOUTS) - 1:  # Есть ещё уровни
                    self.state = LEVEL_COMPLETE
                else:  # Это был последний уровень
                    self.state = WIN

    def draw(self):
        """
        Отрисовка всего на экране
        """
        screen.fill(BLACK)  # Заливаем экран чёрным цветом

        if self.state == MENU:
            # ========== ГЛАВНОЕ МЕНЮ ==========
            # pygame.font.SysFont создаёт шрифт (None = системный шрифт, 72 = размер)
            font = pygame.font.SysFont(None, 72)
            # .render создаёт изображение текста (текст, сглаживание, цвет)
            title = font.render("PAC-MAN", True, YELLOW)
            # Центрируем заголовок
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

            font = pygame.font.SysFont(None, 36)
            instruction = font.render("Press SPACE to start", True, WHITE)
            screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2))

        elif self.state == PLAYING or self.state == GAME_OVER or self.state == LEVEL_COMPLETE or self.state == WIN:
            # ========== ИГРОВОЙ ЭКРАН ==========
            
            # Рисуем стены
            for wall in self.walls:
                wall.draw()

            # Рисуем обычные точки
            for dot in self.dots:
                dot.draw()

            # Рисуем и обновляем большие точки
            for pellet in self.power_pellets:
                pellet.update()  # Обновляем анимацию
                pellet.draw()

            # Рисуем Pac-Man
            self.pacman.draw()

            # Рисуем призраков
            for ghost in self.ghosts:
                ghost.draw()

            # ========== ИНТЕРФЕЙС ==========
            font = pygame.font.SysFont(None, 36)
            
            # Счёт (слева вверху)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Жизни (справа вверху)
            lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
            screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

            # Уровень (по центру вверху)
            level_text = font.render(f"Level: {self.level + 1}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

            # ========== ЭКРАНЫ ОКОНЧАНИЯ ==========
            if self.state == GAME_OVER:
                # Полупрозрачный чёрный фон
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))  # 128 = 50% прозрачности
                screen.blit(overlay, (0, 0))

                font = pygame.font.SysFont(None, 72)
                game_over = font.render("GAME OVER", True, RED)
                screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 3))

                font = pygame.font.SysFont(None, 48)
                final_score = font.render(f"Final Score: {self.score}", True, WHITE)
                screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2))

                font = pygame.font.SysFont(None, 36)
                restart = font.render("Press SPACE to restart", True, WHITE)
                screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

            elif self.state == WIN:
                # Аналогично экрану Game Over, но с текстом победы
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))

                font = pygame.font.SysFont(None, 72)
                win_text = font.render("YOU WIN!", True, GREEN)
                screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 3))

                # ... остальной код аналогично

            elif self.state == LEVEL_COMPLETE:
                # Экран завершения уровня
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))

                font = pygame.font.SysFont(None, 72)
                level_complete = font.render(f"LEVEL {self.level + 1} COMPLETE!", True, GREEN)
                screen.blit(level_complete, (SCREEN_WIDTH // 2 - level_complete.get_width() // 2, SCREEN_HEIGHT // 3))

                # ... остальной код

        # pygame.display.flip() обновляет весь экран (показывает всё нарисованное)
        pygame.display.flip()

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    """
    Главная функция программы
    """
    game = Game()  # Создаём объект игры

    running = True
    while running:  # Главный игровой цикл
        game.handle_events()  # Обрабатываем события (клавиши, мышь)
        game.update()         # Обновляем логику игры
        game.draw()           # Рисуем всё на экране
        clock.tick(60)        # Ограничиваем до 60 FPS (кадров в секунду)

# ==================== ЗАПУСК ПРОГРАММЫ ====================
if __name__ == "__main__":  # Если файл запущен напрямую (не импортирован)
    main()                  # Запускаем главную функцию
    pygame.mixer.quit()     # Закрываем звуковую систему
    pygame.quit()           # Закрываем pygame
