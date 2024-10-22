import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    user = db.execute("SELECT cash FROM users where id = ?", user_id)[0]
    portfolio = []
    total_value = 0

    holdings = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)
    for holding in holdings:
        symbol = holding["symbol"]
        total_shares = holding["total_shares"]
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol", 400)

        current_price = stock["price"]
        holding_value = current_price * total_shares
        portfolio.append({
            "symbol": symbol,
            "name": stock["name"],
            "shares": total_shares,
            "price": current_price,
            "total": holding_value
        })

        total_value += holding_value

    grand_total = user["cash"] + total_value

    return render_template("index.html", portfolio=portfolio, cash=user["cash"], grand_total=grand_total)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please provide a stock symbol", 400)
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol", 400)
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please provide a valid stock symbol", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Please provide a positive integer for shares", 400)
        except ValueError:
            return apology("Please provide a positive integer for shares", 400)

        user_id = session["user_id"]
        user = db.execute("SELECT cash FROM users where id = ?", user_id)[0]
        total_cost = stock["price"] * shares

        if total_cost > user["cash"]:
            return apology("You cannot afford that many shares", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, shares, stock["price"], datetime.datetime.now())
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please provide a valid stock symbol", 400)

        owned_stock = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if not owned_stock or owned_stock[0]["total_shares"] <= 0:
            return apology("You don't have enough shares to sell", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Please provide a positive integer for shares", 400)
        except ValueError:
            return apology("Please provide a positive integer for shares", 400)

        total_shares = owned_stock[0]["total_shares"]
        if shares > total_shares:
            return apology("You don't have enough shares to sell", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol", 400)

        total_value = shares * stock["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, -shares, stock["price"], datetime.datetime.now())

        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=symbols)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, date FROM transactions WHERE user_id = ? ORDER BY date DESC", user_id)

    return render_template("history.html", transactions=transactions)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if any fields are blank
        if not username or not password or not confirmation:
            return apology("All fields are required", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("Passwords do not match", 400)

        hashed_password = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, hashed_password)
        except ValueError:
            return apology("Username already exists", 400)

        return redirect("/login")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
