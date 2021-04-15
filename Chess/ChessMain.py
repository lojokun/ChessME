"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState
Object
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512  # or 400
DIMENSION = 8  # Chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animations
IMAGES = {}

'''
    Initialize a global dictionary of images. This will be called once in the main
'''


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying 'Images['wp']'


'''
The main driver of our code. This will handle user input and updating the graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    # print(gs.board)
    valid_moves = gs.valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    running = True
    piece_at_loc = None
    sq_selected = ()  # no square is selected, keeps track of the last click of user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            # print(e.type)
            if e.type == p.QUIT:
                running = False
            # Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                # mouse_x, mouse_y = get_location(p)
                row, col = get_location_squared(p)
                if sq_selected == (row, col):  # the user clicked the same square
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    # print(move.get_chess_notation())
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            sq_selected = ()  # reset user clicks
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]
                if e.button == 1:
                    initial_pos = (row, col)
                    piece_at_loc = gs.board[row][col]
                    if piece_at_loc == "--":
                        piece_at_loc = None
                    # print(f"initial pos = {initial_pos}")
            elif e.type == p.MOUSEBUTTONUP:
                if e.button == 1:
                    piece_at_loc = None
                    row, col = get_location_squared(p)
                    final_pos = (row, col)
                    move = ChessEngine.Move(initial_pos, final_pos, gs.board)
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()  # reset user clicks
                        player_clicks = []
                    # print(f"final pos = {final_pos}")
            # Key Handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
        if move_made:
            # animate_move(gs.moveLog[-1], screen, gs.board, clock)
            valid_moves = gs.valid_moves()
            move_made = False
        if gs.checkMate:
            print("Checkmate!")
            running = False
        if gs.staleMate:
            print("Stalemate!")
            running = False

        draw_game_state(screen, gs, valid_moves, sq_selected, piece_at_loc)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Highlight square selected and moves for piece selected
'''


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent, 255 solid
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves for the selected piece
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, ((SQ_SIZE * move.end_col), (SQ_SIZE * move.end_row)))


'''
Responsible for all the graphics within a current game state
'''


def draw_game_state(screen, gs, valid_moves, sq_selected, piece_at_loc=None):
    draw_board(screen)  # draw squares on the board
    highlight_squares(screen, gs, valid_moves, sq_selected)
    loc = get_location(p)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares
    if piece_at_loc is not None:
        draw_piece_at(screen, piece_at_loc, loc)


"""
Gets the specific location in a tuple
"""


def get_location(pg):
    location = pg.mouse.get_pos()
    return location


"""
Gets the square location in a tuple
"""


def get_location_squared(pg):
    location = get_location(pg)
    col = location[0] // SQ_SIZE
    row = location[1] // SQ_SIZE
    return row, col


'''
Draw squares on board
'''


def draw_board(screen):
    # global colors
    colors = [p.Color("#eeeed2"), p.Color("#769656")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw pieces on board using the current GameState.board
'''


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draws the piece at the current mouse position
'''


def draw_piece_at(screen, piece, location):
    screen.blit(IMAGES[piece], p.Rect(location[0] - SQ_SIZE // 2, location[1] - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE))


'''
Animating a move
'''

# def animate_move(move, screen, board, clock):
#     global colors
#     dr = move.end_row - move.start_row
#     dc = move.end_col - move.start_col
#     frames_per_sq = 10
#     frame_count = (abs(dr) + abs(dc)) * frames_per_sq
#     for frame in range(frame_count + 1):
#         row, col = (move.start_row + dr*frame/frame_count, move.start_col + dc*frame/frame_count)
#         draw_board(screen)
#         draw_pieces(screen, board)
#         # erase the piece moved from it's ending square
#         color = colors[(move.end_row + move.end_col) % 2]
#         end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
#         p.draw.rect(screen, color, end_square)
#         # draw captured piece onto rectangle
#         if move.pieceCaptured != '--':
#             screen.blit(IMAGES[move.pieceMoved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
#             p.display.flip()
#             clock.tick(60)


if __name__ == "__main__":
    main()
