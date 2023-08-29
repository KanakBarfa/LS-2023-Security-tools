# flag{wh04m1_15_pr0ud_0f_y0u}

from pwn import *
import random
import subprocess


def play():
    p=process('./minesweeper')
    game=1
    p.recvline()
    while game<=25:
        while(True):
            output=['','','','','','','','','','']
            s=p.recvline().decode()
            # print(s)
            if '25' in s:
                output[0]=list(p.recvline().decode()[0:17].split(' '))
                game+=1
            elif "You won" in s:
                print(p.recvline().decode())
                game=26
                break
            else:
                output[0]=list(s[0:17].split(' '))
            for i in range(8):
                s=p.recvline().decode()
                output[i+1]=list(s[0:17].split(' '))
                # print(s)
            output[9]=p.recvline().decode()
            # print(output[9])
            if "You lost" in output[9]:
                p.terminate()
                # print("Oops!, seems like an impossible situation was given, and luck wasn't on our side, please try running the script again~")
                x=subprocess.run(['python3','script.py'])
                game=26
                break
            if 'Enter your' in output[9]:
                move=generate_next_move(output[0:9])
                if move is None:
                    break
                p.sendline(f"{move[0]},{move[1]}".encode())
            elif 'You Lost' in output[9]:
                break
            else:
                break


def generate_next_move(board):
    if all(cell == '_' for row in board for cell in row):
        return (0, 0)
    move=perform_logical_deductions(board)
    if move is not None:
        return move
    move=perform_probability_strategy(board)
    return move


def perform_logical_deductions(board):
    updated = True
    while updated:
        updated = False
        for row in range(9):
            for col in range(9):
                cell = board[row][col]
                if cell in ['1','2','3','4','5','6','7','8']:
                    mine_count = int(cell)
                    neighbors = get_neighbors(row, col)
                    flagged_mines = int(0)
                    covered_cells = []
                    for neighbor_row, neighbor_col in neighbors:
                        neighbor = board[neighbor_row][neighbor_col]
                        if neighbor == 'M':
                            flagged_mines += 1
                        elif neighbor == '_':
                            covered_cells.append((neighbor_row, neighbor_col))
                    if int(flagged_mines)==mine_count:
                        for cell_row, cell_col in covered_cells:
                            updated=True
                            if board[cell_row][cell_col]=='_':
                                return (cell_row,cell_col)
                    elif len(covered_cells)+int(flagged_mines)==mine_count:
                        updated = True
                        for cell_row, cell_col in covered_cells:
                            board[cell_row][cell_col] = 'M'
    return None


def get_neighbors(row, col):
    neighbors = []
    for d_row in [-1, 0, 1]:
        for d_col in [-1, 0, 1]:
            if d_row == 0 and d_col == 0:
                continue
            else:
                neighbor_row = row + d_row
                neighbor_col = col + d_col
                if 0<=neighbor_row<9 and 0<=neighbor_col<9:
                    neighbors.append((neighbor_row, neighbor_col))
    return neighbors


def is_complete(board):
    for row in board:
        for cell in row:
            if cell == '_' or cell == 'M':
                return False
    return True

def perform_probability_strategy(board):
    minimum_probablity=float(100)
    move = None
    for row in range(9):
        for col in range(9):
            cell = board[row][col]
            if cell == '_':
                odds=0
                neighbor=get_neighbors(row,col)
                for n_row,n_col in neighbor:
                    if board[n_row][n_col] in ('0','1','2','3','4','5','6','7','8'):
                        odds+=int(board[n_row][n_col])
                    elif board[n_row][n_col]=='M':
                        odds-=1
                board[row][col]=odds/8
                if minimum_probablity>board[row][col]:
                    minimum_probablity=board[row][col]
                    move=(row,col)
                board[row][col]='_'
    return move

play()
