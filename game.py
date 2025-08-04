from player import Player
import json

def load_deck_data(filename):
    """
    Loads card data and returns a dictionary for efficient lookup
    of card properties by name.
    """
    deck_array = []

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        card_lookup = {}
        for card in data["deck"]:
            card_name = card["name"]
        
            card_lookup[card_name] = {
                "grade": card.get("grade"),
                "count": card.get("count"),
                "type": card.get("type", "Normal")
            }
         
        for card in data["deck"]:
            deck_array.extend([card["name"]] * card["count"])

        return card_lookup, deck_array

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON format.")
        return None
    
deck_1, card_name1 = load_deck_data('./decks/deck_1.json')
deck_2, card_name2 = load_deck_data('./decks/deck_2.json')

class Game:
    def __init__(self):
        self.player1 = Player("Player_1", card_name1)
        self.player2 = Player("Player_2", card_name2)
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
            print(f"\n{player.name} draws initial cards...")
            player.shuffle_cards(player.deck)
            print(player.deck)
            player.draw_cards(5)
            player.show_hand()

            while True:
                print("Show the Deck: " ,player.deck)

                deck = player.deck
                try:
                    choice_index = int(input(f"{player.name}, choose a card to play to the field (0-{len(deck)-1}): "))
                    if 0 <= choice_index < len(player.deck):
                        player.play_card_to_field(choice_index, player.vangaurd_circle)
                        player.show_field(player.vangaurd_circle)
                        break
                    else:
                        print("Invalid choice. Please enter a number within your hand's range.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        print("\n--- Setup Complete! Game is ready to start. ---")


    
    def _handle_player_turn(self, player):
        print(f"\n--- It's {player.name}'s turn. ---")
        player.show_hand()
        user_input = ""
        while user_input != "e":
            if self.player1.is_defeated() or self.player2.is_defeated():
                self.game_running = False
                # Exit current player's turn if game is over
                break 

            user_input = input("Pick a Move (d: draw, f: show field, e: end turn): ").lower()

            player.show_hand()
            
            if user_input == "d":
                player.draw_cards()
            elif user_input == "f":
                player.show_field(player.vangaurd_circle)
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