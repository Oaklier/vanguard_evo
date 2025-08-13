from player import Player
import json
import random

def create_deck(decklist):
    """Expands a decklist with counts into a flat list of individual card objects."""
    playable_deck = []
    for card_info in decklist:
        card_object = {key: value for key, value in card_info.items() if key != "count"}
        
        for _ in range(card_info["count"]):
            playable_deck.append(card_object.copy())

    return playable_deck

def load_deck(filename):
    """Loads a decklist from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)["deck"]
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    
deck_1 = load_deck('./decks/deck_1.json')
deck_2 = load_deck('./decks/deck_2.json')

deck_1_craft = create_deck(deck_1)
deck_2_craft = create_deck(deck_2)

def coin_flip():
    result = random.choice(["Heads", "Tails"])
    print(f"The coin landed on: {result}")
    
    if result == "Heads":
        result = 0
    else:
        result = 1
    return result

class Game:
    def __init__(self):
        self.player1 = Player("Player_1", deck_1_craft)
        self.player2 = Player("Player_2", deck_2_craft)
        self.players = [self.player1, self.player2]
        self.current_player_index = 0
        self.game_running = True

    def _get_current_player(self):
        return self.players[self.current_player_index]
    
    def _switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    

    def _setup_game(self):
        print("\n--- Game Setup Phase ---")

        for player in self.players:
            print(f"\n{player.name} select your starter: ")

            starter_options = [card for card in player.deck if card["grade"] == 0]

            while True:
                print("Starter options: ", [card['name'] for card in starter_options])
                print("Total cards in deck before selection: ", player.card_count(player.deck))
                try:
                    choice_index = int(input(f"{player.name}, choose a card to ride (0-{len(starter_options)-1}): "))
                    if 0 <= choice_index < len(starter_options):

                        selected_card = starter_options[choice_index]

                        player.deck.remove(selected_card)
                        
                        player.vangaurd_circle.append(selected_card)
                        
                        print(f"{player.name} rides with {selected_card['name']}!")

                        player.shuffle_cards(player.deck)
                        player.draw_cards(5)
                        player.show_hand()

                        print("Total cards in deck after selection: ", player.card_count(player.deck))
                        break
                    else:
                        print("Invalid choice. Please enter a number within your hand's range.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    
    def _handle_player_turn(self, player):
        print(f"\n--- It's {player.name}'s turn. ---")
        user_input = ""
        while user_input != "e":
            if self.player1.is_defeated() or self.player2.is_defeated():
                self.game_running = False
                break 

            user_input = input("Pick a Move (d: draw, f: show field, e: end turn): ").lower()
            
            if user_input == "d":
                player.draw_cards()
            elif user_input == "f":
                print( "Currently: ", player.vangaurd_circle)
            elif user_input == "e":
                print(f"{player.name} ends their turn.")
            else:
                print("Invalid input. Please try again.")


    def run_game(self):
        print("Game Start")
        
        self._setup_game() 

        while self.game_running:
            current_player = self._get_current_player()
            self._handle_player_turn(current_player)

            if not self.game_running:
                break

            self._switch_player() 

        print("\n--- Game Over ---")

        if self.player1.is_defeated() and self.player2.is_defeated():
            print("Both players were defeated! It's a tie!")
        elif self.player1.is_defeated():
            print(f"{self.player2.name} wins!")
        elif self.player2.is_defeated():
            print(f"{self.player1.name} wins!")
        else:
            print("Game ended for an unknown reason (neither player defeated).")