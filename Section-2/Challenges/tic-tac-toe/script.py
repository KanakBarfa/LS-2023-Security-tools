import subprocess
from pwn import *
import random
def play_tic_tac_toe():
    password = ""
    game=1
    # Start the ttt program for each game
    p = process('./ttt')
    p.recvline()
    p.recvline()
    while game<=250:
        #print(f"Playing game [{game}/250]...")
        while True:
            output = ['','','','']
            s=p.recvline().decode()
            #print(s)
            
            if '250' in s:
                output[0]=list(p.recvline().decode()[0:5].split(' '))
            elif "You won" in s:
                print(p.recvline().decode())
                game=1000
                break
            else:
                output[0]=list(s[0:5].split(' '))
            output[1]=list(p.recvline().decode()[0:5].split(' '))
            output[2]=list(p.recvline().decode()[0:5].split(' '))
            output[3]=p.recvline().decode()
            # print(output)
            if "Enter the block" in output[3]:
                move = generate_move(output[0:3])
                if move is None:
                    break
                p.sendline(f"{move[0]},{move[1]}".encode())
            elif "Illegal move" in output[3] or "You lost" in output[3]:
                break
            elif "You won" in output[3]:
                print(p.recvline())
                print(p.recvline())
                break
            else:
                break
        game += 1
def generate_move(board):
    best_score = float('-inf')
    best_move = None
    if all(cell == '_' for row in board for cell in row):
        return (0, 0)
    # Iterate over each row and column of the board
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == '_':
                # Empty cell found, make a move and evaluate its score using Minimax
                board[row_idx][col_idx] = 'o'
                score = minimax(board, 0, False)
                board[row_idx][col_idx] = '_'  # Reset the cell

                if score > best_score:
                    best_score = score
                    best_move = (row_idx, col_idx)
    return best_move


def minimax(board, depth, is_maximizing):
    scores = {
        'o': 1,  # 'o' wins
        'x': -1,  # 'x' wins
        'draw': 0  # Draw
    }

    result = check_game_result(board)
    if result is not None:
        return scores[result]

    if is_maximizing:
        best_score = float('-inf')
        for row_idx, row in enumerate(board):
            for col_idx, cell in enumerate(row):
                if cell == '_':
                    board[row_idx][col_idx] = 'o'
                    score = minimax(board, depth + 1, False)
                    board[row_idx][col_idx] = '_'  # Reset the cell
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = float('inf')
        for row_idx, row in enumerate(board):
            for col_idx, cell in enumerate(row):
                if cell == '_':
                    board[row_idx][col_idx] = 'x'
                    score = minimax(board, depth + 1, True)
                    board[row_idx][col_idx] = '_'  # Reset the cell
                    best_score = min(score, best_score)
        return best_score


def check_game_result(board):
    # Check rows
    for row in board:
        if all(cell == 'o' for cell in row):
            return 'o'
        if all(cell == 'x' for cell in row):
            return 'x'

    # Check columns
    for col in range(3):
        if all(board[row][col] == 'o' for row in range(3)):
            return 'o'
        if all(board[row][col] == 'x' for row in range(3)):
            return 'x'

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == 'o':
        return 'o'
    if board[0][0] == board[1][1] == board[2][2] == 'x':
        return 'x'
    if board[0][2] == board[1][1] == board[2][0] == 'o':
        return 'o'
    if board[0][2] == board[1][1] == board[2][0] == 'x':
        return 'x'

    # Check for a draw
    if all(all(cell != '_' for cell in row) for row in board):
        return 'draw'

    return None


play_tic_tac_toe()
