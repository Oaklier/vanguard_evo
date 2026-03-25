from playmat import Playmat
import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck  
        self.playmat = Playmat() 

    def draw_cards(self, count):
        for _ in range(count):
            if self.deck.cards:
                card = self.deck.cards.pop(0)
                self.playmat.hand.append(card)

        print(f"{self.name}'s drew {count} cards.")
    
    def shuffle_deck(self):
        random.shuffle(self.deck.cards)
        print(f"{self.name}'s deck shuffled.")

    def ride_vanguard(self, card):
        if self.playmat.zones["VC"]:
            self.playmat.soul.append(self.playmat.zones["VC"])
        
        self.playmat.zones["VC"] = card
        print(f"{self.name} Rides {card.name}!")

    def call_rear_guard(self, player, unit, zone_name, zone_map):
            if player.playmat.zones[zone_name] == None:
                player.playmat.zones[zone_name] = unit
                print(f"Called {unit.name} to {zone_name}!")

            else:
                if player.playmat.zones[zone_map.get(zone_name)] == None:
                    player.playmat.zones[zone_map.get(zone_name)] = player.playmat.zones[zone_name]
                    player.playmat.zones[zone_name] = unit
                    print(f"Called {unit.name} to {zone_name} and move {zone_map.get(zone_name)} to the rear gaurd!")
                else: 
                    
                    current_unit =  player.playmat.zones[zone_name]
                    player.playmat.drop_zone.append(current_unit)
                    player.playmat.zones[zone_name] = unit
                    print(f"Called {unit.name} to {zone_name}!")

                    print(f"Called {current_unit} to Drop zone!")

            player.playmat.hand.remove(unit)

    def show_board(self):
        self.playmat.display(self)

    def is_defeated(self):
        return len(self.playmat.damage_zone) >= 6 or len(self.deck.cards) == 0
