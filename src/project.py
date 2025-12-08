import pygame
import sys
from pathlib import Path

# States
STATE_WELCOME = "welcome"
STATE_CONFIG  = "config"
STATE_EDITOR  = "editor"

CANVAS_OPTIONS = {
    pygame.K_1: (30, 30),
    pygame.K_2: (50, 50),
    pygame.K_3: (80, 50),
}

UI_PANEL_WIDTH = 200
CELL_SIZE = 16

PALETTE = [
    (0,   0,   0),      # black
    (255,   0,   0),    # red
    (255, 165,   0),    # orange
    (255, 255,   0),    # yellow
    (0,   255,   0),    # green
    (0,   255, 255),    # cyan / light-blue
    (0,     0, 255),    # blue
    (128,   0, 128),    # purple
    (255, 192, 203),    # pink
    (128, 128, 128),    # gray
]

TOOL_COLOR = "color"
TOOL_ERASER = "eraser"

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

    options = ["1) 30 × 30", "2) 50 × 50", "3) 80 × 50"]
    opt_font = pygame.font.SysFont(None, 36)
    for i, text in enumerate(options):
        surf = opt_font.render(text, True, (0, 0, 0))
        rect = surf.get_rect(center=(screen_center[0], screen_center[1] + i * 50))
        screen.blit(surf, rect)

def draw_editor(screen, canvas_size, grid_data, current_tool, current_color, palette):
    screen.fill((200, 200, 200))

    screen_w, screen_h = screen.get_size()

    # --- Draw UI panel (left) ---
    ui_rect = pygame.Rect(0, 0, UI_PANEL_WIDTH, screen_h)
    pygame.draw.rect(screen, (180, 180, 180), ui_rect)

    ui_font = pygame.font.SysFont(None, 24)
    screen.blit(ui_font.render("Palette", True, (0, 0, 0)), (10, 10))

    swatch_size = 30
    swatch_padding = 10
    start_y = 40

    # Color Swatches
    for i, col in enumerate(palette):
        y = start_y + i * (swatch_size + swatch_padding)
        sw_rect = pygame.Rect(10, y, swatch_size, swatch_size)
        pygame.draw.rect(screen, col, sw_rect)
        if current_tool == TOOL_COLOR and col == current_color:
            pygame.draw.rect(screen, (255, 255, 255), sw_rect, 3)
        else:
            pygame.draw.rect(screen, (0, 0, 0), sw_rect, 1)

    # Eraser Swatch
    eraser_y = start_y + len(palette) * (swatch_size + swatch_padding) + 20
    eraser_rect = pygame.Rect(10, eraser_y, swatch_size, swatch_size)
    pygame.draw.rect(screen, (220, 220, 220), eraser_rect)
    pygame.draw.rect(screen, (0, 0, 0), eraser_rect, 1)
    label = ui_font.render("Eraser", True, (0, 0, 0))
    label_rect = label.get_rect(midbottom=(eraser_rect.centerx, eraser_rect.top - 4))
    screen.blit(label, label_rect)
    if current_tool == TOOL_ERASER:
        pygame.draw.rect(screen, (255, 0, 0), eraser_rect, 3)

    # Clear Canvas button
    clear_btn_y = eraser_y + swatch_size + 20
    clear_btn_rect = pygame.Rect(10, clear_btn_y, UI_PANEL_WIDTH - 20, 30)
    pygame.draw.rect(screen, (200, 100, 100), clear_btn_rect)  # red-ish
    clear_label = ui_font.render("Clear Canvas", True, (0, 0, 0))
    screen.blit(clear_label, clear_label.get_rect(center=clear_btn_rect.center))

    # Save Image button
    save_btn_y = clear_btn_y + 40
    save_btn_rect = pygame.Rect(10, save_btn_y, UI_PANEL_WIDTH - 20, 30)
    pygame.draw.rect(screen, (100, 200, 100), save_btn_rect)  # greenish
    btn_label = ui_font.render("Save as PNG", True, (0, 0, 0))
    screen.blit(btn_label, btn_label.get_rect(center=save_btn_rect.center))

    # --- Draw Canvas panel (right) ---
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

    return clear_btn_rect, save_btn_rect

def prompt_filename(screen):
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    input_str = ""
    prompt = "Enter file name (no extension): "
    clock = pygame.time.Clock()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key == pygame.K_RETURN:
                    return input_str.strip()
                elif ev.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                else:
                    if ev.unicode.isprintable():
                        input_str += ev.unicode

        screen.fill((50, 50, 50))
        prompt_surf = font.render(prompt + input_str, True, (255, 255, 255))
        screen.blit(prompt_surf, (50, screen.get_height() // 2))
        pygame.display.flip()
        clock.tick(30)

def get_downloads_folder():
    home = Path.home()
    dl = home / "Downloads"
    return dl

def main():
    pygame.init()
    pygame.display.set_caption("Pixel Art Grid Editor")

    resolution_flags = pygame.FULLSCREEN

    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution, resolution_flags)

    state = STATE_WELCOME
    selected_canvas = None
    grid_data = None
    current_tool = TOOL_COLOR
    current_color = PALETTE[0]
    clear_button_rect = None
    save_button_rect = None

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
                mx, my = event.pos

                if state == STATE_EDITOR and selected_canvas:
                    # Clear Logic
                    if clear_button_rect and clear_button_rect.collidepoint(mx, my):
                        cols, rows = selected_canvas
                        grid_data = [[None for _ in range(cols)] for _ in range(rows)]
                        continue

                    # Save Button Logic
                    if save_button_rect and save_button_rect.collidepoint(mx, my):
                        fname = prompt_filename(screen)
                        if fname:
                            dl = get_downloads_folder()
                            out_path = dl / f"{fname}.png"
                            try:
                                dl.mkdir(parents=True, exist_ok=True)
                            except Exception as e:
                                print("Could not create Downloads folder:", e)

                            cols, rows = selected_canvas
                            surf = pygame.Surface((cols * CELL_SIZE, rows * CELL_SIZE))
                            for r in range(rows):
                                for c in range(cols):
                                    rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE,
                                                       CELL_SIZE, CELL_SIZE)
                                    pygame.draw.rect(surf, (255,255,255), rect)
                                    col = grid_data[r][c]
                                    if col:
                                        pygame.draw.rect(surf, col, rect)
                                    pygame.draw.rect(surf, (200,200,200), rect, 1)
                            try:
                                pygame.image.save(surf, str(out_path))
                                print("Saved canvas to:", out_path)
                            except Exception as e:
                                print("Error saving file:", e)
                        continue

                    # existing palette / eraser / canvas logic ...
                    swatch_size = 30
                    swatch_padding = 10
                    for i, col in enumerate(PALETTE):
                        x = 10
                        y = 40 + i * (swatch_size + swatch_padding)
                        if pygame.Rect(x, y, swatch_size, swatch_size).collidepoint(mx, my):
                            current_tool = TOOL_COLOR
                            current_color = col
                            break
                    else:
                        eraser_y = 40 + len(PALETTE)*(swatch_size + swatch_padding) + 20
                        eraser_rect = pygame.Rect(10, eraser_y, swatch_size, swatch_size)
                        if eraser_rect.collidepoint(mx, my):
                            current_tool = TOOL_ERASER
                        else:
                            if mx >= UI_PANEL_WIDTH:
                                col_i = (mx - UI_PANEL_WIDTH) // CELL_SIZE
                                row_i = my // CELL_SIZE
                                if (0 <= col_i < selected_canvas[0]
                                    and 0 <= row_i < selected_canvas[1]):
                                    if current_tool == TOOL_COLOR:
                                        grid_data[row_i][col_i] = current_color
                                    elif current_tool == TOOL_ERASER:
                                        grid_data[row_i][col_i] = None

        # Drawing
        if state == STATE_WELCOME:
            draw_welcome(screen)
        elif state == STATE_CONFIG:
            draw_config(screen)
        elif state == STATE_EDITOR and selected_canvas:
            clear_button_rect, save_button_rect = draw_editor(
                screen, selected_canvas, grid_data,
                current_tool, current_color, PALETTE
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
