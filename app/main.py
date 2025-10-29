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
        return redirect(url_for("home"))
    return redirect(url_for("login"))

    return f"""
    <h2>Welcome {username}!</h2>

    <h3>Place your bet</h3>
    <form action="{url_for('start')}"method="post">
        Bet amount:
        <input name='bet' type='number' min='1' step='0.01' required><br><br>
        <button type='submit'>Play Blackjack</button>
    </form>

    <p><a href="{url_for('start')}">Go to Wallet(balance & add funds)</a></p>
    <form action="{url_for('logout')}" method="post">
        <button type="submit">Logout</button>
    </form>
    """
@app.route("/wallet")
def wallet():
    username=session.get("username")
    if not user_data:
        session.clear()
        return redirect (url_for("login"))

    balance = float(user_data.get("balance", 0))
    money = float(user_data.get("money_won", 0))
    money_lost = float(user_data.get("money_lost", 0))

    return f"""
        <h2>Wallet</h2>
        <p>Balance: ${balance:.2f}</p>
        <p>Total Won: ${money_won.2f} | Total Lost: ${money_lost:2f}</p>

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if user_manager.authenticate(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "<h3>Invalid login credentials!!</h3>"

    return f"""
        <form method='POST'>
            <h2>Login</h2>
            Username: <input name='username'><br>
            Password: <input type='password' name='password'><br><br>
            <button type='submit'>Login</button>
            <p>Why don't you have an account, you buffoon! <a href='{url_for('register')}'>Register</a></p>
        </form>
        
    """


@app.route("/home")
def home():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    db = user_manager._load_db()
    user_data = db.get("users").get(username)
    if not user_data:
        session.clear()
        return redirect(url_for("login"))
    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)

    player = Player(username, pw, balance, money_won, money_lost)

    return f"""
    <h2>Welcome {username}!</h2>
    <p>Balance: ${balance:.2f}</p>
    <h3>Place your bet</h3>
    <form action="{url_for('start')}" method="post">
        Bet amount:
        <input name='bet' type='number' min='1' max='{balance:.2f}' step='0.01' required><br><br>
        <button type='submit'>Play Blackjack</button>
    </form>
    <form action="{url_for('add_funds')}" method="post">
        Add funds: <input name='amount' type='number' min='0.01' step='0.01' required>
        <button type='submit'>Add</button>
    </form>
    <form action="{url_for('logout')}" method="post">
        <button type="submit">Logout</button>
    </form>
    """

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/start", methods=["GET", "POST"])
def start():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    # load balance from DB
    db = user_manager._load_db()
    user_data = db.get("users", {}).get(username, {})
    if not user_data:
        session.clear()
        return redirect(url_for("login"))
    balance = user_data.get("balance", 0)

    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)
    
    # If form submitted with a bet, validate and start the game
    if request.method == "POST" and request.form.get("bet"):
        try:
            bet = float(request.form.get("bet"))
        except (TypeError, ValueError):
            return f"<h3>Invalid bet amount.</h3><a href='{url_for('start')}'>Back</a>"

        if bet <= 0 or bet > balance:
            return f"<h3>Bet must be between 0.01 and your balance (${balance:.2f}).</h3><a href='{url_for('start')}'>Back</a>"
        session["bet"]= round(bet, 2)

        # store bet in session and deal cards
        dealer_cards = [pick_card(), pick_card()]
        player_cards = [pick_card(), pick_card()]

        session["dealer_cards"] = dealer_cards
        session["player_cards"] = player_cards

        return redirect(url_for("blackjack"))

    # Otherwise show a simple bet form
    return f"""
        <h2>Place your bet</h2>
        <p>Your balance: ${balance:.2f}</p>
        <form method='POST'>
            Bet amount: <input name='bet' type='number' min='0.01' max='{balance:.2f}' step='0.01' required><br><br>
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
    bet is expected as a float.
    """
    try:
        bet = float(bet)
    except (TypeError, ValueError):
        return

    db = user_manager._load_db()
    users = db.setdefault("users", {})
    user = users.get(username)
    if not user:
        return

    balance = float(user.get("balance", 0))
    money_won = float(user.get("money_won", 0))
    money_lost = float(user.get("money_lost", 0))

    if "You win" in result:
        balance += bet
        money_won = money_won + bet
    elif "Dealer wins" in result:
        balance -= bet
        money_lost = money_lost + bet
    else:
#nothing happens if yall tie
        pass
    user["balance"] = round(balance, 2)
    user["money_won"] = round(money_won, 2)
    user["money_lost"] = round (money_lost, 2)

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
    if not user_data:
        session.clear()
        return redirect(url_for("login"))
    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)

    player = Player(username, pw, balance, money_won, money_lost)

    player.update_balance(amount)
    player.update_db()

    return f"<h3>Added ${amount:.2f} to your account.</h3><a href='{url_for('home')}'>You don't need to be here anymore, you silly goose</a>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        success = user_manager.register(username, password)
        if not success:
            return "<h3>Username already exists.</h3><a href='/register'>Try again</a>"

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
