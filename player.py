import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.damage_zone = []
        self.hand = []
        self.deck = deck
        self.vangaurd_circle = []    
        self.r1_circle = []

    def show_hand(self):
        if self.hand:
            print(self.hand)
        else:
            print("Hand is Empty")

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