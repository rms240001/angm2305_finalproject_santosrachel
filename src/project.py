import pygame
import sys

# Possible states / scenes
# TODO: add canvas editor state and possibly a "save image" one
STATE_WELCOME = "welcome"
STATE_CONFIG   = "config"
STATE_EDITOR    = "editor"

CANVAS_OPTIONS = {
    pygame.K_1: (20, 20),
    pygame.K_2: (50, 50),
    pygame.K_3: (100, 100),
}

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
    screen.fill((240, 240, 240))
    font = pygame.font.SysFont(None, 48)
    title_text = "Select your canvas size!"
    title_surf = font.render(title_text, True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(screen.get_rect().centerx,
                                             screen.get_rect().centery - 100))
    screen.blit(title_surf, title_rect)

    option_font = pygame.font.SysFont(None, 36)
    options = [
        "1) 20 × 20 pixels",
        "2) 50 × 50 pixels",
        "3) 100 × 100 pixels",
    ]

    # formatting
    spacing_between_title_and_options = 60
    line_spacing = 50

    start_y = title_rect.bottom + spacing_between_title_and_options
    for i, opt in enumerate(options):
        surf = option_font.render(opt, True, (0, 0, 0))
        rect = surf.get_rect(center=(screen.get_rect().centerx,
                    start_y + i * line_spacing))
        screen.blit(surf, rect)

# TODO: rename after more logic has been implemented
def draw_editor_placeholder(screen, canvas_size):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 48)
    # replace later, just to test
    msg = f"Canvas size: {canvas_size[0]} × {canvas_size[1]}"
    surf = font.render(msg, True, (0,0,0))
    rect = surf.get_rect(center=screen.get_rect().center)
    screen.blit(surf, rect)

def main():
    pygame.init()
    pygame.display.set_caption("Pixel Art Grid Editor")

    resolution = (1920, 1080)  # testing resolution, change to 1920x1080 later
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

                elif state == STATE_WELCOME and event.key == pygame.K_RETURN:
                    state = STATE_CONFIG

                elif state == STATE_CONFIG:
                    if event.key in CANVAS_OPTIONS:
                        selected_canvas = CANVAS_OPTIONS[event.key]
                        state = STATE_EDITOR

        # Render screen based on state
        if state == STATE_WELCOME:
            draw_welcome(screen)
        elif state == STATE_CONFIG:
            draw_config(screen)
        elif state == STATE_EDITOR:
            draw_editor_placeholder(screen, selected_canvas)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
