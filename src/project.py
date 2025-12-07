import pygame
import sys

# Possible states / scenes
# TODO: add canvas editor state and possibly a "save image" one
STATE_WELCOME = "welcome"
STATE_CONFIG   = "config"

def draw_welcome(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 72)
    title_surf = font.render("Welcome to Pixel Art Editor!", True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=screen.get_rect().center)
    screen.blit(title_surf, title_rect)

    small_font = pygame.font.SysFont(None, 36)
    prompt_surf = small_font.render("Press ENTER to continue...", True, (0, 0, 0))

    prompt_rect = prompt_surf.get_rect(
        center=(screen.get_rect().centerx,
                screen.get_rect().centery + 100)
    )
    screen.blit(prompt_surf, prompt_rect)

def draw_config(screen):
    screen.fill((220, 220, 220))
    font = pygame.font.SysFont(None, 48)
    text_surf = font.render("Canvas-size selection screen (work in progress)", True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=screen.get_rect().center)
    screen.blit(text_surf, text_rect)

def main():
    pygame.init()
    pygame.display.set_caption("Pixel Art Grid Editor")

    resolution = (800, 600)  # testing resolution, change to 1920x1080 later
    screen = pygame.display.set_mode(resolution)

    state = STATE_WELCOME

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if state == STATE_WELCOME:
                        state = STATE_CONFIG

        # Render screen based on state
        if state == STATE_WELCOME:
            draw_welcome(screen)
        elif state == STATE_CONFIG:
            draw_config(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
