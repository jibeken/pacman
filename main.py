import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 3
GHOST_SPEED = 2
DOT_SIZE = 8
WALL_COLOR = (0, 0, 255)  # Blue
DOT_COLOR = (255, 255, 0)  # Yellow
SCORE_COLOR = (255, 255, 255)  # White
BG_COLOR = (0, 0, 0)  # Black

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont('Arial', 24)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.speed = PLAYER_SPEED
        self.mouth_open = True
        self.mouth_counter = 0
        
        # COMMENT: Replace this with your Pac-Man image
        # self.image = pygame.image.load('pacman.png')
        # self.image = pygame.transform.scale(self.image, (30, 30))
        
    def update(self, walls):
        # Movement based on direction
        dx, dy = 0, 0
        if self.direction == 0:  # Right
            dx = self.speed
        elif self.direction == 1:  # Down
            dy = self.speed
        elif self.direction == 2:  # Left
            dx = -self.speed
        elif self.direction == 3:  # Up
            dy = -self.speed
        
        # Check if the new position would collide with a wall
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Simple collision detection with walls
        can_move = True
        for wall in walls:
            if wall.colliderect(pygame.Rect(new_x - self.radius, new_y - self.radius, 
                                           self.radius * 2, self.radius * 2)):
                can_move = False
                break
        
        if can_move:
            self.x = new_x
            self.y = new_y
        
        # Wrap around the screen
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
            
        # Animate mouth
        self.mouth_counter += 1
        if self.mouth_counter >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_counter = 0
    
    def draw(self):
        # If using images, uncomment this:
        # rotated_image = pygame.transform.rotate(self.image, -90 * self.direction)
        # screen.blit(rotated_image, (self.x - self.radius, self.y - self.radius))
        
        # For now, draw a simple circle with a "mouth"
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
        
        if self.mouth_open:
            # Draw mouth based on direction
            if self.direction == 0:  # Right
                pygame.draw.polygon(screen, BG_COLOR, [
                    (self.x, self.y),
                    (self.x + self.radius, self.y - self.radius // 2),
                    (self.x + self.radius, self.y + self.radius // 2)
                ])
            elif self.direction == 1:  # Down
                pygame.draw.polygon(screen, BG_COLOR, [
                    (self.x, self.y),
                    (self.x - self.radius // 2, self.y + self.radius),
                    (self.x + self.radius // 2, self.y + self.radius)
                ])
            elif self.direction == 2:  # Left
                pygame.draw.polygon(screen, BG_COLOR, [
                    (self.x, self.y),
                    (self.x - self.radius, self.y - self.radius // 2),
                    (self.x - self.radius, self.y + self.radius // 2)
                ])
            elif self.direction == 3:  # Up
                pygame.draw.polygon(screen, BG_COLOR, [
                    (self.x, self.y),
                    (self.x - self.radius // 2, self.y - self.radius),
                    (self.x + self.radius // 2, self.y - self.radius)
                ])

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color
        self.speed = GHOST_SPEED
        self.direction = random.randint(0, 3)
        self.change_direction_counter = 0
        
        # COMMENT: Replace this with your Ghost image
        # self.image = pygame.image.load(f'ghost_{color}.png')
        # self.image = pygame.transform.scale(self.image, (30, 30))
    
    def update(self, player, walls):
        # Occasionally change direction randomly or chase player
        self.change_direction_counter += 1
        if self.change_direction_counter >= 60:  # Change direction every ~2 seconds
            # 70% chance to chase player, 30% chance for random movement
            if random.random() < 0.7:
                # Chase the player
                dx = player.x - self.x
                dy = player.y - self.y
                
                # Determine best direction to chase player
                if abs(dx) > abs(dy):
                    self.direction = 0 if dx > 0 else 2  # Right or Left
                else:
                    self.direction = 1 if dy > 0 else 3  # Down or Up
            else:
                # Random direction
                self.direction = random.randint(0, 3)
            
            self.change_direction_counter = 0
        
        # Movement based on direction
        dx, dy = 0, 0
        if self.direction == 0:  # Right
            dx = self.speed
        elif self.direction == 1:  # Down
            dy = self.speed
        elif self.direction == 2:  # Left
            dx = -self.speed
        elif self.direction == 3:  # Up
            dy = -self.speed
        
        # Check if the new position would collide with a wall
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Simple collision detection with walls
        can_move = True
        for wall in walls:
            if wall.colliderect(pygame.Rect(new_x - self.radius, new_y - self.radius, 
                                           self.radius * 2, self.radius * 2)):
                can_move = False
                # Choose a new random direction if blocked
                self.direction = random.randint(0, 3)
                break
        
        if can_move:
            self.x = new_x
            self.y = new_y
        
        # Wrap around the screen
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
    
    def draw(self):
        # If using images, uncomment this:
        # screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
        # For now, draw a simple ghost shape
        # Body
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(screen, self.color, (self.x - self.radius, self.y, self.radius * 2, self.radius))
        
        # Bottom wave
        pygame.draw.polygon(screen, self.color, [
            (self.x - self.radius, self.y + self.radius),
            (self.x - self.radius * 2/3, self.y + self.radius * 4/3),
            (self.x - self.radius * 1/3, self.y + self.radius),
            (self.x, self.y + self.radius * 4/3),
            (self.x + self.radius * 1/3, self.y + self.radius),
            (self.x + self.radius * 2/3, self.y + self.radius * 4/3),
            (self.x + self.radius, self.y + self.radius)
        ])
        
        # Eyes
        pygame.draw.circle(screen, (255, 255, 255), (self.x - 5, self.y - 3), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 5, self.y - 3), 4)
        pygame.draw.circle(screen, (0, 0, 255), (self.x - 5, self.y - 3), 2)
        pygame.draw.circle(screen, (0, 0, 255), (self.x + 5, self.y - 3), 2)

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = DOT_SIZE // 2
        self.collected = False
    
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, DOT_COLOR, (self.x, self.y), self.radius)
    
    def check_collision(self, player):
        if not self.collected:
            distance = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
            if distance < player.radius + self.radius:
                self.collected = True
                return True
        return False

def create_walls():
    walls = []
    
    # Outer walls
    wall_thickness = 20
    
    # Top and bottom walls
    walls.append(pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness))
    walls.append(pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness))
    
    # Left and right walls
    walls.append(pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT))
    walls.append(pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT))
    
    # Some inner walls
    walls.append(pygame.Rect(150, 150, 200, 30))
    walls.append(pygame.Rect(450, 150, 200, 30))
    walls.append(pygame.Rect(150, 400, 200, 30))
    walls.append(pygame.Rect(450, 400, 200, 30))
    walls.append(pygame.Rect(350, 250, 100, 100))
    
    return walls

def create_dots(walls):
    dots = []
    dot_spacing = 40
    
    for x in range(dot_spacing, SCREEN_WIDTH, dot_spacing):
        for y in range(dot_spacing, SCREEN_HEIGHT, dot_spacing):
            # Check if dot would be inside a wall
            dot_rect = pygame.Rect(x - DOT_SIZE//2, y - DOT_SIZE//2, DOT_SIZE, DOT_SIZE)
            collision = False
            for wall in walls:
                if wall.colliderect(dot_rect):
                    collision = True
                    break
            
            if not collision:
                dots.append(Dot(x, y))
    
    return dots

def main():
    # Create game objects
    walls = create_walls()
    dots = create_dots(walls)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Create ghosts with different colors
    ghosts = [
        Ghost(100, 100, (255, 0, 0)),    # Red ghost
        Ghost(700, 100, (255, 192, 203)), # Pink ghost
        Ghost(100, 500, (0, 255, 255)),  # Cyan ghost
        Ghost(700, 500, (255, 165, 0))   # Orange ghost
    ]
    
    score = 0
    game_over = False
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.direction = 0
                elif event.key == pygame.K_DOWN:
                    player.direction = 1
                elif event.key == pygame.K_LEFT:
                    player.direction = 2
                elif event.key == pygame.K_UP:
                    player.direction = 3
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    return main()
        
        if not game_over:
            # Update game objects
            player.update(walls)
            
            # Check for dot collisions
            for dot in dots:
                if dot.check_collision(player):
                    score += 10
            
            # Update ghosts
            for ghost in ghosts:
                ghost.update(player, walls)
                
                # Check for ghost collision
                distance = math.sqrt((player.x - ghost.x) ** 2 + (player.y - ghost.y) ** 2)
                if distance < player.radius + ghost.radius:
                    game_over = True
            
            # Check win condition
            all_dots_collected = True
            for dot in dots:
                if not dot.collected:
                    all_dots_collected = False
                    break
            
            if all_dots_collected:
                game_over = True
        
        # Draw everything
        screen.fill(BG_COLOR)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        
        # Draw dots
        for dot in dots:
            dot.draw()
        
        # Draw player and ghosts
        player.draw()
        for ghost in ghosts:
            ghost.draw()
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if game_over:
            if all_dots_collected:
                message = "You Win! Press R to restart"
            else:
                message = "Game Over! Press R to restart"
            
            game_over_text = font.render(message, True, SCORE_COLOR)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
