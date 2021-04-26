import pygame as p

import MainMenu

WIDTH = HEIGHT = 512
LOGO = p.image.load("images/ChessME!.png")
LOGO = p.transform.scale(LOGO, (500, 500))
LOGO_X = 5
LOGO_Y = 0

LOGIN_BUTTON = MainMenu.Button((255, 255, 255), 170, 385, 180, 50, "Login")


def draw_menu(screen, user_input, pass_input, user_input_rect, pass_input_rect):
    screen.fill(p.Color("white"))
    screen.blit(LOGO, (LOGO_X, LOGO_Y))
    input_rect_color = p.Color("lightskyblue2")
    text_rect_color = p.Color("white")
    user_text_rect = p.Rect(170, 243, 180, 32)
    pass_text_rect = p.Rect(170, 313, 180, 32)
    p.draw.rect(screen, input_rect_color, user_input_rect)
    p.draw.rect(screen, input_rect_color, pass_input_rect)
    p.draw.rect(screen, text_rect_color, user_text_rect)
    p.draw.rect(screen, text_rect_color, pass_text_rect)
    base_font = p.font.Font(None, 25)
    text_font = p.font.Font(None, 25)
    user_input_surface = base_font.render(user_input, True, (0, 0, 0))
    pass_input_surface = base_font.render(pass_input, True, (0, 0, 0))
    user_text_surface = text_font.render("Enter username", True, (0, 0, 0))
    pass_text_surface = text_font.render("Enter password", True, (0, 0, 0))
    screen.blit(user_text_surface, (user_text_rect.x + 5, user_text_rect.y + 5))
    screen.blit(pass_text_surface, (pass_text_rect.x + 5, pass_text_rect.y + 5))
    screen.blit(user_input_surface, (user_input_rect.x + 5, user_input_rect.y + 5))
    screen.blit(pass_input_surface, (pass_input_rect.x + 5, pass_input_rect.y + 5))
    LOGIN_BUTTON.draw(screen, (0, 0, 0))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    user_text = ""
    pass_text = ""
    pass_shown = ""
    user_write = False
    pass_write = False
    user_input_rect = p.Rect(170, 275, 180, 32)
    pass_input_rect = p.Rect(170, 345, 180, 32)
    running = True

    while running:
        for e in p.event.get():
            pos = p.mouse.get_pos()

            if e.type == p.QUIT:
                running = False
                print(pass_text)

            if e.type == p.MOUSEBUTTONDOWN:
                if LOGIN_BUTTON.is_over(pos):
                    try:
                        MainMenu.main()
                    except:
                        MainMenu.main()
                if user_input_rect.collidepoint(pos):
                    user_write = True
                    pass_write = False
                elif pass_input_rect.collidepoint(pos):
                    pass_write = True
                    user_write = False
                else:
                    user_write = False
                    pass_write = False

            if e.type == p.KEYDOWN:
                if user_write:
                    if e.key == p.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += e.unicode
                if pass_write:
                    if e.key == p.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                        pass_shown = pass_shown[:-1]
                    else:
                        pass_text += e.unicode
                        pass_shown += "*"
                        if e.key == p.K_LSHIFT:
                            pass_shown = pass_shown[:-1]

        draw_menu(screen, user_text, pass_shown, user_input_rect, pass_input_rect)
        p.display.update()


if __name__ == "__main__":
    main()
