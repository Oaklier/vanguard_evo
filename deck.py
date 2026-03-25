import json
import os

class Card:
    def __init__(self, name, grade,power, trigger=None):
        self.name = name
        self.grade = grade
        self.power = power
        self.trigger = trigger

    def __repr__(self):
        trigger_info = f" [{self.trigger}]" if self.trigger else ""
        return f"{self.name} ({self.grade}){trigger_info}"

class Deck:
    def __init__(self):
        self.cards = []

    def load_from_json(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        for item in data['deck']:
            create_card = Card(
                name=item['name'],
                grade=item['grade'],
                power=item['power'],
                trigger=item.get('trigger')
            )
            
            for i in range(item['count']):
                self.cards.append(create_card)

    def check_cards(self):
        return len(self.cards)
    
def main():
    json_data_path = "./testing_files/deck_1_test.json"
    
    if not os.path.exists(json_data_path):
        print(f"Error: File not found at {json_data_path}")
        return
    
    deck = Deck()
    deck.load_from_json(json_data_path)

    print(deck.check_cards())

if __name__ == "__main__":
    main()