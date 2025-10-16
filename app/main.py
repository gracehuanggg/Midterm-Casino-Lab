from flask import Flask, request, session, redirect, url_for
from user import UserManager
from player import Player
from blackjack import pick_card, add, stand, winner, total

app = Flask(__name__)
user_manager = UserManager()
app.secret_key = "supersecretkey"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if user_manager.authenticate(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "<h3>Invalid username or password.</h3>"

    return """
        <form method='POST'>
            <h2>Login</h2>
            Username: <input name='username'><br>
            Password: <input type='password' name='password'><br><br>
            <button type='submit'>Login</button>
        </form>
    """


@app.route("/home")
def home():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    db = user_manager._load_db()
    user_data = db.get("users").get(username)
    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)

    player = Player(username, pw, balance, money_won, money_lost)

    return f"""
    <h2>Welcome {username}!</h2>
    <p>Balance: ${balance}</p>
    <form action="{url_for('start')}" method="post">
        <button type="submit">Play Blackjack</button>
    </form>
    """
@app.route("/start", methods=["POST"])
def start():
    dealer_cards = [pick_card(), pick_card()]
    player_cards = [pick_card(), pick_card()]

    session["dealer_cards"] = dealer_cards
    session["player_cards"] = player_cards

    return f"""
    <h2>How much do you wnat to bet?</h2>
    <form action="{url_for('bet')}" method="post">
        <input type="number" name="bet_amount" min="1" required>
        <button type="submit">Place Bet</button>
    """

@app.route("/bet", methods=["POST"])
def bet():
    bet_amount = int(request.form["bet_amount"])
    session["bet_amount"] = bet_amount
    return redirect(url_for("blackjack"))


@app.route("/blackjack")
def blackjack():
    dealer_cards = session.get("dealer_cards")
    player_cards = session.get("player_cards")
    dealer_total = total(dealer_cards)
    player_total = total(player_cards)

    return f"""
    <h2>Blackjack</h2>
    <p>Dealer's card: {dealer_cards[0]}</p>
    <p>Your cards: {', '.join(player_cards)}</p>
    <p>Your total: {player_total}</p>

    <form action="{url_for('hit')}" method="post">
        <button type="submit">Hit</button>
    </form>
    <form action="{url_for('stand_route')}" method="post">
        <button type="submit">Stand</button>
    </form>
    """

@app.route("/hit", methods=["POST"])
def hit():
    player_cards = session.get("player_cards")
    new_card = pick_card()
    player_cards.append(new_card)
    session["player_cards"] = player_cards

    player_total = total(player_cards)
    if player_total > 21:
        dealer_cards = session.get("dealer_cards")
        dealer_cards = stand(dealer_cards)
        session["dealer_cards"] = dealer_cards
        result = winner(player_cards, dealer_cards)
        return f"""
        <h3>You busted!</h3>
        <p>Dealer cards: {', '.join(dealer_cards)}</p>
        <p>Your cards: {', '.join(player_cards)}</p>
        <p>Result: {result}</p>
        <a href="{url_for('home')}">Play Again</a>
        """
    return redirect(url_for("blackjack"))

@app.route("/stand", methods=["POST"])
def stand_route():
    dealer_cards = session.get("dealer_cards")
    player_cards = session.get("player_cards")

    dealer_cards = stand(dealer_cards)
    session["dealer_cards"] = dealer_cards

    result = winner(player_cards, dealer_cards)
    return f"""
    <h3>Game Over</h3>
    <p>Dealer cards: {', '.join(dealer_cards)}</p>
    <p>Your cards: {', '.join(player_cards)}</p>
    <p>Result: {result}</p>
    <a href="{url_for('home')}">Play Again</a>
    """
if __name__ == "__main__":
    app.run(debug=True)
