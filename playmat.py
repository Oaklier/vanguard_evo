import textwrap

class Playmat:
    def __init__(self):
        self.zones = {
            "Front_Left": None, "VC": None, "Front_Right": None,
            "Back_Left": None, "Back_Center": None, "Back_Right": None
        }
        self.hand = []
        self.damage_zone = []
        self.drop_zone = []
        self.soul = []

    def _get_zone_lines(self, zone_key):
        card = self.zones[zone_key]
        if not card:
            # 14 characters of content
            return [f"{'[ Empty ]':^14}", f"{' ':^14}", f"{' ':^14}"]
        
        # All lines forced to 14 characters
        name_line = f"{card.name[:14]:^14}"
        trig = f"|{card.trigger[:4]}" if card.trigger else ""
        info_line = f"G{card.grade}{trig:^6}" 
        power_line = f"P: {card.power:^10}"
        
        return [name_line, f"{info_line:^14}", f"{power_line:^14}"]
    
    def display(self, player):
        # Prepare Field Data (14 chars content + 2 spaces = 16 total per zone)
        fl, vc, fr = self._get_zone_lines("Front_Left"), self._get_zone_lines("VC"), self._get_zone_lines("Front_Right")
        bl, bc, br = self._get_zone_lines("Back_Left"), self._get_zone_lines("Back_Center"), self._get_zone_lines("Back_Right")

        # Prepare Damage Zone (exactly 12 chars wide)
        dmg = [f"{c.name[:10]:^10}" for c in self.damage_zone[-3:]]
        while len(dmg) < 3: dmg.insert(0, "  --  ")

        print("\n" + "="*77)
        print(f" PLAYER: {player.name.upper()} ".center(77, "="))
        print("="*77)

        # Row 1: Front Row + Damage + Deck
        print(f" [DAMAGE]   | {fl[0]} | {vc[0]} | {fr[0]} |  [ DECK ] ")
        print(f" {dmg[0]:^10} | {fl[1]} | {vc[1]} | {fr[1]} |  Cards: {len(player.deck.cards):<3}")
        print(f" {dmg[1]:^10} | {fl[2]} | {vc[2]} | {fr[2]} |            ")
        
        # Divider Row
        print(f" {dmg[2]:^10} |{'-'*16}|{'-'*16}|{'-'*16}|  [ DROP ] ")
        
        # Row 2: Back Row + Drop + Soul
        print(f"            | {bl[0]} | {bc[0]} | {br[0]} |  Cards: {len(self.drop_zone):<3}")
        # --- SOUL COUNT ADDED BELOW ---
        print(f"   TOTAL    | {bl[1]} | {bc[1]} | {br[1]} |  Soul: {len(self.soul):<3} ")
        print(f"  DMG: {len(self.damage_zone):<2}   | {bl[2]} | {bc[2]} | {br[2]} |            ")
        print("="*77)

        # Hand Section
        print(f" HAND ({len(self.hand)}):")
        if not self.hand:
            print(" [ Empty ]")
        else:
            hand_str = " | ".join([f"[{i}] {c.name}(G{c.grade})" for i, c in enumerate(self.hand)])
            print(textwrap.fill(hand_str, width=77))
        print("="*77 + "\n")