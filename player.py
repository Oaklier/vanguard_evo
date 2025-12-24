import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.damage_zone = []
        self.hand = []
        self.deck = deck
        self.drop_zone = []
        self.v_circle = []    
        self.r1_circle = [{'name': 'Dragon Monk, Gojo', 'grade': 1}]
        self.r2_circle = []
        self.r3_circle = []
        self.r4_crircle = []
        self.r5_circle = []
        self.grade = 0
        self.is_upgraded = False
        self.step = 0

    def card_count(self, item):
        return len(item)
    
    def get_current_grade(self): 
        return self.grade
    
    def grade_upgrade(self):
        self.grade += 1
        print("Successfully Upgrade!!!")

    def get_card_info(self, search, location):
        return [card[search] for card in location]

    def show_hand(self):
        return self.hand

    def draw_cards(self, num_cards = 1):
        drawn_cards = []

        for _ in range(num_cards):
            card = self.deck.pop(0)
            if card:
                self.hand.append(card)
                drawn_cards.append(card)
            else:
                print(f"{self.name}'s deck is empty! Cannot draw more cards.")
                break
        if drawn_cards:
            print(f"{self.name} drew: {[str(c) for c in drawn_cards]}")
        return drawn_cards
    
    def show_field(self, circle):
        if self.vangaurd_circle:
            print(f"{self.name}'s field: {[str(card) for card in circle]}")
        else:
            print(f"{self.name}'s field is empty.")

    def play_card_to_field(self, card_index, circle):
        if 0 <= card_index < len(self.deck):
            card = self.deck.pop(card_index)
            circle.append(card)
            # self.vangaurd_circle.append(card)
            print(f"{self.name} played {card} to the field.")
            return card
        else:
            print("Invalid card index to play.")
            return None

    def shuffle_cards(self, cards):
        shuffled_cards = random.shuffle(cards)
        return shuffled_cards 
    
    def is_defeated(self):
        return len(self.damage_zone) >= 6 or len(self.deck) <= 0
    
    def show_playmat(self):
        """Playmat"""

        print(f"""
        \t\t\t[]
        \t\t\tcount:

        \t\t[{self.get_card_info("name", self.r1_circle)}] \t[{self.get_card_info("name", self.v_circle)}] \t[{self.get_card_info("name", self.r2_circle)}] \t[Deck]
        \t\tcount:{self.card_count(self.r1_circle)}  \tv_count:{self.card_count(self.v_circle)} \tcount:{self.card_count(self.r2_circle)}  \tcount: {self.card_count(self.deck)}

        \t[Damage Zone]\t[{self.get_card_info("name", self.r3_circle)}] \t[{self.get_card_info("name", self.r4_crircle)}] \t[{self.get_card_info("name", self.r5_circle)}]\t[Drop Zone]
        count:{self.card_count(self.damage_zone)}\tcount:{self.card_count(self.r3_circle)} count:{self.card_count(self.r4_crircle)} count:{self.card_count(self.r5_circle)} \tcount:{self.card_count(self.drop_zone)}

        [{self.show_hand()}]
        h_count: {self.card_count(self.show_hand())}
        """)