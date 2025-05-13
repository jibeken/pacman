import pygame
import random
import sys
import math

pygame.init()

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

MENU = 0
PLAYING = 1
GAME_OVER = 2

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

        self.image = pygame.image.load('pacman.png')
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.mouth_open = not self.mouth_open
            self.animation_counter = 0

        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

        self.direction = self.next_direction

    def draw(self):
        screen.blit(self.image, (self.x - 15, self.y - 15))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

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

    def update(self, pacman):
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

        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

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
        self.pacman = PacMan(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.ghosts = [
            Ghost(100, 100, RED),
            Ghost(SCREEN_WIDTH - 100, 100, PINK),
            Ghost(100, SCREEN_HEIGHT - 100, CYAN),
            Ghost(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, ORANGE)
        ]
        self.dots = []
        self.score = 0
        self.lives = 3
        self.level = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##          ##.#     ",
            "######.## ###--### ##.######",
            "      .   #      #   .      ",
            "######.## ######## ##.######",
            "     #.##          ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#...##................##...#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################",
        ]

        for x in range(DOT_SIZE * 2, SCREEN_WIDTH, DOT_SIZE * 4):
            for y in range(DOT_SIZE * 2, SCREEN_HEIGHT, DOT_SIZE * 4):
                self.dots.append(Dot(x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = PLAYING
                elif self.state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset()
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
            self.pacman.update()

            for ghost in self.ghosts:
                ghost.update(self.pacman)

                if self.pacman.get_rect().colliderect(ghost.get_rect()):
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = GAME_OVER
                    else:
                        self.pacman.x = SCREEN_WIDTH // 2
                        self.pacman.y = SCREEN_HEIGHT // 2
                        for g in self.ghosts:
                            g.x = random.randint(50, SCREEN_WIDTH - 50)
                            g.y = random.randint(50, SCREEN_HEIGHT - 50)

            for dot in self.dots:
                if not dot.collected and self.pacman.get_rect().colliderect(dot.get_rect()):
                    dot.collected = True
                    self.score += SCORE_PER_DOT

            if all(dot.collected for dot in self.dots):
                self.state = GAME_OVER

    def draw(self):
        screen.fill(BLACK)

        if self.state == MENU:
            font = pygame.font.SysFont(None, 72)
            title = font.render("PAC-MAN", True, YELLOW)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

            font = pygame.font.SysFont(None, 36)
            instruction = font.render("Press SPACE to start", True, WHITE)
            screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2))

        elif self.state == PLAYING or self.state == GAME_OVER:
            for dot in self.dots:
                dot.draw()

            self.pacman.draw()

            for ghost in self.ghosts:
                ghost.draw()

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
            screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

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
    pygame.quit()