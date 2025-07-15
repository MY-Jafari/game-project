from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui_Doze_game import Ui_MainWindow
import math
import os

class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.score = 0

    def update_score(self, result):
        if result == "win":
            self.wins += 1
            self.score += 3
        elif result == "loss":
            self.losses += 1
        elif result == "tie":
            self.ties += 1
            self.score += 1

class DozGame(QtWidgets.QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.player = player
        self.human = 'O'
        self.computer = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        self.buttons = [
            [self.ui.btn_00, self.ui.btn_01, self.ui.btn_02],
            [self.ui.btn_10, self.ui.btn_11, self.ui.btn_12],
            [self.ui.btn_20, self.ui.btn_21, self.ui.btn_22]
        ]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].clicked.connect(lambda _, r=i, c=j: self.handle_click(r, c))

        self.ui.btn_restart.clicked.connect(self.reset_board)
        self.ui.btn_exit.clicked.connect(self.close)

        self.reset_board()

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                btn = self.buttons[row][col]
                btn.setText("")
                btn.setEnabled(True)
        self.ui.label_status.setText(f"{self.player.name}'s turn")

    def handle_click(self, row, col):
        if self.board[row][col] != ' ':
            return

        self.board[row][col] = self.human
        self.buttons[row][col].setText(self.human)
        self.buttons[row][col].setEnabled(False)

        if self.check_winner(self.human):
            self.player.update_score("win")
            self.end_game(f"{self.player.name} wins!")
            return
        if not self.is_move_left():
            self.player.update_score("tie")
            self.end_game("It's a tie!")
            return

        move = self.find_best_move()
        if move:
            r, c = move
            self.board[r][c] = self.computer
            self.buttons[r][c].setText(self.computer)
            self.buttons[r][c].setEnabled(False)

        if self.check_winner(self.computer):
            self.player.update_score("loss")
            self.end_game("Computer wins!")
            return
        if not self.is_move_left():
            self.player.update_score("tie")
            self.end_game("It's a tie!")
            return

    def end_game(self, message):
        self.ui.label_status.setText(message)
        QMessageBox.information(self, "Game Over", message)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setEnabled(False)

    def is_move_left(self):
        return any(' ' in row for row in self.board)

    def check_winner(self, mark):
        for i in range(3):
            if all(self.board[i][j] == mark for j in range(3)):
                return True
            if all(self.board[j][i] == mark for j in range(3)):
                return True
        if all(self.board[i][i] == mark for i in range(3)):
            return True
        if all(self.board[i][2 - i] == mark for i in range(3)):
            return True
        return False

    def evaluate(self):
        if self.check_winner(self.computer):
            return 10
        if self.check_winner(self.human):
            return -10
        return 0

    def minimax(self, depth, is_max):
        score = self.evaluate()
        if score == 10 or score == -10:
            return score
        if not self.is_move_left():
            return 0

        if is_max:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.computer
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[i][j] = ' '
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.human
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[i][j] = ' '
            return best

    def find_best_move(self):
        best_val = -math.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.computer
                    move_val = self.minimax(0, False)
                    self.board[i][j] = ' '
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QInputDialog

    app = QtWidgets.QApplication(sys.argv)

    name, ok = QInputDialog.getText(None, "Enter Name", "Please enter your name:")
    if not ok or not name.strip():
        sys.exit()
    player = Player(name.strip())

    window = DozGame(player)
    window.show()
    sys.exit(app.exec_())
