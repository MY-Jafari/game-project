import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui_launcher import Ui_Dialog  
class GameLauncher(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.RPS.clicked.connect(lambda: self.launch_game("RPS_game.py"))
        self.ui.Mine.clicked.connect(lambda: self.launch_game("minesweeper.py"))
        self.ui.Doz.clicked.connect(lambda: self.launch_game("Doz_game.py"))
        self.ui.Guess.clicked.connect(lambda: self.launch_game("guess_word.py"))

    def launch_game(self, game_file):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(current_dir, game_file)

        if not os.path.exists(game_path):
            QMessageBox.critical(self, "Error", f"Game file '{game_file}' not found!")
            return

        try:
            subprocess.Popen(['python', game_path], shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch game:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = GameLauncher()
    launcher.setWindowTitle("Game Launcher")
    launcher.show()
    sys.exit(app.exec_())
