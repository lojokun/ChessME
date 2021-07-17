import pygame as p
import requests
import time
import ChessMain
# import websockets
# import asyncio
# import json

WIDTH = HEIGHT = 512
LOGO = p.image.load("images/ChessME!.png")
LOGO = p.transform.scale(LOGO, (500, 500))
LOGO_X = 5
LOGO_Y = 0


class Button:
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_text(self, screen, font):
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 -
                                                                                       text.get_height() / 2)))

    def draw(self, screen, outline=None):
        if outline:
            p.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        p.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "" and self.text != "Create Account" and self.text != "Add Friend" and self.text != "Challenge":
            font = p.font.SysFont("comicsans", 60)
            self.draw_text(screen, font)
        else:
            font = p.font.SysFont("comicsans", 25)
            self.draw_text(screen, font)

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


quit_button = Button((255, 255, 255), 130, 450, 250, 50, "Quit")
add_friend_button = Button((255, 255, 255), 322, 412, 186, 23, "Add Friend")
challenge_button = Button((255, 255, 255), 12, 412, 186, 23, "Challenge")


def draw_menu(screen, user_input, username, friend_list, challenge_input):
    my_font = p.font.SysFont("comicsans", 25)
    welcome = my_font.render(f"Welcome, {username}!", True, (0, 0, 0))
    friend_add = my_font.render("Enter a username", True, (255, 255, 255))
    challenge_friend = my_font.render("Challenge a friend", True, (255, 255, 255))
    user_input_surface = my_font.render(user_input, True, (0, 0, 0))
    challenge_input_surface = my_font.render(challenge_input, True, (0, 0, 0))
    screen.fill(p.Color("white"))
    screen.blit(LOGO, (LOGO_X, LOGO_Y))
    quit_button.draw(screen, (0, 0, 0))
    add_friend_button.draw(screen, (0, 0, 0))
    challenge_button.draw(screen, (0, 0, 0))
    friend_list_rect = p.Rect(320, 0, 190, 350)
    add_friend_text = p.Rect(320, 360, 190, 25)
    add_friend_write = p.Rect(320, 385, 190, 25)
    challenge_text = p.Rect(10, 360, 190, 25)
    challenge_write = p.Rect(10, 385, 190, 25)
    p.draw.rect(screen, (255, 255, 255), friend_list_rect)
    friend_list_text = my_font.render("Friendlist", True, (0, 0, 0))
    screen.blit(friend_list_text, (375, 0))
    x = 25
    for friend in friend_list:
        friend_text = my_font.render(friend, True, (0, 0, 0))
        screen.blit(friend_text, (320, x))
        x += 25
    p.draw.rect(screen, (0, 0, 0), add_friend_text)
    p.draw.rect(screen, (255, 255, 255), add_friend_write)
    p.draw.rect(screen, (0, 0, 0), challenge_text)
    p.draw.rect(screen, (255, 255, 255), challenge_write)
    screen.blit(welcome, (10, 5))
    screen.blit(friend_add, (320, 360))
    screen.blit(challenge_friend, (10, 360))
    screen.blit(user_input_surface, (add_friend_write.x + 5, add_friend_write.y + 5))
    screen.blit(challenge_input_surface, (challenge_write.x + 5, challenge_write.y + 5))


def add_friend(username, friend, friend_list):
    try:
        response = requests.post("http://127.0.0.1:8000/create-friendship/", data={"friend1": username,
                                                                                   "friend2": friend})
        print(response.content)
        if "User matching query does not exist" not in response.content:
            friend_list.append(friend)
    except:
        print("Username not found")


def send_challenge(challenger, challenged):
    try:
        response = requests.post("http://127.0.0.1:8000/get-challenge/", data={"challenged": challenged,
                                                                               "challenger": challenger})
        print(response)
    except:
        print("Exception")


def get_challenge(user_id):
    try:
        response = requests.post(f"http://127.0.0.1:8000/send-challenge/{user_id}/")
        if response.content != b"":
            print(response)
            print(response.content)
            print(response.json())
    except:
        print("...")
# async def challenge(friend):
#     url = "ws://127.0.0.1:8000/get-challenge/"
#     friend_dict = {"friend": friend}
#     print(friend_dict)
#
#     async with websockets.connect(url) as ws:
#         print("Sending dict")
#         await ws.send(json.dumps(friend_dict))
#         print("Send complete")
#
#
# async def get_challenge():
#     url = "ws://127.0.0.1:8000/send-challenge/"
#
#     async with websockets.connect(url) as ws:
#         response = await ws.recv()
#         print(response)


def main(username, friend_list, user_id):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    friend_text = ""
    challenge_text = ""
    user_write = False
    challenge_write = False

    user_input = p.Rect(320, 385, 190, 25)
    challenge_input = p.Rect(10, 385, 190, 25)
    running = True

    while running:
        for e in p.event.get():
            pos = p.mouse.get_pos()

            if e.type == p.QUIT:
                running = False

            if e.type == p.MOUSEBUTTONDOWN:
                if quit_button.is_over(pos):
                    running = False

                if add_friend_button.is_over(pos):
                    add_friend(username, friend_text, friend_list)
                    pass

                if challenge_button.is_over(pos):
                    # asyncio.get_event_loop().run_until_complete(challenge(challenge_text))
                    send_challenge(username, challenge_text)

                if user_input.collidepoint(pos):
                    user_write = True
                    challenge_write = False

                elif challenge_input.collidepoint(pos):
                    user_write = False
                    challenge_write = True

                else:
                    user_write = False
                    challenge_write = False

            if e.type == p.KEYDOWN:

                if user_write:
                    if e.key == p.K_BACKSPACE:
                        friend_text = friend_text[:-1]
                    else:
                        friend_text += e.unicode

                if challenge_write:
                    if e.key == p.K_BACKSPACE:
                        challenge_text = challenge_text[:-1]
                    else:
                        challenge_text += e.unicode

        draw_menu(screen, friend_text, username, friend_list, challenge_text)
        p.display.update()
        get_challenge(user_id)
        # asyncio.get_event_loop().run_until_complete(get_challenge())


if __name__ == "__main__":
    main("random", ["friend1", "friend2", "friend3"], 0)
