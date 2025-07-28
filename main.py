import random
from game import Game

def coin_flip():
    result = random.choice(["Heads", "Tails"])
    print(f"The coin landed on: {result}")
    
    if result == "Heads":
        result = 0
    else:
        result = 1
    return result

def main():
    start_game = Game()
    start_game.run_game()

if __name__ == "__main__":
    main()
    print("Program finished.")