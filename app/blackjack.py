import random

def pick_card():
    num = random.randint(2, 14)
    if (num <= 10):
        return str(num)
    if (num == 11):
        return "J"
    if (num == 12):
        return "Q"
    if (num == 13):
        return "K"
    return "A"

def find_value(card, total):
    if (card in ["J", "Q", "K"]):
        return 10
    if (card == "A"):
        if total + 11 > 21:
            return 1
        else:
            return 11
    return int(card)

# def bet():
#     b = input("How much do you want to bet? ")
#     return int(b)

def add(card1, card2, total):
    total += find_value(card1, total)
    total += find_value(card2, total)
    return total

def pick(player_total):
    print("Do you want to hit or stand?")
    while True:
        choice = input("Type 'hit' to hit or 'stand' to stand: ")
        if choice.lower() == "hit":
            new_card = pick_card()
            print(f"You picked a {new_card}, and your total is now {player_total + find_value(new_card, player_total)}")
            return find_value(new_card, player_total)
        elif choice.lower() == 'stand':
            return 0
        print("Invalid input; try again")

def stand(cards):
    dealer_total = total(cards) 
    while dealer_total < 17:
        new_card = pick_card()
        cards.append(new_card)
        dealer_total = total(cards)
    
    return cards  


def total(cards):
    total = 0
    for c in cards:
        total += find_value(c, total)
    return total

def winner(player_cards, dealer_cards):
    player_total = total(player_cards)
    dealer_total = total(dealer_cards)
    
    if player_total > 21:
        return "Dealer wins (you busted!)"
    elif dealer_total > 21:
        return "You win (dealer busted!)"
    elif player_total > dealer_total:
        return "You win!"
    elif player_total < dealer_total:
        return "Dealer wins!"
    else:
        return "It's a tie!"
