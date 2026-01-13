from player import Player
import json
import random
import os

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
                        
                        player.play_area[1].append(selected_card)
                        
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

        print(f"\nIt's {player.name}'s turn.")

        player.is_upgraded = False
        player.step += 1

        #PHASE

        user_input = ""
        while user_input != "e":
            if self.player1.is_defeated() or self.player2.is_defeated():
                self.game_running = False
                break 

            #Stand
            print(f"\n--- Stand Phase. ---")
    
            #Draw
            print(f"\n--- Draw Phase. ---")
            print(f"\n{player.name} draw.")
            player.draw_cards(1)
            
            #Ride
            print(f"\n--- Ride Phase. ---")

            player.show_playmat()
            """First do a check on the current grade"""
            player_current_grade = player.get_current_grade()
    
            map_grade = {0: [1, 0], 1: [2, 1], 2: [3, 2], 3: [3, 2]}
            
            card_option = [card for card in player.hand if card["grade"] in map_grade.get(player_current_grade)]
            
            if not card_option:
                print("You have no valid cards to place.")
                continue
                
            print("Current Options: ", card_option)
                

            if len(card_option) == 0:
                print("Currently you have no suitable card to place try other things")
                break

            while True:
                try:
                    choice_index = int(input(f"{player.name}, choose a card (0-{len(card_option)-1}): "))
                    if 0 <= choice_index < len(card_option):
                        selected_card = card_option[choice_index]
                        
                        confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                        if confirmation == 'y':
                            player.play_area[1].append(selected_card)
                            player.hand.remove(selected_card)
                            print(f"{player.name} rides with {selected_card['name']}!")
                            player.grade_upgrade()
                            player.is_upgraded = True

                            break
                    else:
                        print("Invalid choice. Please enter a number within your hand's range.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            #Main
            print(f"\n--- Main Phase. ---")

            while True:
                player.show_playmat()
                user_input = input("Pick a Move (p: place card, m: move card, n: next phase): ").lower()

                print("new playmat", player.play_area)

                if user_input == "n":
                    break
                
                if user_input == "p":
                    print(player.play_area)
                    player_current_grade = player.get_current_grade()
                    map_grade = {0: [1, 0], 1: [2, 1], 2: [3, 2], 3: [3, 2]}

                    card_option = [card for card in player.hand if card["grade"] <= player_current_grade]

                    if card_option:
                        print("Current Options: ", card_option)
                    
                        while True:
                            try:
                                choice_index = int(input(f"{player.name}, choose a card (0-{len(card_option)-1}): "))
                                if 0 <= choice_index < len(card_option):
                                    selected_card = card_option[choice_index]
                                    
                                    position_index = int(input(f"{player.name}, choose a position to place the card: "))

                                    if position_index == 1:
                                        print("Cant ride again")
                                    else:
                                        if selected_card["grade"] <= player_current_grade:
                                            confirmation = input(f"Would you like to ride {selected_card['name']}? (y/n) ").lower()
                                            if confirmation == 'y':
                                                # if player.play_area[position_index]:
                                                #     discard = player.r1_circle.pop(0)
                                                #     player.drop_zone.append(discard)
                                                player.play_area[position_index].append(selected_card)
                                                player.hand.remove(selected_card)
                                                print(f"{player.name} rides with {selected_card['name']}!")
                                    break
                                else:
                                    print("Invalid choice. Please enter a number within your hand's range.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                    else:
                        print("Option empty")

                if user_input == "m":
                    position_index = int(input(f"{player.name}, choose a position to move the card: "))

                    movement_map = {0: 3, 3: 0, 2:5, 5:2}

                    if player.play_area[position_index]:
                        if not player.play_area[movement_map[position_index]]:
                            player.play_area[movement_map[position_index]].append(player.play_area[position_index].pop(0))
                        else:
                            moving = player.play_area[position_index].pop(0)
                            moving2 = player.play_area[movement_map[position_index]].pop(0)

                            player.play_area[position_index].append(moving2)
                            player.play_area[movement_map[position_index]].append(moving)
                    else:
                        print("Slot empty there is nothing to move")
                    
                    print(player.play_area)
         
                else:    
                    print("Select again something within the list")

                        
            player.show_playmat()
            os.system('cls')
            break

        #Battle        
        while True:
            
            value = []
            key = []

            map_attack ={}
            ##Current player who is attacking
            for i in range(len(player.card_active_tracker)):
                print(i)
                if player.play_area[i]:
                    player.card_active_tracker[i].append(i)

            opponent = [p for p in self.players if p != player][0]
    
            print(f"It's {player.name}'s turn. Opponent is {opponent.name}")

            
            for n in range(len(opponent.card_active_tracker)):
                print(n)
                if opponent.play_area[n]:
                    opponent.card_active_tracker[n].append(n)
      
            for n in opponent.card_active_tracker:
                if n:
                    value.append(opponent.card_active_tracker.index(n))
            
            for n in player.card_active_tracker:
                if n:
                    key.append(player.card_active_tracker.index(n))

            for i in range(len(key)):
                map_attack[key[i]] = value


            print("Possible attack combo: ", map_attack)


            position_index = int(input(f"{player.name}, choose a card to attack: "))    


            print("Attack complete")
        

            break
        print(player.card_active_tracker)
        
        print("Name: ", player.name)

        print(opponent.card_active_tracker)
        
        print("Name opponent: ", opponent.name)

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