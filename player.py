import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.damage_zone = []
        self.hand = []
        self.deck = deck
        self.drop_zone = []
        self.grade = 0
        self.is_upgraded = False
        self.step = 0
        self.play_area = [[], [], [],
                        [], [], [] ]

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

    def shuffle_cards(self, cards):
        shuffled_cards = random.shuffle(cards)
        return shuffled_cards 
    
    def is_defeated(self):
        return len(self.damage_zone) >= 6 or len(self.deck) <= 0
    
    def show_playmat(self):
        """Playmat"""

        print(f"""

        \t\t[{self.get_card_info("name", self.play_area[0])}] \t[{self.get_card_info("name", self.play_area[1])}] \t[{self.get_card_info("name", self.play_area[2])}] \t[Deck]
        \t\tcount:{self.card_count(self.play_area[0])}  \tv_count:{self.card_count(self.play_area[1])} \tcount:{self.card_count(self.play_area[2])}  \tcount: {self.card_count(self.deck)}

        \t[Damage Zone]\t[{self.get_card_info("name", self.play_area[3])}] \t[{self.get_card_info("name", self.play_area[4])}] \t[{self.get_card_info("name", self.play_area[5])}]\t[Drop Zone]
        count:{self.card_count(self.damage_zone)}\tcount:{self.card_count(self.play_area[3])} count:{self.card_count(self.play_area[4])} count:{self.card_count(self.play_area[5])} \tcount:{self.card_count(self.drop_zone)}

        [{self.show_hand()}]
        h_count: {self.card_count(self.show_hand())}
        """)