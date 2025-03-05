import random
import os

class player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def win_loss(self, result):
        if result == "win":
            print("this round you win!")
            self.wins +=1
        elif result == "loss":
            print("this round you lost!")
            self.losses +=1
        elif result == "tie":
            print("this round is a tie!")
            self.ties +=1
            pass

class Node:
    def __init__(self,data):
        self.data = data
        self.beats = []

    def add_edge(self,node):
        self.beats.append(node)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.build_graph()

    def add_node(self,data):
        node = Node(data)
        self.nodes[data] = node
        return node
    
    def add_edge(self,from_data,to_data):
        self.nodes[from_data].add_edge(self.nodes[to_data])
        
    def build_graph(self):
        rock = self.add_node("Rock")
        paper = self.add_node("Paper")
        scissors = self.add_node("Scissors")
        water = self.add_node("Water")
        fire = self.add_node("Fire")
        earth = self.add_node("Earth")

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
            
        player.win_loss(result)
        return result

class score:
    @staticmethod
    def print_score(player):
        print(f"\nGame over! {player.name}'s record:")
        print(f"wins: {player1.wins} \nlosses: {player1.losses} \nTie: {player1.ties}")

    @staticmethod
    def save_score(player):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        score_file_path = os.path.join(base_dir, "RPS_score.txt")
        with open(score_file_path, "a") as file:
            file.write(f"Player: {player.name}'s Stats: \n")
            file.write(f"{round} rounds play\n")
            file.write(f"Wins: {player.wins}\n")
            file.write(f"Losses: {player.losses}\n")
            file.write(f"Ties: {player.ties}\n")
            file.write("-" * 20 + "\n")
            
    @staticmethod
    def load_score():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        score_file_path = os.path.join(base_dir, "RPS_score.txt")
        print("----------Previous scores----------")
        try:
            with open(score_file_path, "r") as file:
                print(file.read())  
        except FileNotFoundError:
            print("Previous score data not found.")

def rounds():
    for i in range(int(round)):
        print(f"Round {i+1}")
        player_choice = input("Enter your choice (Rock, Paper, Scissors, Water, Fire, Earth): ").capitalize()
        while player_choice not in game_graph.nodes:
            player_choice = input("Please enter a valid choice (Rock, Paper, Scissors, Water, Fire, Earth): ").capitalize()
        computer_choice = game_graph.get_random_move()
        print(f"Computer choice: {computer_choice}")
        game_graph.determine_winner(player1,player_choice,computer_choice)

game_graph = Graph()
print("welcome to the Rock, Paper, Scissors, Water, Fire, Earth game!")
print("The rules are simple: Rock beats Scissors and Fire, Paper beats Rock and Earth, Scissors beats Paper and Earth,\n Water beats Rock and Fire, Fire beats Paper and Earth, Earth beats Water and Fire")

player.name = input("Enter your name: ")
player1 = player(player.name)

round = input(f"Hello {player.name}! how many rounds would you like to play? ")
while not round.isdigit() or int(round) < 1:
    round = input("Please enter a valid number of rounds: ")
print(f"You will be playing against the computer. The first to win {round} rounds wins the game!")
rounds()
score.print_score(player1)
score.save_score(player1)
score.load_score()
