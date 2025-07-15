import sys
import random
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_RPS_Game import Ui_RPSGameWindow  
class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def update_result(self, result):
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        elif result == "tie":
            self.ties += 1

class Node:
    def __init__(self, data):
        self.data = data
        self.beats = []

    def add_edge(self, node):
        self.beats.append(node)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.build_graph()

    def add_node(self, data):
        node = Node(data)
        self.nodes[data] = node
        return node

    def add_edge(self, from_data, to_data):
        self.nodes[from_data].add_edge(self.nodes[to_data])

    def build_graph(self):
        for move in ["Rock", "Paper", "Scissors", "Water", "Fire", "Earth"]:
            self.add_node(move)

        self.add_edge("Rock", "Scissors")
        self.add_edge("Rock", "Fire")
        self.add_edge("Paper", "Rock")
        self.add_edge("Paper", "Earth")
        self.add_edge("Scissors", "Paper")
        self.add_edge("Scissors", "Earth")
        self.add_edge("Water", "Rock")
        self.add_edge("Water", "Fire")
        self.add_edge("Fire", "Paper")
        self.add_edge("Fire", "Earth")
        self.add_edge("Earth", "Water")
        self.add_edge("Earth", "Fire")

    def get_random_move(self):
        return random.choice(list(self.nodes.keys()))

    def determine_winner(self, player, player_choice, computer_choice):
        player_node = self.nodes[player_choice]
        computer_node = self.nodes[computer_choice]

        if player_node == computer_node:
            result = "tie"
        elif computer_node in player_node.beats:
            result = "win"
        else:
            result = "loss"

        player.update_result(result)
        return result

class RPSGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RPSGameWindow()
        self.ui.setupUi(self)

        self.graph = Graph()
        self.player = None
        self.total_rounds = 0
        self.current_round = 0

        # دکمه‌ها
        self.ui.btn_start.clicked.connect(self.start_game)
        self.ui.btn_rock.clicked.connect(lambda: self.play_round("Rock"))
        self.ui.btn_paper.clicked.connect(lambda: self.play_round("Paper"))
        self.ui.btn_scissors.clicked.connect(lambda: self.play_round("Scissors"))
        self.ui.btn_water.clicked.connect(lambda: self.play_round("Water"))
        self.ui.btn_fire.clicked.connect(lambda: self.play_round("Fire"))
        self.ui.btn_earth.clicked.connect(lambda: self.play_round("Earth"))
        self.ui.btn_show_scores.clicked.connect(self.load_scores)

        self.disable_move_buttons()

    def start_game(self):
        name = self.ui.lineEdit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return

        self.player = Player(name)
        self.total_rounds = self.ui.spinBox_rounds.value()
        self.current_round = 0
        self.update_score_label()
        self.ui.label_result.setText("Game started! Choose your move.")
        self.enable_move_buttons()

    def play_round(self, player_choice):
        if self.current_round >= self.total_rounds:
            QMessageBox.information(self, "Game Over", "Game already finished!")
            self.disable_move_buttons()
            return

        computer_choice = self.graph.get_random_move()
        result = self.graph.determine_winner(self.player, player_choice, computer_choice)
        self.current_round += 1

        result_text = {
            "win": "You win!",
            "loss": "You lose!",
            "tie": "It's a tie!"
        }

        self.ui.label_result.setText(
            f"Round {self.current_round}/{self.total_rounds}\n"
            f"Your move: {player_choice}\n"
            f"Computer move: {computer_choice}\n"
            f"Result: {result_text[result]}"
        )

        self.update_score_label()

        if self.current_round == self.total_rounds:
            self.disable_move_buttons()
            QMessageBox.information(self, "Game Finished", "All rounds completed. Saving score.")
            self.save_score()

    def update_score_label(self):
        self.ui.label_score.setText(
            f"Wins: {self.player.wins} | Losses: {self.player.losses} | Ties: {self.player.ties}"
        )

    def disable_move_buttons(self):
        for btn in [
            self.ui.btn_rock,
            self.ui.btn_paper,
            self.ui.btn_scissors,
            self.ui.btn_water,
            self.ui.btn_fire,
            self.ui.btn_earth
        ]:
            btn.setEnabled(False)

    def enable_move_buttons(self):
        for btn in [
            self.ui.btn_rock,
            self.ui.btn_paper,
            self.ui.btn_scissors,
            self.ui.btn_water,
            self.ui.btn_fire,
            self.ui.btn_earth
        ]:
            btn.setEnabled(True)

    def save_score(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "RPS_score.txt")
        with open(path, "a", encoding="utf-8") as file:
            file.write(f"Player: {self.player.name}\n")
            file.write(f"Rounds: {self.total_rounds}\n")
            file.write(f"Wins: {self.player.wins}\n")
            file.write(f"Losses: {self.player.losses}\n")
            file.write(f"Ties: {self.player.ties}\n")
            file.write("-" * 30 + "\n")

    def load_scores(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "RPS_score.txt")
        if not os.path.exists(path):
            QMessageBox.information(self, "No Scores", "No previous scores found.")
            return
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
        QMessageBox.information(self, "Previous Scores", data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RPSGameWindow()
    window.show()
    sys.exit(app.exec_())
