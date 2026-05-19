"""
GHAS Demo App — Backend (Flask)
Deliberately vulnerable for GH-500 training.
DO NOT deploy to production.
"""

import sqlite3
import os
from flask import Flask, request, jsonify, g

app = Flask(__name__)

# VULNERABILITY: Hardcoded database credentials (Demo 5.3 — custom CodeQL query)
DB_PASSWORD = "SuperSecret123!"
DB_HOST = "prod-db.internal.example.com"
API_SECRET_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"

DATABASE = os.path.join(os.path.dirname(__file__), "users.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables and seed demo data."""
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    """
    )
    # Seed data
    for user in [
        ("alice", "alice@example.com", "admin"),
        ("bob", "bob@example.com", "user"),
        ("charlie", "charlie@example.com", "user"),
    ]:
        db.execute(
            "INSERT OR IGNORE INTO users (username, email, role) VALUES (?, ?, ?)", user
        )
    for product in [
        ("Widget", 9.99, "A standard widget"),
        ("Gadget", 19.99, "A fancy gadget"),
        ("Gizmo", 29.99, "An advanced gizmo"),
    ]:
        db.execute(
            "INSERT OR IGNORE INTO products (name, price, description) VALUES (?, ?, ?)",
            product,
        )
    db.commit()
    db.close()


# ---------------------------------------------------------------------------
# VULNERABILITY: SQL Injection — Demo 1.2, 4.3, 5.4
# Used for: CodeQL code scanning alerts, taint-tracking path query
# ---------------------------------------------------------------------------


@app.route("/user")
def get_user():
    """Fetch a user by username. VULNERABLE to SQL injection."""
    username = request.args.get("username", "")
    db = get_db()
    # BAD: f-string interpolation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor = db.execute(query)
    row = cursor.fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "User not found"}), 404


@app.route("/search")
def search():
    """Search products by name. VULNERABLE to SQL injection."""
    q = request.args.get("q", "")
    db = get_db()
    # BAD: user input directly in SQL
    cursor = db.execute(f"SELECT * FROM products WHERE name LIKE '%{q}%'")
    results = [dict(r) for r in cursor.fetchall()]
    return jsonify(results)


@app.route("/user/delete")
def delete_user():
    """Delete a user. VULNERABLE to SQL injection."""
    user_id = request.args.get("id", "")
    db = get_db()
    # BAD: unparameterized query
    db.execute("DELETE FROM users WHERE id = " + user_id)
    db.commit()
    return jsonify({"status": "deleted"})


# ---------------------------------------------------------------------------
# SAFE versions (used to show the fix in Demo 4.3)
# ---------------------------------------------------------------------------


@app.route("/user/safe")
def get_user_safe():
    """Fetch a user by username. SAFE — parameterized query."""
    username = request.args.get("username", "")
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "User not found"}), 404


@app.route("/search/safe")
def search_safe():
    """Search products by name. SAFE — parameterized query."""
    q = request.args.get("q", "")
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM products WHERE name LIKE ?", (f"%{q}%",)
    )
    results = [dict(r) for r in cursor.fetchall()]
    return jsonify(results)


# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    # VULNERABILITY: Debug mode on, binding to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
