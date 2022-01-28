import imp
import os
from queue import PriorityQueue
import sys
import time

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
            total -= 11
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
            x = slowinput("Do you want to hit or stand? (h/s) ", "white")
            if x == "h":
                y = self.hit(deck)
                if y == False:
                    return False
                return True
            elif x == "s":
                return False
            else:
                slowprint("Please enter h or s", "red")

    def chips_value(self):
        slowprint("You have {} chips".format(self.chips),"blue")

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
        slowprint("Player hand: {} (value: {})".format(self.player.hand.hand_cards(), self.player.hand.real_value_calculator()), "yellow")
        slowprint("Dealer showing: {} (value: {})".format(self.dealer.hand.hand_cards_hidden(), self.dealer.hand.hand_value_hidden()), "magenta")

    def show_cards_all_revealed(self):
        slowprint("Player hand: {} (value: {})".format(self.player.hand.hand_cards(), self.player.hand.real_value_calculator()), "yellow")
        slowprint("Dealer hand: {} (value: {})".format(self.dealer.hand.hand_cards(), self.dealer.hand.real_value_calculator()), "magenta")

    def player_turn(self):
        return self.player.hit_or_stand(self.deck)

    def dealer_turn(self):
        return self.dealer.hit_or_stand(self.deck)

    def deck_plus_hidden(self):
        temp_deck = deck()
        temp_deck.cards = []
        for card in self.deck.cards:
            temp_deck.cards.append(card)
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
            probabilities[key] = round(values[key] / len(mydeck.cards), 4)*100
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
        return round(total_hit, 2)

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
        return round(total_bust, 2)

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
        return round(total_better, 2)

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
        return round(total_bust*100, 2)
    
    

        

                
def slowprint(s, color):
    # change the color
    if color == "red":
        print("\033[91m", end="")
    elif color == "green":
        print("\033[92m", end="")
    elif color == "yellow":
        print("\033[93m", end="")
    elif color == "blue":
        print("\033[94m", end="")
    elif color == "magenta":
        print("\033[95m", end="")
    elif color == "cyan":
        print("\033[96m", end="")
    elif color == "white":
        print("\033[97m", end="")
    elif color == "black":
        print("\033[90m", end="")
    elif color == "reset":
        print("\033[0m", end="")
    # print the string
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    sys.stdout.write('\n')
        
def slowinput(s, color):
    slowprint(s, color)
    return input()


def reset_color():
    print("\033[0m", end="")

    
def take_bet(chips):
    while True:
        try:
            chip = int(slowinput("How many chips would you like to bet? ", "white"))
        except:
            slowprint("Please enter an integer", "white")
        else:
            if chip > chips:
                slowprint("You don't have enough chips", "red")
            else:
                return chip

def main(game_instance):
    game_instance.deck.shuffle()
    while True:
        game_instance.player.chips_value()
        bet = take_bet(game_instance.player.chips)
        game_instance.deal_cards()
        game_instance.show_cards_all_hidden()
        if game_instance.player.hand.real_value_calculator() == 21:
            slowprint("BLACKJACK!", "green")
        else:
            slowprint("{}".format(game_instance.p1()), "blue")
            slowprint("The dealer has a {}% chance of hitting".format(game_instance.p2()), "blue")
            slowprint("You have a {}% chance of busting if you hit".format(game_instance.p3()), "blue")
            slowprint("Your hand is better than the dealers {}% of the time".format(game_instance.p4()), "blue")
            slowprint("The dealer has a {}% chance of busting if they hit".format(game_instance.p5()), "blue")
            h = game_instance.player_turn()
            while h:
                game_instance.show_cards_all_hidden()
                if game_instance.player.hand.real_value_calculator() > 21:
                    slowprint("You busted!", "red")
                    break
                elif game_instance.player.hand.real_value_calculator() == 21:
                    slowprint("BLACKJACK!", "green")
                    break
                slowprint("You have a {}% chance of busting if you hit".format(game_instance.p3()), "blue")
                slowprint("Your hand is better than the dealers {}% of the time".format(game_instance.p4()),   "blue")
                slowprint("The dealer has a {}% chance of busting if they hit".format(game_instance.p5()), "blue")
                h = game_instance.player_turn()
       

        
        if game_instance.player.hand.real_value_calculator() == 21:
            game_instance.show_cards_all_revealed()
            game_instance.player.chips += bet
            slowprint("You won {} chips".format(bet), "green")
        else:
            j = game_instance.dealer_turn()
            while j:
                if game_instance.dealer.hand.real_value_calculator() > 21:
                    slowprint("Dealer busted!", "green")
                    break
                j = game_instance.dealer_turn()
            game_instance.show_cards_all_revealed()
            if game_instance.player.hand.real_value_calculator() == game_instance.dealer.hand.real_value_calculator() < 21:
                slowprint("It's a tie!", "yellow")
            elif game_instance.player.hand.real_value_calculator() > 21:
                game_instance.player.chips -= bet
                slowprint("You lost {} chips".format(bet), "red")
            elif game_instance.dealer.hand.real_value_calculator() > 21:
                game_instance.player.chips += bet
                slowprint("You won {} chips".format(bet), "green")
            elif game_instance.player.hand.real_value_calculator() > game_instance.dealer.hand.real_value_calculator():
                game_instance.player.chips += bet
                slowprint("You won {} chips".format(bet), "green")
            else:
                game_instance.player.chips -= bet
                slowprint("You lost {} chips".format(bet), "red")

        if game_instance.player.chips <= 0:
            slowprint("You are out of chips", "red")
            print("\033[0m", end="")
            update_save(game_instance.player.chips)
            break
        else:
            x = slowinput("Do you want to play again? (y/n) ", "white")
            if x == "y":
                game_instance.player.hand.empty_hand()
                game_instance.dealer.hand.empty_hand()
                game_instance.deck = deck()
                game_instance.deck.shuffle()
                continue
            else:
                slowprint("You have {} chips".format(game_instance.player.chips), "blue")
                # save the chips to a file named save.txt
                print("\033[0m", end="")
                update_save(game_instance.player.chips)
                break

        

slowprint("Welcome to Blackjack!", "magenta")
slowprint("The goal of the game is to get as close to 21 as possible without going over", "magenta")
name = slowinput("What is your name?", "white")
# check if there is a save file and if there is load the chips
if os.path.isfile("save.txt"):
    with open("save.txt", "r") as f:
        saves = f.read()

saveslib = {

}
if len(saves) > 0:
    saves = saves.split("\n")
    for line in saves:
        if line != "":
            line = line.split(",")
            saveslib[line[0]] = int(line[1])

if name in saveslib:
    slowprint("Welcome back {}!".format(name), "magenta")
    chips = saveslib[name]
else:
    slowprint("Hello {}!".format(name), "magenta")
    saveslib[name] = 100
    chips = saveslib[name]

def write_save():
    with open("save.txt", "w") as f:
        for line in saveslib:
            f.write(line + "," + str(saveslib[line]) + "\n")

def update_save(chips):
    saveslib[name] = chips
    write_save()

if chips <= 0:
    chips = 100

main(game(chips))









