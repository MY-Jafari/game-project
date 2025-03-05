import math
import os

class Player():
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.score = 0

    def update_score(self, result):
        if result == "win":
            print(f"{self.name} wins this round!")
            self.wins += 1
            self.score += 3  
        elif result == "loss":
            print(f"{self.name} lost this round!")
            self.losses += 1
        elif result == "tie":
            print(f"{self.name}, this round is a tie!")
            self.ties += 1
            self.score += 1  

class Doz():
    def __init__(self, player):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = player
        self.human = 'O'
        self.computer = 'X'

    def print_board_with_coordinates(self):
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        coord_map = self.convert_to_coordinates()  
        
        for i in range(3):
            print(" | ".join([names[i * 3 + j] if self.board[i][j] == ' ' else self.board[i][j] for j in range(3)]))
            if i < 2:
                print(" ---" * 2)  
    def print_board(self):
        for i in range(3):
            print(" | ".join(self.board[i]).replace(" ", "-"))  
            if i < 2:
                print(" ---" * 2)  

    def is_move_left(self):
        return any(' ' in row for row in self.board)

    def check_winner(self, mark):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == mark:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == mark:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == mark:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == mark:
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
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = self.computer
                        best = max(best, self.minimax(depth+1, False))
                        self.board[row][col] = ' '
            return best
        else:
            best = math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = self.human
                        best = min(best, self.minimax(depth+1, True))
                        self.board[row][col] = ' '
            return best
        
    def find_best_move(self):
        best_val = -math.inf
        best_move = (-1, -1)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.computer
                    move_val = self.minimax(0, False)
                    self.board[row][col] = ' ' 

                    if move_val > best_val:
                        best_move = (row, col)
                        best_val = move_val
        return best_move
    
    def convert_to_coordinates(self):
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        coords = {}
        for i in range(3):
            for j in range(3):
                coords[names[i * 3 + j]] = (i, j)  
        return coords

    def play_game(self):
        coord_map = self.convert_to_coordinates()
        
        while self.is_move_left():
            self.print_board_with_coordinates()  
            print("\nAvailable choices: a, b, c, d, e, f, g, h, i")
            move = input("Enter your choice (a-i): ").lower()
            while move not in coord_map:
                print("Invalid move!")
                move = input("Enter your choice (a-i): ").lower()
            
            row, col = coord_map[move]
            while self.board[row][col] != ' ':
                print("Invalid choice!")
                move = input("Enter your choice (a-i): ").lower()
                row, col = coord_map[move]

            self.board[row][col] = self.human

            if self.check_winner(self.human):
                self.print_board_with_coordinates()  
                self.player.update_score("win")
                break
            if not self.is_move_left():
                self.print_board_with_coordinates()  
                self.player.update_score("tie")
                break

            print("Computer's turn...")
            best_move = self.find_best_move()
            self.board[best_move[0]][best_move[1]] = self.computer

            if self.check_winner(self.computer):
                self.print_board_with_coordinates()  
                self.player.update_score("loss")
                break
            if not self.is_move_left():
                self.print_board_with_coordinates()  
                self.player.update_score("tie")
                break

class score():  
    @staticmethod
    def print_score(player):
        print(f"{player.name}'s Stats: \n Wins: {player.wins} \n Losses: {player.losses} \n Ties: {player.ties} \n Score: {player.score}")

    @staticmethod
    def save_score(player):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        score_file_path = os.path.join(base_dir, "Doz_score.txt")
        with open(score_file_path, "a") as file:
            file.write(f"Player: {player.name}'s Stats: \n")
            file.write(f"{round} rounds play\n")
            file.write(f"Wins: {player.wins}\n")
            file.write(f"Losses: {player.losses}\n")
            file.write(f"Ties: {player.ties}\n")
            file.write(f"Score: {player.score}\n")
            file.write("-" * 20 + "\n")
            
    @staticmethod
    def load_score():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        score_file_path = os.path.join(base_dir, "Doz_score.txt")
        print("----------Previous scores----------")
        try:
            with open(score_file_path, "r") as file:
                print(file.read()) 
        except FileNotFoundError:
            print("Previous score data not found.")


def rounds():
    for i in range(int(round)):
        print(f"Round {i+1}")
        game = Doz(player1)
        game.play_game()
        print("-" * 20)

print("Welcome to the Tic Tac Toe game!")
print("Your choice mark with 'O' and computer choice mark with 'X'!")

Player.name = input("Enter your name: ")
player1 = Player(Player.name)

round = input(f"Hello {Player.name}! how many rounds would you like to play? ")
while not round.isdigit() or int(round) < 1:
    round = input("Please enter a valid number of rounds: ")
print(f"You will be playing against the computer. The first to win {round} rounds wins the game!")

rounds()
score.print_score(player1)
score.save_score(player1)
score.load_score()
