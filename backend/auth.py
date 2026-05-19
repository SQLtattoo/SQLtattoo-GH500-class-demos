"""
GHAS Demo App — Authentication module
Deliberately vulnerable for GH-500 training.
"""

import hashlib
import traceback
from flask import request, jsonify


# VULNERABILITY: Hardcoded API key (Demo 3.3 — custom secret pattern)
INTERNAL_API_TOKEN = "INTERNAL_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"
BACKUP_TOKEN = "INTERNAL_9Z8Y7X6W5V4U3T2S1R0QPONMLKJIHGFED"


def hash_password(password):
    """Hash a password. VULNERABLE — uses MD5 (weak, no salt)."""
    # BAD: MD5 is cryptographically broken for password storage
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    """Verify password against stored hash."""
    return hash_password(password) == stored_hash


def authenticate(app):
    """Register auth routes on the Flask app."""

    @app.route("/login", methods=["POST"])
    def login():
        """Login endpoint. VULNERABLE — information disclosure on error."""
        try:
            data = request.get_json()
            username = data.get("username", "")
            password = data.get("password", "")

            if not username or not password:
                return jsonify({"error": "Missing credentials"}), 400

            db = app.extensions.get("db")
            if db is None:
                from app import get_db
                db = get_db()

            cursor = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            )
            user = cursor.fetchone()

            if user is None:
                # BAD: reveals that the username doesn't exist
                return jsonify({"error": f"User '{username}' does not exist"}), 401

            password_hash = hash_password(password)
            # In a real app we'd compare against a stored hash column
            return jsonify({"message": f"Welcome, {username}!", "role": user["role"]})

        except Exception as e:
            # VULNERABILITY: Stack trace leaked to client (information disclosure)
            return jsonify({
                "error": "Internal server error",
                "details": str(e),
                "trace": traceback.format_exc()
            }), 500

    @app.route("/api/admin")
    def admin_endpoint():
        """Admin API. VULNERABLE — token comparison in source."""
        token = request.headers.get("Authorization", "")
        # BAD: hardcoded token comparison
        if token != f"Bearer {INTERNAL_API_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 403
        return jsonify({"data": "Sensitive admin information"})
