import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from ui_minesweeper import Ui_MainWindow

class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.rows = 7
        self.cols = 7
        self.mines = 10

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        self.ui.btn_restart.clicked.connect(self.restart_game)
        self.setup_game()

    def setup_game(self):
        self.board, self.mine_positions = self.create_board(self.rows, self.cols, self.mines)
        self.calculate_numbers(self.board, self.rows, self.cols)

        for i in reversed(range(self.ui.gridLayout_board.count())):
            self.ui.gridLayout_board.itemAt(i).widget().setParent(None)

        for row in range(self.rows):
            for col in range(self.cols):
                btn = QPushButton("")
                btn.setFixedSize(40, 40)
                btn.clicked.connect(lambda _, r=row, c=col: self.handle_click(r, c))
                self.ui.gridLayout_board.addWidget(btn, row, col)
                self.buttons[row][col] = btn

        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.ui.label_status.setText("Game Started")

    def create_board(self, rows, cols, mines):
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        mine_positions = set()
        while len(mine_positions) < mines:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            mine_positions.add((r, c))
        for (r, c) in mine_positions:
            board[r][c] = 'M'
        return board, mine_positions

    def calculate_numbers(self, board, rows, cols):
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

    def handle_click(self, row, col):
        if self.revealed[row][col]:
            return
        self.reveal_cell(row, col)
        if (row, col) in self.mine_positions:
            self.buttons[row][col].setText("💣")
            self.ui.label_status.setText("Game Over!")
            self.reveal_all()
            QMessageBox.information(self, "Game Over", "You hit a mine!")
        elif self.check_win():
            self.ui.label_status.setText("You Won!")
            self.reveal_all()
            QMessageBox.information(self, "Congratulations!", "You cleared the board!")

    def reveal_cell(self, row, col):
        if self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        value = self.board[row][col]
        btn = self.buttons[row][col]
        if value == 0:
            btn.setText("")
            btn.setStyleSheet("background-color: #ddd")
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        self.reveal_cell(r, c)
        elif value == 'M':
            btn.setText("💣")
        else:
            btn.setText(str(value))
            btn.setStyleSheet("background-color: #ccc")

    def reveal_all(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col]:
                    self.reveal_cell(row, col)

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and self.board[row][col] != 'M':
                    return False
        return True

    def restart_game(self):
        self.setup_game()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Minesweeper()
    window.show()
    sys.exit(app.exec_())
