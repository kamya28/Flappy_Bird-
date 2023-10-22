import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 30
GRAVITY = 1
BIRD_JUMP = -15
PIPE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
BIRD_YELLOW = (255, 255, 102)
GROUND_BROWN = (139, 69, 19)

# Bird properties
bird_pos = [50, HEIGHT // 2]
bird_velocity = 0
bird_size = 20

# Pipe properties
pipe_width = 50
pipe_gap = 150
pipe_distance = 200
pipes = []

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


def draw_bird(pos):
    pygame.draw.circle(screen, BIRD_YELLOW, pos, bird_size)


def draw_pipe(pipe):
    pygame.draw.rect(screen, GREEN, pipe)


def draw_ground():
    pygame.draw.rect(screen, GROUND_BROWN, (0, HEIGHT - 20, WIDTH, 20))


def draw_splash_screen():
    font = pygame.font.Font(None, 36)
    text1 = font.render("Flappy Bird", True, WHITE)
    text2 = font.render("Press SPACE to start", True, WHITE)
    screen.blit(text1, (WIDTH // 4, HEIGHT // 3))
    screen.blit(text2, (WIDTH // 5, HEIGHT // 2))


def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


def main():
    global bird_pos, bird_velocity, pipes

    splash_screen = True
    game_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if splash_screen:
                    splash_screen = False
                    game_active = True
                elif game_active:
                    bird_velocity = BIRD_JUMP

        if splash_screen:
            screen.fill(SKY_BLUE)
            draw_splash_screen()
        elif game_active:
            # Update bird position
            bird_velocity += GRAVITY
            bird_pos[1] += bird_velocity

            # Generate pipes
            if len(pipes) == 0 or pipes[-1][0] < WIDTH - pipe_distance:
                pipe_height = random.randint(50, HEIGHT - 50 - pipe_gap)
                pipes.append([WIDTH, HEIGHT - pipe_height, pipe_width, pipe_height])

            # Update pipes and check collisions
            for pipe in pipes:
                pipe[0] -= PIPE_SPEED

                pipe_rect = pygame.Rect(pipe[0], pipe[1], pipe[2], pipe[3])

                if (
                    pipe_rect.colliderect(
                        (bird_pos[0], bird_pos[1], bird_size, bird_size)
                    )
                    or bird_pos[1] + bird_size > HEIGHT - 20
                ):
                    game_over()

                if pipe[0] + pipe[2] < 0:
                    pipes.remove(pipe)

            # Draw everything
            screen.fill(SKY_BLUE)
            draw_bird(bird_pos)
            for pipe in pipes:
                draw_pipe(pipe)
            draw_ground()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
