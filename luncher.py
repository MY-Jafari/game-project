import os
import subprocess
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def print_menu():
    print("\n=== Welcome to Game Launcher ===")
    print("1. Rock Paper Scissors ")
    print("2. Minesweeper")
    print("3. Tic Tac Toe")
    print("4. Exit")
    print("=============================")
def launch_game(game_file):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(current_dir, game_file)
        if not os.path.exists(game_path):
            print(f"\nError: {game_file} not found!")
            return False
        subprocess.run(['python', game_path])
        return True
    except Exception as e:
        print(f"\nError launching game: {e}")
        return False
while True:
    clear_screen()
    print_menu()       
    choice = input("\nPlease select a game (1-4): ")       
    if choice == '1':
        if launch_game('RPS_game.py'):
            input("\nPress Enter to return to menu...")       
    elif choice == '2':
        if launch_game('bomb.py'):
            input("\nPress Enter to return to menu...")       
    elif choice == '3':
        if launch_game('Doz_game.py'):
            input("\nPress Enter to return to menu...")       
    elif choice == '4':
        print("\nThank you for playing! Goodbye!")
        break       
    else:
        print("\nInvalid choice! Please try again.")
        input("Press Enter to continue...")
