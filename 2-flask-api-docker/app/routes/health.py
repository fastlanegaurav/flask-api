"""Health check endpoints — used by ALB target groups and monitoring."""

from flask import Blueprint, jsonify
from app import db
import sqlalchemy

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """
    Basic liveness check — returns 200 if app is running.
    ALB checks this every 30s.
    """
    return jsonify({"status": "healthy"}), 200


@health_bp.get("/health/ready")
def readiness():
    """
    Readiness check — verifies DB connectivity before accepting traffic.
    Returns 503 if DB is unreachable (prevents bad traffic routing).
    """
    try:
        db.session.execute(sqlalchemy.text("SELECT 1"))
        return jsonify({"status": "ready", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not_ready", "database": "unreachable", "error": str(e)}), 503
