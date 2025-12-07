import pygame
import sys

# States
STATE_WELCOME = "welcome"
STATE_CONFIG  = "config"
STATE_EDITOR  = "editor"

CANVAS_OPTIONS = {
    pygame.K_1: (20, 20),
    pygame.K_2: (50, 50),
    pygame.K_3: (100, 100),
}

UI_PANEL_WIDTH = 200
CELL_SIZE = 16 # TODO: this may need to change soon?

def draw_welcome(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 72)
    title = font.render("Welcome to Pixel Art Editor!", True, (0, 0, 0))
    title_rect = title.get_rect(center=screen.get_rect().center)
    screen.blit(title, title_rect)

    small_font = pygame.font.SysFont(None, 36)
    prompt = small_font.render("Press ENTER to continue...", True, (0, 0, 0))
    prompt_rect = prompt.get_rect(
        center=(screen.get_rect().centerx,
                screen.get_rect().centery + 100)
    )
    screen.blit(prompt, prompt_rect)

def draw_config(screen):
    screen.fill((240, 240, 240))
    font = pygame.font.SysFont(None, 48)
    title = font.render("Select canvas size:", True, (0, 0, 0))
    screen_center = screen.get_rect().center
    title_rect = title.get_rect(center=(screen_center[0], screen_center[1] - 60))
    screen.blit(title, title_rect)

    options = ["1) 20 × 20", "2) 50 × 50", "3) 100 × 100"]
    opt_font = pygame.font.SysFont(None, 36)
    for i, text in enumerate(options):
        surf = opt_font.render(text, True, (0, 0, 0))
        rect = surf.get_rect(center=(screen_center[0], screen_center[1] + i * 50))
        screen.blit(surf, rect)

def draw_editor(screen, canvas_size, grid_data, current_color):
    screen.fill((200, 200, 200))  # background for UI + canvas

    screen_w, screen_h = screen.get_size()

    # --- Draw UI panel (left) ---
    ui_rect = pygame.Rect(0, 0, UI_PANEL_WIDTH, screen_h)
    pygame.draw.rect(screen, (180, 180, 180), ui_rect)

    ui_font = pygame.font.SysFont(None, 24)
    ui_text = ui_font.render("UI Panel (colors/tools)", True, (0, 0, 0))
    screen.blit(ui_text, (10, 10))

    pygame.draw.rect(screen, current_color, (10, 40, 50, 50))

    # --- Draw canvas area (right) ---
    canvas_origin_x = UI_PANEL_WIDTH
    cols, rows = canvas_size

    for row in range(rows):
        for col in range(cols):
            x = canvas_origin_x + col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, (255, 255, 255), rect)

            color = grid_data[row][col]
            if color:
                pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

def main():
    pygame.init()
    pygame.display.set_caption("Pixel Art Grid Editor")

    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)

    state = STATE_WELCOME
    selected_canvas = None
    grid_data = None
    current_color = (0, 0, 0)  # default paint color: black

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
                elif state == STATE_CONFIG and event.key in CANVAS_OPTIONS:
                    selected_canvas = CANVAS_OPTIONS[event.key]
                    cols, rows = selected_canvas
                    grid_data = [[None for _ in range(cols)] for _ in range(rows)]
                    state = STATE_EDITOR

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == STATE_EDITOR and selected_canvas:
                    mx, my = event.pos
                    # if click in canvas area
                    if mx >= UI_PANEL_WIDTH:
                        col = (mx - UI_PANEL_WIDTH) // CELL_SIZE
                        row = my // CELL_SIZE
                        if 0 <= col < selected_canvas[0] and 0 <= row < selected_canvas[1]:
                            # set the pixel to current color
                            grid_data[row][col] = current_color

        # ---- Drawing ----
        if state == STATE_WELCOME:
            draw_welcome(screen)
        elif state == STATE_CONFIG:
            draw_config(screen)
        elif state == STATE_EDITOR and selected_canvas:
            draw_editor(screen, selected_canvas, grid_data, current_color)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
