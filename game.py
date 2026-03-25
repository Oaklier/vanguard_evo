import random
import os
from player import Player
from deck import Deck

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    def __init__(self):
        deck1 = Deck()
        deck2 = Deck()
        deck1.load_from_json("./testing_files/deck_1_test.json")
        deck2.load_from_json("./testing_files/deck_2_test.json")
        self.player1 = Player("Player 1", deck1)
        self.player2 = Player("Player 2", deck2)
        self.players = [self.player1, self.player2]
        self.current_player_index = 0
        self.game_status = True
        self.rzones_map = {"Front_Left" : "Back_Left", "Front_Right" : "Back_Right", "Back_Left" : "Front_Left", "Back_Right" : "Front_Right"}

    def handle_player_turn(self, player):
        player.is_upgraded = False
        self.stand_and_draw(player)
        self.ride_phase(player)
        self.main_phase(player)
        self.battle_phase(player)

    def get_current_player(self):
        return self.players[self.current_player_index]

    def _get_choice(self, prompt, options, allow_cancel=False):
        if not options:
            print("No options available.")
            return None

        while True:
            try:
                for idx, opt in enumerate(options):
                    name = opt.get('name', opt) if isinstance(opt, dict) else opt
                    print(f"[{idx}] {name}")
                
                msg = f"{prompt} (0-{len(options)-1})"
                if allow_cancel: msg += " or 'q' to cancel"
                
                choice = input(f"{msg}: ").lower()
                if allow_cancel and choice == 'q': return None
                
                idx = int(choice)
                if 0 <= idx < len(options):
                    return options[idx]
                print("Out of range.")
            except ValueError:
                print("Invalid input. Please enter a number.")


    def setup_game(self):
        print("\n--- Game Setup Phase ---")
        for player in self.players:
            starters = [c for c in player.deck.cards if c.grade == 0]
            
            if not starters:
                print(f"Error: {player.name} has no Grade 0 cards!")
                self.game_status = False 
                return

            print(f"\n{player.name}, select your starter:")
            selected = self._get_choice("Choose starter", starters)
            
            player.ride_vanguard(selected)
            player.deck.cards.remove(selected)

            player.shuffle_deck()
            player.draw_cards(5)
            player.show_board()

    def stand_and_draw(self, player):
        print(f"\n--- {player.name}: Stand & Draw Phase ---")
        player.draw_cards(1)

    def ride_phase(self, player):
        print(f"\n--- {player.name}: Ride Phase ---")
        current_vanguard = player.playmat.zones["VC"]
        
        valid_rides = [
            c for c in player.playmat.hand 
            if c.grade == current_vanguard.grade or c.grade == current_vanguard.grade + 1
        ]

        if not valid_rides:
            print("No valid units to Ride.")
            return

        selected = self._get_choice("Select a unit to Ride", valid_rides, allow_cancel=True)
        
        if selected:
            player.playmat.soul.append(current_vanguard)
            player.playmat.zones["VC"] = selected
            player.playmat.hand.remove(selected)
            print(f"{player.name} RIDES {selected.name}! ✨")

    def main_phase(self, player):
        print(f"\n--- {player.name}: Main Phase ---")
        
        while True:
            current_grade = player.playmat.zones["VC"].grade
            valid_calls = [c for c in player.playmat.hand if c.grade <= current_grade]

            if not valid_calls:
                print("No more valid units to call.")
                break

            print("\nYour current field:")
            player.show_board()
            
            unit = self._get_choice("Select unit to CALL to Rear-guard", valid_calls, allow_cancel=True)
            if not unit: break 

            rg_zones = ["Front_Left", "Front_Right", "Back_Left", "Back_Center", "Back_Right"]
            zone_name = self._get_choice("Select a circle to place the unit", rg_zones)

            player.call_rear_guard(player, unit, zone_name, self.rzones_map)

    def battle_phase(self, player):
        print(f"\n--- {player.name}: Battle Phase ---")
 
    def switch_player(self):
        self.current_player_index = 0 if self.current_player_index == 1 else 1

    def run_game(self):
        clear_terminal()
        self.setup_game() 

        self.current_player_index = random.randint(0, 1)
        print(f"\n{self.get_current_player().name} wins the coin toss!")

        while self.game_status:
            current_player = self.get_current_player()
        
            self.handle_player_turn(current_player)
            
            if self.player1.is_defeated() or self.player2.is_defeated():
                self.game_status = False
                break 
                
            self.switch_player()
            clear_terminal()

        if self.player1.is_defeated():
            print(f"\n WINNER: {self.player2.name}!")
        else:
            print(f"\n WINNER: {self.player1.name}!")
