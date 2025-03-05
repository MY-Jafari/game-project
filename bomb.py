import random
import os
def G_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    return os.path.join(base_dir, filename)
def load_txt():
    scores_path = G_path("scores.txt")  
    if not os.path.exists(scores_path):  
        open(scores_path, "w").close()  
    with open(scores_path, "r") as file:
        scores = file.readlines()
    return [score.strip() for score in scores]
def save_scores(scores):
    scores_path = G_path("scores.txt")  
    with open(scores_path, "w") as file:
        for score in scores:
            file.write(score + "\n")
def display_scores(scores):
    print("\n--- All Scores ---")
    for score in scores:
        print(score)
    print("------------------\n")
def create_board(rows, cols, mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()
    while len(mine_positions) < mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        mine_positions.add((row, col))
    for (row, col) in mine_positions:
        board[row][col] = 'M'
    return board, mine_positions
def calculate_numbers(board, rows, cols):
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 'M':
                continue
            count = 0
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < rows and 0 <= c < cols and board[r][c] == 'M':
                        count += 1
            board[row][col] = count
def display_board(board, revealed):
    print("   " + " ".join(str(i) for i in range(len(board[0]))))
    print("  " + "-" * (2 * len(board[0]) + 1))
    for row in range(len(board)):
        print(row, end=" |")
        for col in range(len(board[0])):
            if revealed[row][col]:
                print(board[row][col], end=" ")
            else:
                print(".", end=" ")
        print()
def reveal_cell(board, revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == 0:
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < len(board) and 0 <= c < len(board[0]):
                    reveal_cell(board, revealed, r, c)
def count_revealed_cells(revealed):
    return sum(sum(row) for row in revealed)
def play_game(rows, cols, mines):
    scores = load_txt()  
    board, mine_positions = create_board(rows, cols, mines)
    calculate_numbers(board, rows, cols)
    revealed = [[False for _ in range(cols)] for _ in range(rows)] 
    game_over = False
    while not game_over:
        display_board(board, revealed)
        try:
            row = int(input("Enter row (0 to 6): "))
            col = int(input("Enter col (0 to 6): "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            continue
        if not (0 <= row < rows and 0 <= col < cols):
            print("Invalid row or column. Please enter values between 0 and 6.")
            continue
        if (row, col) in mine_positions:
            print("Game Over! You hit a mine.")
            game_over = True
        else:
            reveal_cell(board, revealed, row, col)
            if all(revealed[r][c] or (r, c) in mine_positions for r in range(rows) for c in range(cols)):
                print("Congratulations! You won!")
                game_over = True
    display_board(board, [[True for _ in range(cols)] for _ in range(rows)])
    revealed_count = count_revealed_cells(revealed)
    print(f"You revealed {revealed_count} cells.")

    scores.append(str(revealed_count))
    save_scores(scores)
    display_scores(scores)
if __name__ == "__main__":
    rows = 7
    cols = 7
    mines = 10
    play_game(rows, cols, mines)
