from flask import Flask, request, session, redirect, url_for
from user import UserManager
from player import Player
from blackjack import pick_card, add, stand, winner, total
from slot import pull_lever

app = Flask(__name__)
user_manager = UserManager()
app.secret_key = "hiding_shit"


def center_page(body_html: str) -> str:
    return f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 0; }}
            .center-container {{
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                gap: 12px;
                padding: 20px;
                box-sizing: border-box;
            }}
            .center-container form {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
            }}
            .center-container input[type='number'],
            .center-container input[type='text'],
            .center-container input[type='password'] {{
                padding: 6px 8px;
                font-size: 14px;
            }}
            .center-container button {{
                padding: 8px 12px;
                font-size: 14px;
                cursor: pointer;
            }}
            a {{ color: #0645AD; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class='center-container'>
            {body_html}
        </div>
    </body>
    </html>
    """


@app.route("/")
def index():
    username = session.get("username")
    if username:
        return redirect(url_for("home"))
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
            return center_page("""
                <h3>Invalid login credentials!!</h3>
                <a href='{}'>Back to Login</a>
            """.format(url_for('login')))

    return center_page(f"""
        <form method='POST'>
            <h2>Login</h2>
            Username: <input name='username' type='text'><br>
            Password: <input type='password' name='password'><br>
            <button type='submit'>Login</button>
            <p>Why don't you have an account, you buffoon! <a href='{url_for('register')}'>Register</a></p>
        </form>
    """)


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
    
    display_name = user_data.get("preferred_name") or username

    return f"""
        <h2>Welcome {display_name}!</h2>

        <h3>Place your bet</h3>
        <form action="{url_for('start')}" method="post">
            Bet amount:
            <input name='bet' type='number' min='0.01' step='0.01' required><br><br>
            <button type='submit'>Play Blackjack</button>
        </form>

        <p><a href="{url_for('wallet')}">Go to Wallet (balance & add funds)</a></p>

        <form action="{url_for('slot')}" method="post">
            <button type="submit">Pull Slot Machine Lever</button>
        </form>
        <p>Play the slot machine game! 10$ to spin once! </p>
        <form action="{url_for('logout')}" method="post">
            <button type="submit">Logout</button>
        </form>
"""

@app.route("/wallet")
def wallet():
    username=session.get("username")
    if not username:
        return redirect(url_for("login"))

    db = user_manager._load_db()
    user_data = db.get("users", {}).get(username)
    if not user_data:
        session.clear()
        return redirect(url_for("login"))

    balance = float(user_data.get("balance", 0))
    money_won = float(user_data.get("money_won", 0))
    money_lost = float(user_data.get("money_lost", 0))

    return f"""
        <h2>Wallet</h2>
        <p>Balance: ${balance:.2f}</p>
        <p>Total Won: ${money_won:.2f} | Total Lost: ${money_lost:.2f}</p>

        <h3>Add Funds</h3>
        <form action="{url_for('add_funds')}" method="post">
            <label>Amount:</label>
            <input name='amount' type='number' min='0.01' step='0.01' required>
            <button type='submit'>Add</button>
        </form>

        <p><a href="{url_for('home')}">Back to Home</a></p>
    """

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/slot", methods=["GET", "POST"])
def slot():
    username = session.get("username")
    if not username:    
        return redirect(url_for("login"))
    
    db = user_manager._load_db()
    users = db.setdefault("users", {})
    user_data = users.get(username)
    pw = user_data.get("pw")
    balance = user_data.get("balance", 0)
    money_won = user_data.get("money_won", 0)
    money_lost = user_data.get("money_lost", 0)

    player = Player(username, pw, balance, money_won, money_lost)
    cards = pull_lever()
    player.update_balance(-10)
    message = ""
    if (cards[0] == cards[1] == cards[2]):
        player.update_balance(cards[0] * 3)
        message = f"Congrats! You won {cards[0] * 3}!"
    else:
        message = "You didn't win anything :("

    return center_page(f"""
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
    """)
    player.update_db()
    return f"""
    <h2>Slot Machine: </h2>   
    <p>Your pulls: {', '.join(map(str, cards))}</p>
    <p>{message}</p>
    <p>Your new balance is: ${player.balance}</p>
    <a href="{url_for('home')}">Back to Home</a>
    """

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
    balance = float(user_data.get("balance", 0))
    
    # If form submitted with a bet, validate and start the game
    if request.method == "POST" and request.form.get("bet"):
        try:
            bet = float(request.form.get("bet"))
        except (TypeError, ValueError):
            return center_page(f"""
                <h3>Invalid bet amount.</h3>
                <a href='{url_for('start')}'>Back</a>
            """)

        if bet <= 0 or bet > balance:
            return center_page(f"""
                <h3>Bet must be between 1 and your balance (${balance}).</h3>
                <a href='{url_for('start')}'>Back</a>
            """)
            return f"<h3>Bet must be between 0.01 and your balance (${balance:.2f}).</h3><a href='{url_for('start')}'>Back</a>"
        session["bet"]= round(bet, 2)

        # store bet in session and deal cards
        dealer_cards = [pick_card(), pick_card()]
        player_cards = [pick_card(), pick_card()]

        session["dealer_cards"] = dealer_cards
        session["player_cards"] = player_cards

        return redirect(url_for("blackjack"))

    # Otherwise show a simple bet form
    return center_page(f"""
        <h2>Place your bet</h2>
        <p>Your balance: ${balance}</p>
        <form method='POST'>
            Bet amount: <input name='bet' type='number' min='1' max='{balance}' required>
            <button type='submit'>Start Game</button>
        </form>
        <a href='{url_for('home')}'>Back to Home</a>
    """)

@app.route("/blackjack")
def blackjack():
    dealer_cards = session.get("dealer_cards")
    player_cards = session.get("player_cards")

    if not dealer_cards or not player_cards:
        return redirect(url_for("start"))
        
    dealer_total = total(dealer_cards)
    player_total = total(player_cards)

    return center_page(f"""
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
    """)

@app.route("/hit", methods=["POST"])
def hit():
    player_cards = session.get("player_cards")
    if not player_cards:
        return redirect(url_for("start"))
    new_card = pick_card()
    player_cards.append(new_card)
    session["player_cards"] = player_cards

    player_total = total(player_cards)
    if player_total > 21:
        dealer_cards = session.get("dealer_cards")
        dealer_cards = stand(dealer_cards)
        if not dealer_cards or not player_cards:
            return redirect(url_for("start"))
        dealer_cards = stand(dealer_cards)
        session["dealer_cards"] = dealer_cards
        result = winner(player_cards, dealer_cards)
        bet = session.get("bet", 0)
        username = session.get("username")
        if username and bet:
            apply_bet_result(username, result, bet)
        return center_page(f"""
        <h3>You busted!</h3>
        <p>Dealer cards: {', '.join(dealer_cards)}</p>
        <p>Your cards: {', '.join(player_cards)}</p>
        <p>Result: {result}</p>
        <a href="{url_for('home')}">Play Again</a>
        """)
    return redirect(url_for("blackjack"))

@app.route("/stand", methods=["POST"])
def stand_route():
    dealer_cards = session.get("dealer_cards")
    player_cards = session.get("player_cards")
    if not dealer_cards or not player_cards:
        return redirect(url_for("start"))
    dealer_cards = stand(dealer_cards)
    session["dealer_cards"] = dealer_cards

    result = winner(player_cards, dealer_cards)
    # apply bet outcome to user's balance
    bet = session.get("bet", 0)
    username = session.get("username")
    if username and bet:
        apply_bet_result(username, result, bet)

    return center_page(f"""
    <h3>Game Over</h3>
    <p>Dealer cards: {', '.join(dealer_cards)}</p>
    <p>Your cards: {', '.join(player_cards)}</p>
    <p>Result: {result}</p>
    <a href="{url_for('home')}">Play Again</a>
    """)


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
    if not username:
        return redirect(url_for("login"))
    amount_number = request.form.get("amount")
    try:
        amount = float(amount_number)
    except (TypeError, ValueError):
        return center_page(f"""
            <h3>Invalid amount, dofus.</h3>
            <a href='{url_for('home')}'>Back</a>
        """)

    if amount <= 0:
        return center_page(f"""
            <h3>Amount must be positive, ding dong.</h3>
            <a href='{url_for('home')}'>Back</a>
        """)

    if amount > 1_000_000_000:
        return center_page(f"""<h3>Deposit exceeds the $1,000,000,000 limit. Do not add so much money!</h3><a href='{url_for('home')}'>Back</a>"
        """)

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

    return center_page(f"""
        <h3>Added ${amount:.2f} to your account.</h3>
        <a href='{url_for('home')}'>Back to Home</a>
    """)


@app.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        preferred_name = request.form.get('preferred_name', '').strip()
        if preferred_name == "":
            preferred_name = None

        success = user_manager.register(username, password, preferred_name)

        if not success:
            return center_page("""
                <h3>Username already exists.</h3>
                <a href='/register'>Try again</a>
            """)

        session['username'] = username
        return redirect(url_for('home'))

    # GET -> show simple registration form
    return center_page(f"""
        <form method='POST'>
            <h2>Register</h2>
            Username: <input name='username'><br>
            Password: <input type='password' name='password'><br>
            Preferred Name (optional): <input name='preferred_name'><br><br>
            <button type='submit'>Register</button>
        </form>
        <a href='{url_for('login')}'>Back to Login</a>
    """)

if __name__ == "__main__":
    app.run(debug=True)
