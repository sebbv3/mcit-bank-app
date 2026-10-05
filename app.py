from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mcit-bank-demo-key"

account = {
    "name": "Sebastian Vita",
    "account_number": "0007007007",
    "account_type": "Chequing Account",
    "branch": "Montreal",
    "currency": "CAD"
}

balance = 1000.00

transactions = [
    {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "Opening Balance",
        "amount": 1000.00,
        "balance": 1000.00
    }
]


@app.route("/")
def home():

    total_deposits = sum(
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "Deposit"
    )

    total_withdrawals = sum(
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "Withdrawal"
    )

    return render_template(
        "index.html",
        account=account,
        balance=balance,
        total_deposits=total_deposits,
        total_withdrawals=total_withdrawals,
        transactions=reversed(transactions)
    )


@app.route("/deposit", methods=["POST"])
def deposit():

    global balance

    try:
        amount = float(request.form["amount"])

        if amount <= 0:
            flash("Please enter a valid deposit amount.", "error")
            return redirect(url_for("home"))

        balance += amount

        transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Deposit",
            "amount": amount,
            "balance": balance
        })

        flash("Deposit successful!", "success")

    except ValueError:
        flash("Invalid amount.", "error")

    return redirect(url_for("home"))


@app.route("/withdraw", methods=["POST"])
def withdraw():

    global balance

    try:
        amount = float(request.form["amount"])

        if amount <= 0:
            flash("Please enter a valid withdrawal amount.", "error")

        elif amount > balance:
            flash("Insufficient funds.", "error")

        else:
            balance -= amount

            transactions.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Withdrawal",
                "amount": amount,
                "balance": balance
            })

            flash("Withdrawal successful!", "success")

    except ValueError:
        flash("Invalid amount.", "error")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)