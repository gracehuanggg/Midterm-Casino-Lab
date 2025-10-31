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
            body {{ 
                font-family: Arial, Helvetica, sans-serif; 
                margin: 0; 
                padding: 0; 
                background-color: #b8e2f2;
            }}
            .center-container {{
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                gap: 12px;
                padding: 20px;
                box-sizing: border-box;
                background-color: #f0f0f0;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: 20px auto;
                min-height: calc(100vh - 40px);
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
    if username in session:
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
            <p>Why dont you have an account you buffon <a href='{url_for('register')}'>Register</a></p>
        </form>
    """)


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

    return center_page(f"""
    <h2>Welcome {username}!</h2>
    <p>Balance: ${balance}</p>
    <div style="width:100%; max-width:500px; background:#ffffff; border:1px solid #ddd; padding:12px; border-radius:8px; display:flex; gap:12px;">
        <div style="text-align:center;">
            <div style="font-size:18px; font-weight:600;">${money_won}</div>
            <div style="font-size:12px; color:#666;">Money Won</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:18px; font-weight:600;">${money_lost}</div>
            <div style="font-size:12px; color:#666;">Money Lost</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:18px; font-weight:600;">${money_won - money_lost}</div>
            <div style="font-size:12px; color:#666;">Net</div>
        </div>
    </div>
    <form action="{url_for('start')}" method="post">
        <button type="submit">Play Blackjack</button>
    </form>
    <form action="{url_for('start_slots')}" method="post">
        <button type="submit">Lose all money in slots</button>
    </form>
    <form action="{url_for('add_funds')}" method="post">
        Add funds: <input name='amount' type='number' min='1' step='1' required>
        <button type='submit'>Add</button>
    </form>
    <form action="{url_for('logout')}" method="post">
        <button type="submit">Logout</button>
    </form>
    """)

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
            return center_page(f"""
                <h3>Invalid bet amount.</h3>
                <a href='{url_for('start')}'>Back</a>
            """)

        if bet <= 0 or bet > balance:
            return center_page(f"""
                <h3>Bet must be between 1 and your balance (${balance}).</h3>
                <a href='{url_for('start')}'>Back</a>
            """)

        # store bet in session and deal cards
        session["bet"] = bet
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
        return center_page(f"""
            <h3>Invalid amount, dofus.</h3>
            <a href='{url_for('home')}'>Back</a>
        """)

    if amount <= 0:
        return center_page(f"""
            <h3>Amount must be positive, ding dong.</h3>
            <a href='{url_for('home')}'>Back</a>
        """)

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

    return center_page(f"""
        <h3>Added ${amount:.2f} to your account.</h3>
        <a href='{url_for('home')}'>Back to Home</a>
    """)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        success = user_manager.register(username, password)
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
            Username: <input name='username' type='text'><br>
            Password: <input type='password' name='password'><br>
            <button type='submit'>Register</button>
        </form>
        <a href='{url_for('login')}'>Back to Login</a>
    """)



@app.route("/start_slots", methods=["GET", "POST"])
def start_slots():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    db = user_manager._load_db()
    user_data = db.get("users", {}).get(username, {})
    balance = user_data.get("balance", 0)

    if request.method == "POST" and request.form.get("bet"):
        try:
            bet = int(request.form.get("bet"))
        except (TypeError, ValueError):
            return center_page(f"""
                <h3>Invalid bet amount.</h3>
                <a href='{url_for('start_slots')}'>Back</a>
            """)

        if bet <= 0 or bet > balance:
            return center_page(f"""
                <h3>Bet must be between 1 and your balance (${balance}).</h3>
                <a href='{url_for('start_slots')}'>Back</a>
            """)

        session["slots_bet"] = bet
        return redirect(url_for("play_slots"))

    return center_page(f"""
        <h2>Place your bet for Slots</h2>
        <p>Your balance: ${balance}</p>
        <form method='POST'>
            Bet amount: <input name='bet' type='number' min='1' max='{balance}' required>
            <button type='submit'>Play Slots</button>
        </form>
        <a href='{url_for('home')}'>Back to Home</a>
    """)

@app.route("/play_slots")
def play_slots():

    
    bet = session.get("slots_bet", 0)
    if not bet:
        return redirect(url_for("start_slots"))

    slot_results = pull_lever()    

    won = len(set(slot_results)) == 1   

    if won:
        win_amount = bet * 3  
        result_text = f"Congratulations! You won ${win_amount}!"
    else:
        win_amount = -bet
        result_text = f"Why would you play slots? You just lost ${bet}. Try again!"

    username = session.get("username")
    if username:
        db = user_manager._load_db()
        users = db.setdefault("users", {})
        user = users.get(username)
        if user:
            balance = user.get("balance", 0)
            money_won = user.get("money_won", 0)
            money_lost = user.get("money_lost", 0)

            if won:
                balance += win_amount
                money_won += win_amount
            else:
                balance -= bet
                money_lost += bet

            user["balance"] = balance
            user["money_won"] = money_won
            user["money_lost"] = money_lost
            user_manager._save_db(db)

    session.pop("slots_bet", None)

    emoji_map = {4: "🍎", 8: "🍌", 12: "🍒", 16: "🎰"}
    slot_display = " ".join([emoji_map.get(num, "❓") for num in slot_results])

    return center_page(f"""
        <h2>Slot Machine Results</h2>
        <div style="font-size: 48px; margin: 20px 0;">
            {slot_display}
        </div>
        <p>{result_text}</p>
        <form action="{url_for('start_slots')}" method="get">
            <button type="submit">Play Again</button>
        </form>
        <a href="{url_for('home')}">Back to Home</a>
    """)

if __name__ == "__main__":
    app.run(debug=True)
