from flask import Flask, request, session, redirect, url_for
from user import UserManager
from player import Player
from blackjack import pick_card, add, stand, winner, total

app = Flask(__name__)
user_manager = UserManager()
app.secret_key = "hiding_shit"


@app.route("/")
def index():
    username = session.get("username")
    if username:
        return redirect(url_for("login"))
    return redirect(url_for("login"))


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

    return f"""
        <form method='POST'>
            <h2>Login</h2>
            Username: <input name='username'><br>
            Password: <input type='password' name='password'><br><br>
            <button type='submit'>Login</button>
            <p>Why dont you have an account you buffon <a href='{url_for('register')}'>Register</a></p>
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
    <form action="{url_for('add_funds')}" method="post">
        Add funds: <input name='amount' type='number' min='1' step='1' required>
        <button type='submit'>Add</button>
    </form>
    <form action="{url_for('logout')}" method="post">
        <button type="submit">Logout</button>
    </form>
    """

@app.route("/logout", methods=["POST"])
def logout():
    return redirect(url_for("login"))
@app.route("/start", methods=["GET", "POST"])
def start():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    # load balance from DB
    db = user_manager._load_db()
    user_data = db.get("users", {}).get(username, {})
    balance = user_data.get("balance", 0)

    # If form submitted with a bet, validate and start the game
    if request.method == "POST" and request.form.get("bet"):
        try:
            bet = int(request.form.get("bet"))
        except (TypeError, ValueError):
            return f"<h3>Invalid bet amount.</h3><a href='{url_for('start')}'>Back</a>"

        if bet <= 0 or bet > balance:
            return f"<h3>Bet must be between 1 and your balance (${balance}).</h3><a href='{url_for('start')}'>Back</a>"

        # store bet in session and deal cards
        session["bet"] = bet
        dealer_cards = [pick_card(), pick_card()]
        player_cards = [pick_card(), pick_card()]

        session["dealer_cards"] = dealer_cards
        session["player_cards"] = player_cards

        return redirect(url_for("blackjack"))

    # Otherwise show a simple bet form
    return f"""
        <h2>Place your bet</h2>
        <p>Your balance: ${balance}</p>
        <form method='POST'>
            Bet amount: <input name='bet' type='number' min='1' max='{balance}' required><br><br>
            <button type='submit'>Start Game</button>
        </form>
        <a href='{url_for('home')}'>Back to Home</a>
    """

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
        bet = session.get("bet", 0)
        username = session.get("username")
        if username and bet:
            apply_bet_result(username, result, bet)

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
    # apply bet outcome to user's balance
    bet = session.get("bet", 0)
    username = session.get("username")
    if username and bet:
        apply_bet_result(username, result, bet)

    return f"""
    <h3>Game Over</h3>
    <p>Dealer cards: {', '.join(dealer_cards)}</p>
    <p>Your cards: {', '.join(player_cards)}</p>
    <p>Result: {result}</p>
    <a href="{url_for('home')}">Play Again</a>
    """


def apply_bet_result(username, result, bet):
    """Update the user's balance and win/loss counters in the JSON DB.
    bet is expected as an int.
    """
    try:
        bet = int(bet)
    except (TypeError, ValueError):
        return

    db = user_manager._load_db()
    users = db.setdefault("users", {})
    user = users.get(username)
    if not user:
        return

    balance = user.get("balance", 0)
    money_won = user.get("money_won", 0)
    money_lost = user.get("money_lost", 0)

    if "You win" in result:
        balance += bet
        money_won = money_won + bet
    elif "Dealer wins" in result:
        balance -= bet
        money_lost = money_lost + bet
    else:
#nothing happens if yall tie
        pass
    user["balance"] = balance
    user["money_won"] = money_won
    user["money_lost"] = money_lost

    user_manager._save_db(db)


@app.route("/add_funds", methods=["POST"])
def add_funds():
    username = session.get("username")
    amount_number = request.form.get("amount")
    try:
        amount = float(amount_number)
    except (TypeError, ValueError):
        return f"<h3>Invalid amount, dofus.</h3><a href='{url_for('home')}'>Back</a>"

    if amount <= 0:
        return f"<h3>Amount must be positive, ding dong.</h3><a href='{url_for('home')}'>Back</a>"

    db = user_manager._load_db()
    users = db.setdefault("users", {})
    user_data = users.get(username)
    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)

    player = Player(username, pw, balance, money_won, money_lost)

    player.update_balance(amount)
    player.update_db()

    return f"<h3>Added ${amount:.2f} to your account.</h3><a href='{url_for('home')}'>You dont need to be here anymore do silly goose</a>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        db = user_manager._load_db()
        users = db.setdefault('users', {})
        users.setdefault(username, {})
        users[username].setdefault('balance', 67)
        users[username].setdefault('money_won', 0)
        users[username].setdefault('money_lost', 0)
        user_manager._save_db(db)

        session['username'] = username
        return redirect(url_for('home'))

    # GET -> show simple registration form
    return f"""
        <form method='POST'>
            <h2>Register</h2>
            Username: <input name='username'><br>
            Password: <input type='password' name='password'><br><br>
            <button type='submit'>Register</button>
        </form>
        <a href='{url_for('login')}'>Back to Login</a>
    """



if __name__ == "__main__":
    app.run(debug=True)
