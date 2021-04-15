"""
This class is responsible for storing all the information about the current state of a chess game. Also responsible
for determining the valid moves at the current state. It also keeps a moves log.
"""


class GameState:
    def __init__(self):
        # board is an 8x8 2D list, each element of the list has 2 characters.
        # The first character is the color 'b' or 'w'
        # The second character is the type 'K', 'Q', 'R', 'B', 'N', or 'p'
        # The string "--" is an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.pawn_moves, 'R': self.rook_moves, 'N': self.knight_moves,
                              'B': self.bishop_moves, 'Q': self.queen_moves, 'K': self.king_moves}
        self.whiteToMove = True  # keeps track of who's turn is it
        self.moveLog = []  # keeps track of all moves
        self.whiteKingLocation = (7, 4)  # keeps track of the white kings location
        self.blackKingLocation = (0, 4)  # keeps track of the black kings location
        self.checkMate = False  # Checks fork checkmate
        self.staleMate = False  # Checks for stalemate
        self.enpassantPossible = ()  # Coordinates for the enpassant
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    def make_move(self, move):
        """
        Takes a Move as a parameter and executes it (not work for castling, and en-passant, or promotion
        :param move: object
        :return: None
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update kings location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.end_row, move.end_col)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.end_row, move.end_col)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.end_row][move.end_col] = move.pieceMoved[0] + 'Q'

        # en passant
        if move.isEnpassantMove:
            self.board[move.start_row][move.end_col] = '--'  # capturing the pawn

        # update enpassantPossible
        if move.pieceMoved[1] == 'p' and abs(move.start_row - move.end_row) == 2:  # Only on 2 square pawn advance
            self.enpassantPossible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassantPossible = False

        # castle move
        if move.isCastleMove:
            if move.end_col - move.start_col == 2:  # kingside castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]  # moves rook
                self.board[move.end_row][move.end_col + 1] = "--"  # erase old rook
            else:  # queenside castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"  # erase old rook

        # update castling rights - whenever it is a rook or a king move
        self.update_castle_rights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                 self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    def undo_move(self):
        """
        Takes a Move as a parameter and goes back to the previous position
        :return: None
        """
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.pieceMoved
            self.board[move.end_row][move.end_col] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # updates kings location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.start_row, move.start_col)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.start_row, move.start_col)
            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.end_row][move.end_col] = '--'  # leave landing square blank
                self.board[move.start_row][move.end_col] = move.pieceCaptured
                self.enpassantPossible = (move.end_row, move.end_col)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpassantPossible = ()
            # undo castle move
            if move.isCastleMove:
                if move.end_col - move.start_col == 2:  # kingside
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # queenside
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
            # undo castling rights
            self.castleRightsLog.pop()  # get rid of the castle rights from the move we are undoing
            self.currentCastlingRights = self.castleRightsLog[-1]  # set the current castle rights to the last move

    def update_castle_rights(self, move):
        """
        Updates the castle rights
        :param move: obj
        :return: None
        """
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:  # left rook
                    self.currentCastlingRights.wqs = False
                elif move.start_col == 7:  # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:  # left rook
                    self.currentCastlingRights.bqs = False
                elif move.start_col == 7:  # right rook
                    self.currentCastlingRights.bks = False

    def valid_moves(self):
        temp_enpassant_possible = self.enpassantPossible
        temp_castle_rights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                          self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        # 1) Generate all possible moves
        moves = self.possible_moves()
        if self.whiteToMove:
            self.get_castle_moves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.get_castle_moves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2) For each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            # 3) Generate all opponent's moves
            # 4) For each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.in_check():
                moves.remove(moves[i])  # 5) If they do attack your king, move not valid
            self.whiteToMove = not self.whiteToMove
            self.undo_move()
        if len(moves) == 0:  # either checkmate or stalemate
            if self.in_check():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = temp_enpassant_possible
        self.currentCastlingRights = temp_castle_rights
        return moves

    def in_check(self):
        """
        Determine if the current player is in check
        :return: bool
        """
        if self.whiteToMove:
            return self.square_under_attack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.square_under_attack(self.blackKingLocation[0], self.blackKingLocation[1])

    def square_under_attack(self, r, c):
        """
        Determines if the square (r, c) is under attack
        :param r: int
        :param c: int
        :return: bool
        """
        self.whiteToMove = not self.whiteToMove  # switch to the opponent's turn
        opp_moves = self.possible_moves()
        self.whiteToMove = not self.whiteToMove
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:  # square is under attack
                return True
        return False

    def possible_moves(self):
        """
        Checks all possible move
        :return: list
        """
        moves = []
        for r in range(len(self.board)):  # nr of rows
            for c in range(len(self.board[r])):  # nr of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function for every piece
        return moves

    def pawn_moves(self, row, col, moves):
        """
        Gets all the pawn moves for the pawn located at (row, col) and adds these moves to the list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        if self.whiteToMove:  # white pawn moves
            if self.board[row - 1][col] == "--":  # 1 square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:  # captures
                if 'b' in self.board[row - 1][col - 1]:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_en_passant_move=True))
            if col + 1 <= 7:
                if 'b' in self.board[row - 1][col + 1]:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_en_passant_move=True))

        else:  # black pawn moves
            if self.board[row + 1][col] == "--":  # 1 square pawn advance
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:  # captures
                if 'w' in self.board[row + 1][col - 1]:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_en_passant_move=True))
            if col + 1 <= 7:
                if 'w' in self.board[row + 1][col + 1]:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_en_passant_move=True))

    def rook_moves(self, row, col, moves):
        """
        Gets all the moves for a rook located at (row, col) and adds these moves to the list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # a rooks directions are up, left, down and right
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif enemy_color in end_piece:  # enemy piece interaction
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off the board
                    break

    def knight_moves(self, row, col, moves):
        """
        Gets all valid moves for a knight situated at (row, col) and adds them to moves list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        # Directions for the knight, L shaped
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0]
                end_col = col + d[1]
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif enemy_color in end_piece:  # enemy piece interaction
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off the board
                    break

    def bishop_moves(self, row, col, moves):
        """
        Gets all valid moves for a bishop located at (row, col) and adds them to moves list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # a bishop goes diagonally
        # up left, up right, down left, down right
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif enemy_color in end_piece:  # enemy piece interaction
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:  # off the board
                    break

    def queen_moves(self, row, col, moves):
        """
        Gets all the possible queen moves located at (row, col) and adds them to the moves list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        self.rook_moves(row, col, moves)
        self.bishop_moves(row, col, moves)

    def king_moves(self, row, col, moves):
        """
        All valid moves for a king situated at (row, col), adds them in a moves list
        :param row: int
        :param col: int
        :param moves: object
        :return: None
        """
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if ally_color not in end_piece:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_castle_moves(self, row, col, moves):
        """
        Generates all valid castle moves for king at (row, col)
        :param row: int
        :param col: int
        :param moves: obj
        :return: obj
        """
        if self.square_under_attack(row, col):
            return  # can't castle while in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or \
                (not self.whiteToMove and self.currentCastlingRights.bks):
            self.get_ks_castle_moves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or \
                (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.get_qs_castle_moves(row, col, moves)

    def get_ks_castle_moves(self, row, col, moves):
        if self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--":
            if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))

    def get_qs_castle_moves(self, row, col, moves):
        if self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" and self.board[row][col - 3] == "--":
            if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))


"""
This class is responsible for handling the castle movement
"""


class CastleRights:

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


"""
This class is responsible for storing moves, its' starting position and its' ending position, and also if a piece is 
captured
"""


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start_sq, end_sq, board, is_en_passant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.pieceMoved = board[self.start_row][self.start_col]
        self.pieceCaptured = board[self.end_row][self.end_col]
        # Pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.end_row == 0) or (self.pieceMoved == "bp" and self.end_row == 7):
            self.isPawnPromotion = True
        # En passant
        self.isEnpassantMove = is_en_passant_move
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # castle move
        self.isCastleMove = is_castle_move
        # print(self.moveID)  # Prints valid moves

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
