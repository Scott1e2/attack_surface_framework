from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change for production

# Load configuration
DATA_FILE = "../reports/output/detailed_report.json"


def load_results():
    """
    Loads vulnerability results from the JSON file.
    """
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results: {e}")
        return []


@app.route("/", methods=["GET", "POST"])
def login():
    """
    User login page.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Example credentials (replace with a proper database or authentication system)
        if username == "admin" and password == "password":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """
    Dashboard for viewing vulnerabilities.
    """
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    results = load_results()
    return render_template("dashboard.html", results=results)


@app.route("/filter", methods=["GET"])
def filter_results():
    """
    API endpoint to filter results based on query parameters.
    """
    severity = request.args.get("severity")
    plugin = request.args.get("plugin")
    results = load_results()

    if severity:
        results = [r for r in results if r.get("severity") == severity]

    if plugin:
        results = [r for r in results if r.get("plugin") == plugin]

    return jsonify(results)


@app.route("/logout")
def logout():
    """
    Log out the current user.
    """
    session.pop("logged_in", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
