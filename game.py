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
    
    def handle_player_turn(self, player):

        player.is_upgraded = False
        player.step += 1

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

            \t\t[{player.get_card_info("name", player.r1_circle)}] \t[{player.get_card_info("name", player.v_circle)}] \t[{player.get_card_info("name", player.r2_circle)}] \t[Deck]
            \t\tcount:{player.card_count(player.r1_circle)}  \tv_count:{player.card_count(player.v_circle)} \tcount:{player.card_count(player.r2_circle)}  \tcount: {player.card_count(player.deck)}

            \t[Damage Zone]\t[{player.get_card_info("name", player.r3_circle)}] \t[{player.get_card_info("name", player.r4_crircle)}] \t[{player.get_card_info("name", player.r5_circle)}]\t[Drop Zone]
            count:{player.card_count(player.damage_zone)}\tcount:{player.card_count(player.r3_circle)} count:{player.card_count(player.r4_crircle)} count:{player.card_count(player.r5_circle)} \tcount:{player.card_count(player.drop_zone)}

            [{player.show_hand()}]
            h_count: {player.card_count(player.show_hand())}
            """)

            user_input = input("Pick a Move (p: place card, e: end turn): ").lower()

            if user_input == "p":
                
                """First do a check on the current grade"""
                player_current_grade = player.get_current_grade()
        
                map_grade = {0: [1, 0], 1: [2, 1], 2: [3, 2], 3: [3, 2]}
                
                # Determine valid cards based on upgrade status and grade
                if not player.is_upgraded:
                    card_option = [card for card in player.hand if card["grade"] in map_grade.get(player_current_grade)]
                else:
                    card_option = [card for card in player.hand if card["grade"] <= player_current_grade]
                
                if not card_option:
                    print("You have no valid cards to place.")
                    continue
                    
                print("Current Options: ", card_option)
                    

                if len(card_option) == 0:
                    print("Currently you have no suitable card to place try other things")
                    break

                else:
                    """First do a check on the current grade"""
                    player_current_grade = player.get_current_grade()
            
                    map_grade = {0: [1, 0], 1: [2, 1], 2: [3, 2], 3: [3, 2]}
                    
                    # Determine valid cards based on upgrade status and grade
                    if not player.is_upgraded:
                        card_option = [card for card in player.hand if card["grade"] in map_grade.get(player_current_grade)]
                    else:
                        card_option = [card for card in player.hand if card["grade"] <= player_current_grade]
                    
                    if not card_option:
                        print("You have no valid cards to place.")
                        continue
                        
                    # print("Current Options: ", card_option)                   
                    while True:
                        try:
                            choice_index = int(input(f"{player.name}, choose a card (0-{len(card_option)-1}): "))
                            if 0 <= choice_index < len(card_option):
                                selected_card = card_option[choice_index]
                                
                                position_index = str(input(f"{player.name}, choose a position to place the card: "))
                        
                                if position_index == "v":
                                    if selected_card["grade"] > player_current_grade and not player.is_upgraded:
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.v_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                            player.grade_upgrade()
                                            player.is_upgraded = True
                                    elif selected_card["grade"] == player_current_grade:
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.v_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")

                                elif position_index == "r1":
                                    if selected_card["grade"] <= player_current_grade:
                                        if player.r1_circle:
                                            discard = player.r1_circle.pop(0)
                                            player.drop_zone.append(discard)
                                        
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.r1_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                        else:
                                            print("option invalid try again")

                                elif position_index == "r2":
                                    if selected_card["grade"] <= player_current_grade:
                                        if player.r2_circle:
                                            discard = player.r2_circle.pop(0)
                                            player.drop_zone.append(discard)
                                        
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.r2_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                        else:
                                            print("option invalid try again")
                                    else:
                                        print("option invalid try again")

                                elif position_index == "r3":
                                    if selected_card["grade"] <= player_current_grade:
                                        if player.r3_circle:
                                            discard = player.r3_circle.pop(0)
                                            player.drop_zone.append(discard)
                                        
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.r3_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                        else:
                                            print("option invalid try again")
                                    else:
                                        print("option invalid try again")
                                

                                elif position_index == "r4":
                                    if selected_card["grade"] <= player_current_grade:
                                        if player.r4_circle:
                                            discard = player.r4_circle.pop(0)
                                            player.drop_zone.append(discard)
                                        
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.r4_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                        else:
                                            print("option invalid try again")
                                    else:
                                        print("option invalid try again")
                                

                                elif position_index == "r5":
                                    if selected_card["grade"] <= player_current_grade:
                                        if player.r5_circle:
                                            discard = player.r5_circle.pop(0)
                                            player.drop_zone.append(discard)
                                        
                                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                        if confirmation == 'y':
                                            player.r5_circle.append(selected_card)
                                            player.hand.remove(selected_card)
                                            print(f"{player.name} rides with {selected_card['name']}!")
                                        else:
                                            print("option invalid try again")
                                    else:
                                        print("option invalid try again")

                                # if selected_card["grade"] > player_current_grade and not player.is_upgraded:
                                #     confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                #     if confirmation == 'y':
                                #         player.v_circle.append(selected_card)
                                #         player.hand.remove(selected_card)
                                #         print(f"{player.name} rides with {selected_card['name']}!")
                                #         player.grade_upgrade()
                                #         player.is_upgraded = True
                                # elif selected_card["grade"] <= player_current_grade:
                                #     print(f"Placing {selected_card['name']} as a rearguard.")
                                break
                            else:
                                print("Invalid choice. Please enter a number within your hand's range.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
            
            elif user_input == "m":
                position_index = str(input(f"{player.name}, choose a position to move the card: "))

                if position_index == "r1":
                    if not player.r3_circle:
                        move = player.r1_circle.pop(0)
                        player.r3_circle.append(move)

                        print("card move back")
                    else:
                        print("Can't be moved back due to a card.")
                
                if position_index == "r2":
                    if not player.r5_circle:
                        move = player.r2_circle.pop(0)
                        player.r5_circle.append(move)

                        print("card move back")
                    else:
                        print("Can't be moved back due to a card.")

                if position_index == "r3":
                    if not player.r1_circle:
                        move = player.r3_circle.pop(0)
                        player.r1_circle.append(move)

                        print("card move front")
                    else:
                        print("Can't be moved back due to a card.")

                if position_index == "r5":
                    if not player.r2_circle:
                        move = player.r5_circle.pop(0)
                        player.r2_circle.append(move)

                        print("card move front")
                    else:
                        print("Can't be moved back due to a card.")

            elif user_input == "e":
                print(f"{player.name} ends their turn.")
            else:
                print("Invalid input. Please try again.")

    def run_game(self):
        print("Load Game")  
        
        self.setup_game() 
        
        first_to_go = self.coin_flip()
        self.current_player_index = self.players.index(first_to_go)

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