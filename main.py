import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 40
PLAYER_SPEED = 5
ENEMY_SPEED = 2
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
SPAWN_INTERVAL = 2000  # milliseconds

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivor")
clock = pygame.time.Clock()

# Player setup
def create_player():
    rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
    return rect

player = create_player()

# Enemy list
enemies = []

def spawn_enemy():
    x = random.choice([0, WIDTH - ENEMY_SIZE])
    y = random.randint(0, HEIGHT - ENEMY_SIZE)
    enemy_rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
    enemies.append(enemy_rect)

pygame.time.set_timer(SPAWN_ENEMY_EVENT, SPAWN_INTERVAL)

font = pygame.font.SysFont(None, 36)
start_ticks = pygame.time.get_ticks()

def move_player(keys, player_rect):
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += PLAYER_SPEED


def move_enemies(player_rect):
    for enemy in enemies:
        if enemy.x < player_rect.x:
            enemy.x += ENEMY_SPEED
        elif enemy.x > player_rect.x:
            enemy.x -= ENEMY_SPEED
        if enemy.y < player_rect.y:
            enemy.y += ENEMY_SPEED
        elif enemy.y > player_rect.y:
            enemy.y -= ENEMY_SPEED


def check_collisions(player_rect):
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            return True
    return False


running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_ENEMY_EVENT:
            spawn_enemy()

    keys = pygame.key.get_pressed()
    move_player(keys, player)
    move_enemies(player)

    if check_collisions(player):
        running = False

    screen.fill((30, 30, 30))

    for enemy in enemies:
        pygame.draw.rect(screen, (200, 0, 0), enemy)

    pygame.draw.rect(screen, (0, 200, 0), player)

    survived_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_surface = font.render(f"Time: {survived_seconds:.1f}s", True, (255, 255, 255))
    screen.blit(timer_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
print(f"You survived {survived_seconds:.1f} seconds!")
