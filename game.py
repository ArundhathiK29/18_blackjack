from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def round(self, bet):
        deck = Deck()
        player = []
        dealer = []

        for _ in range(2):
            card = deck.draw()
            if card is not None:
                player.append(card)

        for _ in range(2):
            card = deck.draw()
            if card is not None:
                dealer.append(card)

        self.show(player, dealer)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Natural blackjack
        if pv == 21 and len(player) == 2:
            self.show(player, dealer, hide=False)

            if dv == 21 and len(dealer) == 2:
                print("Push.")
            else:
                winnings = bet * 3 // 2
                self.chips += winnings
                print("Blackjack! Player wins.")
            return True

        if dv == 21 and len(dealer) == 2:
            self.chips -= bet
            self.show(player, dealer, hide=False)
            print("Dealer blackjack. Dealer wins.")
            return True

        # Player turn
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()

            if key == "q":
                return False
            if key == "s":
                break
            if key == "h":
                card = deck.draw()
                if card is None:
                    break

                player.append(card)
                self.show(player, dealer)

                if hand_value(player) > 21:
                    self.chips -= bet
                    print("Bust.")
                    return True
            else:
                print("Invalid choice.")

        # Dealer turn
        while hand_value(dealer) < 17:
            card = deck.draw()
            if card is None:
                break
            dealer.append(card)

        self.show(player, dealer, hide=False)

        pv = hand_value(player)
        dv = hand_value(dealer)

        if dv > 21 or pv > dv:
            self.chips += bet
            print("Player wins.")
        elif pv < dv:
            self.chips -= bet
            print("Dealer wins.")
        else:
            print("Push.")

        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)

        while self.chips > 0:
            while True:
                entry = input(f"Chips: {self.chips}. Bet: ").strip().lower()

                if entry == "q":
                    return

                try:
                    bet = int(entry)
                    if 1 <= bet <= self.chips:
                        break
                except ValueError:
                    pass

                print("Invalid bet.")

            if not self.round(bet):
                return

            print("Chips:", self.chips)

            if self.chips == 0:
                print("Out of chips. Game over.")
                return

            if input("Play again? [y/n]: ").strip().lower() != "y":
                return