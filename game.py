from player import Player

deck = [
 [
    # Grade 3 (2 cards)
    'Dragonic Overlord',
    'Dragonic Overlord',
    
    # Grade 3 (1 card)
    'Dragon Monk, Goku',
    
    # Grade 3 (4 cards)
    'Demonic Dragon Berserker, Yaksha',
    'Demonic Dragon Berserker, Yaksha',
    'Demonic Dragon Berserker, Yaksha',
    'Demonic Dragon Berserker, Yaksha',
    
    # Grade 2 (4 cards)
    'Dragon Knight, Nehalem',
    'Dragon Knight, Nehalem',
    'Dragon Knight, Nehalem',
    'Dragon Knight, Nehalem',
    
    # Grade 2 (4 cards)
    'Berserk Dragon',
    'Berserk Dragon',
    'Berserk Dragon',
    'Berserk Dragon',
    
    # Grade 2 (4 cards)
    'Wyvern Strike, Tejas',
    'Wyvern Strike, Tejas',
    'Wyvern Strike, Tejas',
    'Wyvern Strike, Tejas',
    
    # Grade 1 (4 cards)
    'Embodiment of Armor, Bahr',
    'Embodiment of Armor, Bahr',
    'Embodiment of Armor, Bahr',
    'Embodiment of Armor, Bahr',
    
    # Grade 1 (2 cards)
    'Dragon Monk, Gojo',
    'Dragon Monk, Gojo',
    
    # Grade 1 (4 cards)
    'Flame of Hope, Aermo',
    'Flame of Hope, Aermo',
    'Flame of Hope, Aermo',
    'Flame of Hope, Aermo',
    
    # Grade 1 (2 cards)
    'Demonic Dragon Madonna, Joka',
    'Demonic Dragon Madonna, Joka',
    
    # Grade 1 (2 cards)
    'Wyvern Strike, Jarran',
    'Wyvern Strike, Jarran',
    
    # Grade 0 (1 card)
    'Lizard Runner, Undeux',
    
    # Grade 0 - Draw Trigger (4 cards)
    'Dragon Dancer, Monica',
    'Dragon Dancer, Monica',
    'Dragon Dancer, Monica',
    'Dragon Dancer, Monica',
    
    # Grade 0 - Stand Trigger (4 cards)
    'Lizard Soldier, Ganlu',
    'Lizard Soldier, Ganlu',
    'Lizard Soldier, Ganlu',
    'Lizard Soldier, Ganlu',
    
    # Grade 0 - Heal Trigger (4 cards)
    'Dragon Monk, Genjo',
    'Dragon Monk, Genjo',
    'Dragon Monk, Genjo',
    'Dragon Monk, Genjo',
    
    # Grade 0 - Critical Trigger (4 cards)
    'Demonic Dragon Mage, Rakshasa',
    'Demonic Dragon Mage, Rakshasa',
    'Demonic Dragon Mage, Rakshasa',
    'Demonic Dragon Mage, Rakshasa',
],

[
    # Grade 3 (4 cards)
    'Crimson Butterfly, Brigitte',
    'Crimson Butterfly, Brigitte',
    'Crimson Butterfly, Brigitte',
    'Crimson Butterfly, Brigitte',
    
    # Grade 3 (1 card)
    'Knight of Conviction, Bors',
    
    # # Grade 3 (2 cards)
    'Solitary Knight, Gancelot',
    # 'Solitary Knight, Gancelot',
    
    # Grade 2 (4 cards)
    'Knight of Silence, Gallatin',
    'Knight of Silence, Gallatin',
    'Knight of Silence, Gallatin',
    'Knight of Silence, Gallatin',
    
    # Grade 2 (1 card)
    'Blaster Blade',
    
    # Grade 2 (3 cards)
    'Knight of the Harp, Tristan',
    'Knight of the Harp, Tristan',
    'Knight of the Harp, Tristan',
    
    # Grade 2 (4 cards)
    'Covenant Knight, Randolf',
    'Covenant Knight, Randolf',
    'Covenant Knight, Randolf',
    'Covenant Knight, Randolf',
    
    # Grade 1 (4 cards)
    'Little Sage, Marron',
    'Little Sage, Marron',
    'Little Sage, Marron',
    'Little Sage, Marron',
    
    # Grade 1 (2 cards)
    'Wingal',
    'Wingal',
    
    # Grade 1 (4 cards)
    'Starlight Unicorn',
    'Starlight Unicorn',
    'Starlight Unicorn',
    'Starlight Unicorn',
    
    # Grade 1 (4 cards)
    'Knight of Rose, Morgana',
    'Knight of Rose, Morgana',
    'Knight of Rose, Morgana',
    'Knight of Rose, Morgana',
    
    # Grade 0 (1 card)
    'Stardust Trumpeter',
    
    # Grade 0 - Critical Trigger (4 cards)
    'Bringer of Good Luck, Epona',
    'Bringer of Good Luck, Epona',
    'Bringer of Good Luck, Epona',
    'Bringer of Good Luck, Epona',
    
    # Grade 0 - Heal Trigger (4 cards)
    'Yggdrasil Maiden, Elaine',
    'Yggdrasil Maiden, Elaine',
    'Yggdrasil Maiden, Elaine',
    'Yggdrasil Maiden, Elaine',
    
    # Grade 0 - Draw Trigger (4 cards)
    'Weapons Dealer, Govannon',
    'Weapons Dealer, Govannon',
    'Weapons Dealer, Govannon',
    'Weapons Dealer, Govannon',
    
    # Grade 0 - Stand Trigger (4 cards)
    'Flogal',
    'Flogal',
    'Flogal',
    'Flogal',

        ]

]

class Game:
    def __init__(self):
        self.player1 = Player("Player_1", deck[0])
        self.player2 = Player("Player_2", deck[1])
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