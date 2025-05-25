import math
import pygame
import random
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("pacman_playing_song.mp3")
pygame.mixer.music.play(-1)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
PACMAN_SPEED = 3
GHOST_SPEED = 2
DOT_SIZE = 8
SCORE_PER_DOT = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WALL_COLOR = (33, 33, 222)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3
LEVEL_COMPLETE = 4

# Define maze layouts for different levels
# 0 = empty space, 1 = wall, 2 = dot position, 3 = power pellet, 4 = pacman start, 5-8 = ghost starts
LEVEL_LAYOUTS = [
    # Level 1 - Simple maze
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
        [0, 0, 0, 1, 2, 1, 0, 0, 0, 5, 6, 0, 0, 0, 1, 2, 1, 0, 0, 0],
        [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
        [0, 0, 0, 0, 2, 0, 0, 1, 7, 8, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
        [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
        [0, 0, 0, 1, 2, 1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
        [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 3, 2, 1, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 1, 2, 3, 1],
        [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # Level 2 - More complex maze
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 0, 0, 1, 2, 1, 0, 0, 0, 5, 6, 0, 0, 0, 1, 2, 1, 0, 0, 1],
        [1, 0, 0, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 0, 0, 1],
        [1, 0, 0, 1, 2, 0, 0, 1, 7, 8, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1],
        [1, 0, 0, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 0, 0, 1],
        [1, 0, 0, 1, 2, 1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 2, 1, 0, 0, 1],
        [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 3, 2, 1, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 1, 2, 3, 1],
        [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # Level 3 - Advanced maze
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0, 1, 2, 1],
        [1, 2, 1, 0, 1, 1, 0, 1, 2, 1, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1],
        [1, 2, 1, 0, 1, 1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 1, 0, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [0, 0, 0, 1, 2, 1, 7, 0, 0, 8, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
        [1, 1, 1, 1, 2, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1],
        [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

class PacMan:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.direction = "right"
        self.next_direction = "right"
        self.speed = PACMAN_SPEED
        self.mouth_open = True
        self.mouth_angle = 45
        self.animation_counter = 0
        self.rotation = 0  # Rotation angle in degrees
        # Добавляем переменные для плавного поворота
        self.turning_point = None
        self.align_threshold = self.speed  # Порог для выравнивания по сетке

        self.image = pygame.image.load('pacman.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.original_image = self.image.copy()
        self.images = [
            pygame.image.load("pacman.png"),
            pygame.image.load("pacman_close.png")
        ]
        self.animation_index = 0
        self.animation_timer = 0
        self.image = self.images[self.animation_index]

    def update(self, walls):

        self.animation_timer += 1


        if self.animation_timer >= 5:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]
            self.animation_timer = 0

        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.mouth_open = not self.mouth_open
            self.animation_counter = 0

        # Store current position to revert if collision occurs
        old_x, old_y = self.x, self.y

        # Получаем размер ячейки лабиринта
        cell_width = SCREEN_WIDTH // len(LEVEL_LAYOUTS[0][0])
        cell_height = SCREEN_HEIGHT // len(LEVEL_LAYOUTS[0])

        # Проверяем, можно ли повернуть в запрошенном направлении
        if self.next_direction != self.direction:
            # Вычисляем центр текущей ячейки
            current_cell_x = round(self.x / cell_width) * cell_width + cell_width // 2
            current_cell_y = round(self.y / cell_height) * cell_height + cell_height // 2

            # Проверяем, близок ли Pac-Man к центру ячейки для поворота
            x_aligned = abs(self.x - current_cell_x) < self.align_threshold
            y_aligned = abs(self.y - current_cell_y) < self.align_threshold

            # Если Pac-Man движется горизонтально и хочет повернуть вертикально
            if self.direction in ["left", "right"] and self.next_direction in ["up", "down"]:
                if x_aligned:
                    # Выравниваем по центру ячейки по X для плавного поворота
                    self.x = current_cell_x

                    # Проверяем, возможен ли поворот (нет ли стены)
                    test_y = self.y
                    if self.next_direction == "up":
                        test_y -= self.speed
                    else:  # down
                        test_y += self.speed

                    test_rect = pygame.Rect(self.x - self.radius, test_y - self.radius,
                                            self.radius * 2, self.radius * 2)

                    collision = False
                    for wall in walls:
                        if test_rect.colliderect(wall.rect):
                            collision = True
                            break

                    if not collision:
                        self.direction = self.next_direction

            # Если Pac-Man движется вертикально и хочет повернуть горизонтально
            elif self.direction in ["up", "down"] and self.next_direction in ["left", "right"]:
                if y_aligned:
                    # Выравниваем по центру ячейки по Y для плавного поворота
                    self.y = current_cell_y

                    # Проверяем, возможен ли поворот (нет ли стены)
                    test_x = self.x
                    if self.next_direction == "left":
                        test_x -= self.speed
                    else:  # right
                        test_x += self.speed

                    test_rect = pygame.Rect(test_x - self.radius, self.y - self.radius,
                                            self.radius * 2, self.radius * 2)

                    collision = False
                    for wall in walls:
                        if test_rect.colliderect(wall.rect):
                            collision = True
                            break

                    if not collision:
                        self.direction = self.next_direction

        # Move in the current direction
        if self.direction == "right":
            self.x += self.speed
            self.rotation = 0
        elif self.direction == "left":
            self.x -= self.speed
            self.rotation = 180
        elif self.direction == "up":
            self.y -= self.speed
            self.rotation = 90
        elif self.direction == "down":
            self.y += self.speed
            self.rotation = 270

        # Check for collision with walls
        pacman_rect = self.get_rect()
        collision_occurred = False
        for wall in walls:
            if pacman_rect.colliderect(wall.rect):
                collision_occurred = True

                # Пытаемся "скользить" вдоль стены вместо полной остановки
                # Сначала пробуем сохранить движение по X
                slide_x = True
                self.y = old_y
                slide_rect_x = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                           self.radius * 2, self.radius * 2)

                for w in walls:
                    if slide_rect_x.colliderect(w.rect):
                        slide_x = False
                        break

                # Если скольжение по X невозможно, пробуем по Y
                if not slide_x:
                    slide_y = True
                    self.x = old_x
                    self.y = old_y + (
                        self.speed if self.direction == "down" else -self.speed if self.direction == "up" else 0)

                    slide_rect_y = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                               self.radius * 2, self.radius * 2)

                    for w in walls:
                        if slide_rect_y.colliderect(w.rect):
                            slide_y = False
                            break

                    # Если и скольжение по Y невозможно, возвращаемся на старую позицию
                    if not slide_y:
                        self.x, self.y = old_x, old_y

                break

        # В методе update() или move() класса Pacman:

        def update(self):
            # Текущая логика движения тут
            self.rect.x += self.dx
            self.rect.y += self.dy

            # --- Телепорт слева направо и наоборот ---
            if self.rect.right < 0:
                self.rect.left = 600  # экран шириной 600
            elif self.rect.left > 600:
                self.rect.right = 0

        # Если произошла коллизия, попробуем автоматически изменить направление
        if collision_occurred:
            # Проверяем, можно ли двигаться в направлении next_direction
            if self.next_direction != self.direction:
                test_x, test_y = old_x, old_y

                if self.next_direction == "right":
                    test_x += self.speed
                elif self.next_direction == "left":
                    test_x -= self.speed
                elif self.next_direction == "up":
                    test_y -= self.speed
                elif self.next_direction == "down":
                    test_y += self.speed

                test_rect = pygame.Rect(test_x - self.radius, test_y - self.radius,
                                        self.radius * 2, self.radius * 2)

                can_turn = True
                for wall in walls:
                    if test_rect.colliderect(wall.rect):
                        can_turn = False
                        break

                if can_turn:
                    self.direction = self.next_direction
                    self.x, self.y = test_x, test_y

        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def get_valid_direction(self, walls):
        # Return a valid direction if current direction causes collision
        directions = ["right", "left", "up", "down"]
        valid_directions = []

        for dir in directions:
            test_x, test_y = self.x, self.y
            if dir == "right":
                test_x += self.speed
            elif dir == "left":
                test_x -= self.speed
            elif dir == "up":
                test_y -= self.speed
            elif dir == "down":
                test_y += self.speed

            test_rect = pygame.Rect(test_x - self.radius, test_y - self.radius, self.radius * 2, self.radius * 2)
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    collision = True
                    break

            if not collision:
                valid_directions.append(dir)

        if valid_directions:
            return valid_directions[0]  # Return first valid direction
        return self.direction  # If all directions cause collision, keep current

    def draw(self):
        # Rotate the image based on direction
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        # Get the rect of the rotated image and set its center to the pacman's position
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, WALL_COLOR, self.rect)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 15
        self.direction = random.choice(["right", "left", "up", "down"])
        self.speed = GHOST_SPEED
        self.change_direction_counter = 0

        self.image = pygame.image.load('ghost.webp')
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self, pacman, walls):
        self.change_direction_counter += 1
        if self.change_direction_counter >= 60:
            if random.random() < 0.7:
                dx = pacman.x - self.x
                dy = pacman.y - self.y

                if abs(dx) > abs(dy):
                    self.direction = "right" if dx > 0 else "left"
                else:
                    self.direction = "down" if dy > 0 else "up"
            else:
                self.direction = random.choice(["right", "left", "up", "down"])

            self.change_direction_counter = 0

        # Store current position to revert if collision occurs
        old_x, old_y = self.x, self.y

        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Check for collision with walls
        ghost_rect = self.get_rect()
        for wall in walls:
            if ghost_rect.colliderect(wall.rect):
                self.x, self.y = old_x, old_y
                self.direction = random.choice(["right", "left", "up", "down"])
                break

        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        screen.blit(self.image, (self.x - 15, self.y - 15))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class PowerPellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = DOT_SIZE
        self.collected = False
        self.animation_counter = 0

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= 30:
            self.animation_counter = 0

    def draw(self):
        if not self.collected:
            # Pulsating effect
            size_mod = abs(math.sin(self.animation_counter * 0.1)) * 2
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius + size_mod)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = DOT_SIZE // 2
        self.collected = False

        self.image = pygame.image.load('dot.png')
        self.image = pygame.transform.scale(self.image, (DOT_SIZE, DOT_SIZE))

    def draw(self):
        if not self.collected:
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = MENU
        self.level = 0
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.power_pellets = []
        self.walls = []
        self.score = 0
        self.lives = 3
        self.load_level(self.level)

    def load_level(self, level_index):
        if level_index >= len(LEVEL_LAYOUTS):
            self.state = WIN
            return

        self.dots = []
        self.power_pellets = []
        self.walls = []
        self.ghosts = []

        layout = LEVEL_LAYOUTS[level_index]
        cell_width = SCREEN_WIDTH // len(layout[0])
        cell_height = SCREEN_HEIGHT // len(layout)

        pacman_pos = None
        ghost_positions = []

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                cell_x = x * cell_width + cell_width // 2
                cell_y = y * cell_height + cell_height // 2

                if cell == 1:  # Wall
                    self.walls.append(Wall(x * cell_width, y * cell_height, cell_width, cell_height))
                elif cell == 2:  # Dot
                    self.dots.append(Dot(cell_x, cell_y))
                elif cell == 3:  # Power Pellet
                    self.power_pellets.append(PowerPellet(cell_x, cell_y))
                elif cell == 4:  # Pacman start
                    pacman_pos = (cell_x, cell_y)
                elif cell >= 5 and cell <= 8:  # Ghost starts
                    ghost_positions.append((cell_x, cell_y, cell - 5))

        # Create Pacman
        if pacman_pos:
            self.pacman = PacMan(pacman_pos[0], pacman_pos[1])
        else:
            self.pacman = PacMan(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Create Ghosts
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        for pos in ghost_positions:
            self.ghosts.append(Ghost(pos[0], pos[1], ghost_colors[pos[2]]))

        # If no ghosts defined in the layout, create default ones
        if not self.ghosts:
            self.ghosts = [
                Ghost(100, 100, RED),
                Ghost(SCREEN_WIDTH - 100, 100, PINK),
                Ghost(100, SCREEN_HEIGHT - 100, CYAN),
                Ghost(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, ORANGE)
            ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = PLAYING
                elif self.state == GAME_OVER or self.state == WIN:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                elif self.state == LEVEL_COMPLETE:
                    if event.key == pygame.K_SPACE:
                        self.level += 1
                        self.load_level(self.level)
                        self.state = PLAYING
                elif self.state == PLAYING:
                    if event.key == pygame.K_RIGHT:
                        self.pacman.next_direction = "right"
                    elif event.key == pygame.K_LEFT:
                        self.pacman.next_direction = "left"
                    elif event.key == pygame.K_UP:
                        self.pacman.next_direction = "up"
                    elif event.key == pygame.K_DOWN:
                        self.pacman.next_direction = "down"

    def update(self):
        if self.state == PLAYING:
            self.pacman.update(self.walls)

            for ghost in self.ghosts:
                ghost.update(self.pacman, self.walls)

                if self.pacman.get_rect().colliderect(ghost.get_rect()):
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = GAME_OVER
                    else:
                        # Reset positions but keep the level
                        self.load_level(self.level)
                        break

            for dot in self.dots:
                if not dot.collected and self.pacman.get_rect().colliderect(dot.get_rect()):
                    dot.collected = True
                    self.score += SCORE_PER_DOT

            for pellet in self.power_pellets:
                if not pellet.collected and self.pacman.get_rect().colliderect(pellet.get_rect()):
                    pellet.collected = True
                    self.score += SCORE_PER_DOT * 5
                    # TODO: Make ghosts vulnerable

            # Check if all dots and power pellets are collected
            if all(dot.collected for dot in self.dots) and all(pellet.collected for pellet in self.power_pellets):
                if self.level < len(LEVEL_LAYOUTS) - 1:
                    self.state = LEVEL_COMPLETE
                else:
                    self.state = WIN

    def draw(self):
        screen.fill(BLACK)

        if self.state == MENU:
            font = pygame.font.SysFont(None, 72)
            title = font.render("PAC-MAN", True, YELLOW)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

            font = pygame.font.SysFont(None, 36)
            instruction = font.render("Press SPACE to start", True, WHITE)
            screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2))

        elif self.state == PLAYING or self.state == GAME_OVER or self.state == LEVEL_COMPLETE or self.state == WIN:
            # Draw walls
            for wall in self.walls:
                wall.draw()

            # Draw dots
            for dot in self.dots:
                dot.draw()

            # Draw power pellets
            for pellet in self.power_pellets:
                pellet.update()
                pellet.draw()

            self.pacman.draw()

            for ghost in self.ghosts:
                ghost.draw()

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
            screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

            level_text = font.render(f"Level: {self.level + 1}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

            if self.state == GAME_OVER:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
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
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))

                font = pygame.font.SysFont(None, 72)
                win_text = font.render("YOU WIN!", True, GREEN)
                screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 3))

                font = pygame.font.SysFont(None, 48)
                final_score = font.render(f"Final Score: {self.score}", True, WHITE)
                screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2))

                font = pygame.font.SysFont(None, 36)
                restart = font.render("Press SPACE to restart", True, WHITE)
                screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

            elif self.state == LEVEL_COMPLETE:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))

                font = pygame.font.SysFont(None, 72)
                level_complete = font.render(f"LEVEL {self.level + 1} COMPLETE!", True, GREEN)
                screen.blit(level_complete, (SCREEN_WIDTH // 2 - level_complete.get_width() // 2, SCREEN_HEIGHT // 3))

                font = pygame.font.SysFont(None, 48)
                current_score = font.render(f"Score: {self.score}", True, WHITE)
                screen.blit(current_score, (SCREEN_WIDTH // 2 - current_score.get_width() // 2, SCREEN_HEIGHT // 2))

                font = pygame.font.SysFont(None, 36)
                next_level = font.render("Press SPACE for next level", True, WHITE)
                screen.blit(next_level, (SCREEN_WIDTH // 2 - next_level.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()


def main():
    game = Game()

    running = True
    while running:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.mixer.quit()
    pygame.quit()
