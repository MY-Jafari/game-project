from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui_Guess_word import Ui_MainWindow
import random
import sys

class GuessGame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.words = [
            "APPLE", "ANT", "AIR", "BALL", "BOOK", "BIRD", "CAT", "CAR", "CLOUD",
            "DOG", "DOOR", "DANCE", "EGG", "EARTH", "EYE", "FISH", "FLOWER", "FIRE",
            "GOAT", "GRASS", "GOLD", "HOUSE", "HORSE", "HAT", "ICE", "IRON", "ISLAND",
            "JUICE", "JUMP", "JEWEL", "KING", "KITE", "KEY", "LION", "LEAF", "LIGHT",
            "MOON", "MOUNTAIN", "MILK", "NEST", "NIGHT", "NOSE", "ORANGE", "OCEAN", "OWL",
            "PEN", "PLANT", "PARK", "QUEEN", "QUILT", "QUICK", "RABBIT", "RIVER", "RAIN",
            "SUN", "STAR", "SAND", "TREE", "TIGER", "TABLE", "UMBRELLA", "UNCLE", "UNIFORM",
            "VAN", "VOICE", "VALLEY", "WATER", "WIND", "WOLF", "XBOX", "XRAY", "XENON",
            "YELLOW", "YAHOO", "YEAR", "ZEBRA", "ZOO", "ZERO"
        ]

        self.word = random.choice(self.words)
        self.attempts = 0
        self.max_attempts = 8
        self.word_length = len(self.word)

        self.ui.label_status.setText(f"Guess the {self.word_length}-letter word.")
        self.ui.textBrowser_output.setText("_ " * self.word_length)

        self.ui.btn_submit.clicked.connect(self.submit_guess)

    def check_guess(self, word, guess):
        result = ["R"] * len(word)
        counts = {}

        for i in range(len(word)):
            if word[i] == guess[i]:
                result[i] = "G"
            else:
                counts[word[i]] = counts.get(word[i], 0) + 1

        for i in range(len(word)):
            if result[i] == "R" and guess[i] in counts and counts[guess[i]] > 0:
                result[i] = "Y"
                counts[guess[i]] -= 1

        return "".join(result)

    def submit_guess(self):
        guess = self.ui.lineEdit_guess.text().upper()
        if len(guess) != self.word_length:
            QMessageBox.warning(self, "Invalid", f"Please enter a {self.word_length}-letter word.")
            return

        self.attempts += 1
        result = self.check_guess(self.word, guess)
        self.ui.textBrowser_output.append(f"{guess} -> {result}")

        if result == "G" * self.word_length:
            QMessageBox.information(self, "Victory", "You win!")
            self.ui.label_status.setText("You guessed the word!")
            self.ui.btn_submit.setEnabled(False)
        elif self.attempts >= self.max_attempts:
            QMessageBox.critical(self, "Defeat", f"You lose... The word was: {self.word}")
            self.ui.label_status.setText("Game Over")
            self.ui.btn_submit.setEnabled(False)
        else:
            self.ui.label_status.setText(f"Attempt {self.attempts + 1}/{self.max_attempts}")
            self.ui.lineEdit_guess.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GuessGame()
    window.show()
    sys.exit(app.exec_())
