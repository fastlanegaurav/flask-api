"""
Auth Routes — JWT-based Authentication
POST /api/auth/register  — create account
POST /api/auth/login     — get access + refresh tokens
POST /api/auth/refresh   — rotate access token
POST /api/auth/logout    — revoke token (blocklist)

Author: Gaurav Kumar
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app import db, limiter
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# Blocklist for logged-out tokens (use Redis in production)
TOKEN_BLOCKLIST: set = set()


@auth_bp.post("/register")
@limiter.limit("5 per minute")
def register():
    """
    Register a new user.
    Body: { "email": str, "password": str, "name": str }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required = ["email", "password", "name"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 422

    if User.query.filter_by(email=data["email"].lower()).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(email=data["email"].lower(), name=data["name"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": user.id}), 201


@auth_bp.post("/login")
@limiter.limit("10 per minute")
def login():
    """
    Authenticate and return JWT tokens.
    Body: { "email": str, "password": str }
    Returns: { access_token, refresh_token }
    """
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Rotate access token using a valid refresh token."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    """Revoke current token (adds JTI to blocklist)."""
    jti = get_jwt()["jti"]
    TOKEN_BLOCKLIST.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
