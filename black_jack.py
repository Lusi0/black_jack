import os

class card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
    
    def __str__(self):
        return self.rank + " of " + self.suit

# Create a deck of cards
class deck:
    def __init__(self):
        self.cards = []
        for suit in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for rank in ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]:
                if rank == "Jack":
                    self.cards.append(card(suit, rank, 10))
                elif rank == "Queen":
                    self.cards.append(card(suit, rank, 10))
                elif rank == "King":
                    self.cards.append(card(suit, rank, 10))
                elif rank == "Ace":
                    self.cards.append(card(suit, rank, "special"))
                else:
                    self.cards.append(card(suit, rank, int(rank)))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def __str__(self):
        return str(self.cards)



class hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.value == "special":
            self.aces += 1
        else:
            self.value += card.value
        if self.real_value_calculator() > 21:
            return False
        
    def empty_hand(self):
        self.cards = []
        self.value = 0
        self.aces = 0


    def real_value_calculator(self):
        total = self.value
        total += 11 * self.aces
        while total > 21 and self.aces > 0:
            total -= 10
            self.aces -= 1
        return total
    

    def __str__(self):
        return str(self.cards)

    def hand_value(self):
        return self.value
    
    def hand_cards(self):
        cards_legable = []
        for card in self.cards:
            cards_legable.append(card.__str__())
        return cards_legable

class hand_dealer(hand):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self):
        return str(self.cards)

    def hand_cards_hidden(self):
        # return all cards in self.cards except the first one
        cards_legable = []
        for card in self.cards[1:]:
            cards_legable.append(card.__str__())
        return cards_legable

    def hand_value_hidden(self):
        total = self.value
        total += 11 * self.aces


        myaces = self.aces
        if self.cards[0].value == "special":
            myaces -= 1
        while total > 21 and myaces > 0:
            total -= 10
            myaces -= 1
        if self.cards[0].value == "special":
            return total
        else:
            return total - self.cards[0].value
    
    def hand_shown(self):
        # return all cards after the first one
        cards_legable = []
        for card in self.cards[1:]:
            cards_legable.append(card)
        return cards_legable



class player:
    def __init__(self,chips):
        self.hand = hand()
        self.chips = chips

    def hit(self, deck):
        self.hand.add_card(deck.deal())
    
    def hit_or_stand(self, deck):
        while True:
            x = input("Do you want to hit or stand? (h/s) ")
            if x == "h":
                y = self.hit(deck)
                if y == False:
                    return False
                return True
            elif x == "s":
                return False
            else:
                print("Please enter h or s")

    def chips_value(self):
        print("You have {} chips".format(self.chips))

    def __str__(self):
        return "Player hand: {}".format(self.hand.hand_cards())
    

class dealer:
    def __init__(self, hitunder):
        self.hand = hand_dealer()
        self.hitunder = hitunder

    def hit(self, deck):
        self.hand.add_card(deck.deal())

    def hit_or_stand(self, deck):
        while True:
            if self.hand.real_value_calculator() < self.hitunder:
                self.hit(deck)
                return True
            else:
                return False

    def __str__(self):
        return "Dealer hand: {}".format(self.hand.hand_cards())


class game:
    def __init__(self, chips):
        self.deck = deck()
        self.player = player(chips)
        self.dealer = dealer(17)
        
    def deal_cards(self):
        self.player.hit(self.deck)
        self.player.hit(self.deck)
        self.dealer.hit(self.deck)
        self.dealer.hit(self.deck)
    
    def show_cards_all_hidden(self):
        print("Player hand: {} (value: {})".format(self.player.hand.hand_cards(), self.player.hand.real_value_calculator()))
        print("Dealer showing: {} (value: {})".format(self.dealer.hand.hand_cards_hidden(), self.dealer.hand.hand_value_hidden()))

    def show_cards_all_revealed(self):
        print("Player hand: {} (value: {})".format(self.player.hand.hand_cards(), self.player.hand.real_value_calculator()))
        print("Dealer hand: {} (value: {})".format(self.dealer.hand.hand_cards(), self.dealer.hand.real_value_calculator()))

    def player_turn(self):
        return self.player.hit_or_stand(self.deck)

    def dealer_turn(self):
        return self.dealer.hit_or_stand(self.deck)

    def deck_plus_hidden(self):
        temp_deck = deck()
        temp_deck.cards = self.deck.cards
        temp_deck.cards.append(self.dealer.hand.cards[0])
        return temp_deck
    
    def p1(self):
        # probability of drawing each card
        values = {

        }
        mydeck = self.deck_plus_hidden()
        for card in mydeck.cards:
            if card.value in values:
                values[card.value] += 1
            else:
                values[card.value] = 1
        probabilities = {}
        for key in values:
            probabilities[key] = round(values[key] / len(mydeck.cards), 5)*100
        return probabilities

    def p2(self):
        # probability that the dealer will hit
        pro = self.p1()
        hit_under = self.dealer.hitunder
        value_showing = self.dealer.hand.hand_value_hidden()
        total_hit = 0
        for key in pro:
            if key == "special":
                if 11 + value_showing <= hit_under:
                    total_hit += pro[key]
            elif int(key) + value_showing < hit_under:
                total_hit += pro[key]
        return round(total_hit, 3)

    def p3(self):
        # probability you will bust if you hit
        pro = self.p1()
        hand_value = self.player.hand.real_value_calculator()
        total_bust = 0
        for key in pro:
            if key == "special":
                if 1 + hand_value > 21:
                    total_bust += pro[key]
            elif int(key) + hand_value > 21:
                total_bust += pro[key]
        return round(total_bust, 3)

    def p4(self):
        # probability your hand is better than the dealers
        pro = self.p1()
        hand_value = self.player.hand.real_value_calculator()
        dealer_value = self.dealer.hand.hand_value_hidden()
        total_better = 0
        for key in pro:
            if key == "special":
                if hand_value > dealer_value + 11:
                    total_better += pro[key]
            elif int(key) + dealer_value < hand_value:
                total_better += pro[key]
        return round(total_better, 3)

    def p5(self):
        # what is the probability that the dealer will bust if they hit
        pro = self.p1()
        pro_2d = {

        }
        for key in pro:
            temp = pro 
            if temp[key]/100 - 1/len(self.deck_plus_hidden().cards) > 0:
                temp[key] = temp[key]/100
                temp[key] -= 1/len(self.deck_plus_hidden().cards)

            pro_2d[key] = temp
        total_bust = 0
        for key_lib in pro_2d:
            for key in pro_2d[key_lib]:
                if key_lib == "special":
                    if key == "special":
                        if 1 + 1 + self.dealer.hand.hand_value_hidden() > 21:
                            total_bust += pro_2d[key_lib][key] * pro[key_lib]
                    elif int(key) + 1 + self.dealer.hand.hand_value_hidden() > 21:
                        total_bust += pro_2d[key_lib][key] * pro[key_lib]
                elif key == "special":
                    if 1 + int(key_lib) + self.dealer.hand.hand_value_hidden() > 21:
                        total_bust += pro_2d[key_lib][key] * pro[key_lib]
                elif int(key) + int(key_lib) + self.dealer.hand.hand_value_hidden() > 21:
                    total_bust += pro_2d[key_lib][key] * pro[key_lib]
        return round(total_bust*100, 3)
    

        

                

        



    
def take_bet(chips):
    while True:
        try:
            chip = int(input("How many chips would you like to bet? "))
        except:
            print("Please enter an integer")
        else:
            if chip > chips:
                print("You don't have enough chips")
            else:
                return chip

def main(game_instance):
    game_instance.deck.shuffle()
    while True:
        game_instance.player.chips_value()
        bet = take_bet(game_instance.player.chips)
        game_instance.deal_cards()
        game_instance.show_cards_all_hidden()
        print(game_instance.p1())
        print("The dealer has a {}% chance of hitting".format(game_instance.p2()))
        print("You have a {}% chance of busting if you hit".format(game_instance.p3()))
        print("Your hand is better than the dealers {}% of the time".format(game_instance.p4()))
        print("The dealer has a {}% chance of busting if they hit".format(game_instance.p5()))
        h = game_instance.player_turn()
        while h:
            game_instance.show_cards_all_hidden()
            if game_instance.player.hand.real_value_calculator() > 21:
                print("You busted!")
                break
            print("You have a {}% chance of busting if you hit".format(game_instance.p3()))
            print("Your hand is better than the dealers {}% of the time".format(game_instance.p4()))
            print("The dealer has a {}% chance of busting if they hit".format(game_instance.p5()))
            h = game_instance.player_turn()
       

            
        if game_instance.player.hand.real_value_calculator() == 21:
            game_instance.show_cards_all_revealed()
            game_instance.player.chips += bet
            print("You won {} chips".format(bet))
        elif game_instance.player.hand.real_value_calculator() < 21:
            j = game_instance.dealer_turn()
            while j:
                if game_instance.dealer.hand.real_value_calculator() > 21:
                    print("Dealer busted!")
                    break
                j = game_instance.dealer_turn()
            game_instance.show_cards_all_revealed()
        elif game_instance.player.hand.real_value_calculator() > 21:
            game_instance.player.chips -= bet
            print("You lost {} chips".format(bet))
        elif game_instance.dealer.hand.real_value_calculator() > 21:
            game_instance.player.chips += bet
            print("You won {} chips".format(bet))
        elif game_instance.player.hand.real_value_calculator() > game_instance.dealer.hand.real_value_calculator():
            game_instance.player.chips += bet
            print("You won {} chips".format(bet))
        else:
            game_instance.player.chips -= bet
            print("You lost {} chips".format(bet))

        if game_instance.player.chips <= 0:
            print("You are out of chips")
            with open("save.txt", "w") as f:
                    f.write(str(game_instance.player.chips))
            break
        else:
            x = input("Do you want to play again? (y/n) ")
            if x == "y":
                game_instance.player.hand.empty_hand()
                game_instance.dealer.hand.empty_hand()
                game_instance.deck = deck()
                game_instance.deck.shuffle()
                continue
            else:
                print("You have {} chips".format(game_instance.player.chips))
                # save the chips to a file named save.txt
                with open("save.txt", "w") as f:
                    f.write(str(game_instance.player.chips))
                break

        


# check if there is a save file and if there is load the chips
chips = 100
if os.path.isfile("save.txt"):
    with open("save.txt", "r") as f:
        chips = int(f.read())

if chips <= 0:
    chips = 100

main(game(chips))









