from player import Player
import json
import random


def load_deck(filename):
    """Loads a decklist from a JSON file."""
    try:
        with open(filename, 'r') as f:

            """Expands a decklist with counts into a flat list of individual card objects."""
            deck = []
            for card_info in json.load(f)["deck"]:
                card_object = {key: value for key, value in card_info.items() if key != "count"}
                
                for _ in range(card_info["count"]):
                    deck.append(card_object.copy())

            return deck
        
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    
class Game:
    def __init__(self):
        deck_1 = load_deck('./decks/deck_1.json')
        deck_2 = load_deck('./decks/deck_2.json')
        self.player1 = Player("Player_1", deck_1)
        self.player2 = Player("Player_2", deck_2)
        self.players = [self.player1, self.player2]
        self.current_player_index = 0
        self.game_running = True
    
    def coin_flip(self):
        result = random.choice(["Heads", "Tails"])
        print(f"The coin landed on: {result}")
    
        if result == "Heads":
            return self.player1
        else:
            return self.player2
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    

    def setup_game(self):
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
                        
                        player.v_circle.append(selected_card)
                        
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
        
        print("\n--- Setup Completed ---")
    
    def condition_to_end(self):
        pass

    def handle_player_turn(self, player):

        print(f"\n--- It's {player.name}'s turn. ---")
        print(f"\n--- {player.name} draw. ---")
        player.draw_cards(1)
        user_input = ""
        while user_input != "e":
            if self.player1.is_defeated() or self.player2.is_defeated():
                self.game_running = False
                break 
            
            """Playmat"""

            print(f"""
            \t\t\t[]
            \t\t\tcount:

            \t\t[] \t[{player.get_card_info("name", player.v_circle)}] \t[]
            \t\tcount: v_count:{player.card_count(player.v_circle)} count: 

            \t[]\t[] \t[] \t[]\t[]
            count:\tcount: count: count: \tcount:

            \t\t[] \t[] \t[]\t[]
            \t\tcount: count: count: \tcount:

            [{player.show_hand()}]
            h_count: {player.card_count(player.show_hand())}
            """)

            user_input = input("Pick a Move (p: place card, e: end turn): ").lower()

            if user_input == "p":
                """First do a check on the current grade"""
                player_current_grade = player.get_current_grade()

                if player.is_upgraded == False:
                    if player_current_grade == 0: 
                        card_option = [card for card in player.hand if card["grade"] == 1 or card["grade"] == 0]
                        try:
                            print("Here are the options: ", card_option)
                            choice_index = int(input(f"{player.name}, choose a card to ride (0-{len(card_option)-1}): "))
                            if 0 <= choice_index < len(card_option):

                                selected_card = card_option[choice_index]
                                
                                if selected_card["grade"] == 1:
                                    print("Grade 1")
                                    player.v_circle.append(selected_card)
                                    player.hand.remove(selected_card)
                                    print(f"{player.name} rides with {selected_card['name']}! on the Vangaurd Circle")       
                                    player.grade_upgrade()  
                                    player.is_upgraded = True
                                else:
                                    print("Grade 0")

                            else:
                                print("Invalid choice. Please enter a number within your hand's range.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    
                    elif player_current_grade == 1: 
                        card_option = [card for card in player.hand if card["grade"] == 2 or card["grade"] == 1]
                        try:
                            print("Here are the options: ", card_option)
                            choice_index = int(input(f"{player.name}, choose a card to ride (0-{len(card_option)-1}): "))
                            if 0 <= choice_index < len(card_option):

                                selected_card = card_option[choice_index]
                                
                                if selected_card["grade"] == 2:
                                    print("Grade 2")
                                    player.v_circle.append(selected_card)
                                    player.hand.remove(selected_card)
                                    print(f"{player.name} rides with {selected_card['name']}! on the Vangaurd Circle")       
                                    player.grade_upgrade()  
                                    player.is_upgraded = True
                                    print("Whats up man: ", player.is_upgraded)

                                else:
                                    print("Grade 1")
                    
                            else:
                                print("Invalid choice. Please enter a number within your hand's range.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    elif player_current_grade == 2: 
                        card_option = [card for card in player.hand if card["grade"] == 3 or card["grade"] == 2]
                        try:
                            print("Here are the options: ", card_option)
                            choice_index = int(input(f"{player.name}, choose a card to ride (0-{len(card_option)-1}): "))
                            if 0 <= choice_index < len(card_option):

                                selected_card = card_option[choice_index]
                                
                                if selected_card["grade"] == 3:
                                    print("Grade 3")
                                    player.v_circle.append(selected_card)
                                    player.hand.remove(selected_card)
                                    print(f"{player.name} rides with {selected_card['name']}! on the Vangaurd Circle")       
                                    player.grade_upgrade()  
                                    player.is_upgraded = True
                                    print("Whats up man: ", player.is_upgraded)

                                else:
                                    print("Grade 2")
                    
                            else:
                                print("Invalid choice. Please enter a number within your hand's range.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    elif player_current_grade == 3: 
                        card_option = [card for card in player.hand if card["grade"] == 3 or card["grade"] == 2]
                        try:
                            print("Here are the options: ", card_option)
                            choice_index = int(input(f"{player.name}, choose a card to ride (0-{len(card_option)-1}): "))
                            if 0 <= choice_index < len(card_option):

                                selected_card = card_option[choice_index]
                                
                                if selected_card["grade"] == 3:
                                    print("Grade 3")
                                    player.v_circle.append(selected_card)
                                    player.hand.remove(selected_card)
                                    print(f"{player.name} rides with {selected_card['name']}! on the Vangaurd Circle")       
                                    player.grade_upgrade()  
                                    player.is_upgraded = True
                                    print("Whats up man: ", player.is_upgraded)

                                else:
                                    print("Grade 2")
                    
                            else:
                                print("Invalid choice. Please enter a number within your hand's range.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                elif player.is_upgraded == True:
                    print("Cannot upgrade anymore wait for ur next turn")
                
            elif user_input == "e":
                print(f"{player.name} ends their turn.")
                player.is_upgraded = False
            else:
                print("Invalid input. Please try again.")

    def run_game(self):
        print("Load Game")
        
        self.setup_game() 
        
        current_player = self.coin_flip()
        self.handle_player_turn(current_player)

        while self.game_running:
            current_player = self.get_current_player()
            self.handle_player_turn(current_player)

            if not self.game_running:
                break

            self.switch_player() 

        print("\n--- Game Over ---")

        if self.player1.is_defeated() and self.player2.is_defeated():
            print("Both players were defeated! It's a tie!")
        elif self.player1.is_defeated():
            print(f"{self.player2.name} wins!")
        elif self.player2.is_defeated():
            print(f"{self.player1.name} wins!")
        else:
            print("Game ended for an unknown reason (neither player defeated).")