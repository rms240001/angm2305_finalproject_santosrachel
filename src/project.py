import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption("Pixel Art Grid Editor")

    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)

    running = True
    while running:
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    running = False

        # --- Drawing code ---
        screen.fill((255, 255, 255))

        font = pygame.font.SysFont(None, 72)
        text_surface = font.render("Welcome to Pixel Art Editor!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=screen.get_rect().center)
        screen.blit(text_surface, text_rect)

        small_font = pygame.font.SysFont(None, 36)
        prompt_surface = small_font.render("Press ENTER to continue...", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(resolution[0] // 2, resolution[1] // 2 + 100))

        screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
