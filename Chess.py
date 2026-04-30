# Simple text-based chess (basic version)

def create_board():
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"],
    ]

def print_board(board):
    print("\n  a b c d e f g h")
    for i, row in enumerate(board):
        print(8 - i, " ".join(row), 8 - i)
    print("  a b c d e f g h\n")

def parse_move(move):
    try:
        start, end = move.split()
        col_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        sr, sc = 8 - int(start[1]), col_map[start[0]]
        er, ec = 8 - int(end[1]), col_map[end[0]]
        return sr, sc, er, ec
    except:
        return None

def is_valid_move(board, sr, sc, er, ec, player):
    piece = board[sr][sc]
    target = board[er][ec]

    if piece == ".":
        return False
    if player == "white" and not piece.isupper():
        return False
    if player == "black" and not piece.islower():
        return False
    if target != ".":
        if player == "white" and target.isupper():
            return False
        if player == "black" and target.islower():
            return False

    # VERY basic movement (not full chess rules!)
    dr, dc = er - sr, ec - sc

    # Pawns
    if piece.lower() == "p":
        direction = -1 if piece.isupper() else 1
        if dc == 0 and dr == direction and target == ".":
            return True
        if abs(dc) == 1 and dr == direction and target != ".":
            return True

    # Rook
    if piece.lower() == "r":
        return sr == er or sc == ec

    # Bishop
    if piece.lower() == "b":
        return abs(dr) == abs(dc)

    # Queen
    if piece.lower() == "q":
        return sr == er or sc == ec or abs(dr) == abs(dc)

    # King
    if piece.lower() == "k":
        return abs(dr) <= 1 and abs(dc) <= 1

    # Knight
    if piece.lower() == "n":
        return (abs(dr), abs(dc)) in [(2,1),(1,2)]

    return False

def move_piece(board, sr, sc, er, ec):
    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."

def game():
    board = create_board()
    player = "white"

    while True:
        print_board(board)
        print(f"{player.capitalize()}'s turn (e.g., e2 e4)")

        move = input("Move: ")
        parsed = parse_move(move)

        if not parsed:
            print("Invalid format. Use like: e2 e4")
            continue

        sr, sc, er, ec = parsed

        if not (0 <= sr < 8 and 0 <= sc < 8 and 0 <= er < 8 and 0 <= ec < 8):
            print("Out of bounds!")
            continue

        if not is_valid_move(board, sr, sc, er, ec, player):
            print("Illegal move!")
            continue

        move_piece(board, sr, sc, er, ec)

        # Switch player
        player = "black" if player == "white" else "white"

# Run game
game()

import random

def get_all_valid_moves(board, player):
    moves = []
    for sr in range(8):
        for sc in range(8):
            for er in range(8):
                for ec in range(8):
                    if is_valid_move(board, sr, sc, er, ec, player):
                        moves.append((sr, sc, er, ec))
    return moves

def ai_move(board):
    moves = get_all_valid_moves(board, "black")
    if not moves:
        return None
    return random.choice(moves)

def game():
    board = create_board()
    player = "white"

    while True:
        print_board(board)

        if player == "white":
            print("Your turn (e.g., e2 e4)")
            move = input("Move: ")
            parsed = parse_move(move)

            if not parsed:
                print("Invalid format.")
                continue

            sr, sc, er, ec = parsed

            if not is_valid_move(board, sr, sc, er, ec, player):
                print("Illegal move!")
                continue

        else:
            print("AI is thinking...")
            ai = ai_move(board)

            if ai is None:
                print("AI has no moves. Game over.")
                break

            sr, sc, er, ec = ai
            print(f"AI plays: {chr(sc+97)}{8-sr} {chr(ec+97)}{8-er}")

        move_piece(board, sr, sc, er, ec)

        player = "black" if player == "white" else "white"
