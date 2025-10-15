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

def bet():
    b = input("How much do you want to bet? ")
    return int(b)

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

def stand(dealer_total):
    while(dealer_total < 17):
        new_card = pick_card()
        print(f"The dealer picked a {new_card}")
        dealer_total += find_value(new_card, dealer_total)
    
    return dealer_total

def winner(dealer_total, player_total):
    winner = ""
    print(f"The dealer's total is {dealer_total}")
    print(f"Your total is {player_total}")
    if dealer_total > 21:
        print("Dealer busts! You win!")
        winner = "player"
    elif dealer_total == player_total:
        print("It's a tie!")
        winner = "tie"
    elif dealer_total > player_total:
        print("Dealer wins!")
        winner = "dealer"
    else:
        print("You win!")
        winner = "player"
    return winner

def game():
    print("Blackjack is starting!")
    dealer_card1 = pick_card()
    dealer_card2 = pick_card()
    player_card1 = pick_card()
    player_card2 = pick_card()

    print(f"One of the dealer's card is: {dealer_card1}")
    print(f"Your cards are {player_card1} and {player_card2}")
    dealer_total = 0
    player_total = 0
    dealer_total = add(dealer_card1, dealer_card2, dealer_total)
    player_total = add(player_card1, player_card2, player_total)
    print(f"Your total is {player_total}")

    while True:
        choice = pick(player_total)
        if choice == "stand": 
            dealer_total = stand(dealer_total)
            winner(dealer_total, player_total)
            break
        else: 
            player_total += choice
            if player_total > 21:
                winner(dealer_total, player_total)
                break
            if (dealer_total < 17):
                dealer_total += find_value(pick_card(), dealer_total)
                if dealer_total > 21:
                    winner(dealer_total, player_total)
                    break