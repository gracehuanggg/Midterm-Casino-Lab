from flask import Flask, request
from user import UserManager

app = Flask(__name__)
user_manager = UserManager()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if user_manager.authenticate(username, password):
            return f"<h2>Welcome, {username}!</h2>"
        else:
            return "<h3>Invalid username or password.</h3>"

    # GET: show the form
    return '''
        <form method="POST">
            <h2>Python Casino Login</h2>
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Login</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

