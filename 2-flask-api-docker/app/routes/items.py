"""
Items Routes — Protected CRUD Resource
GET    /api/items        — list user's items (paginated)
POST   /api/items        — create item
GET    /api/items/<id>   — get single item
PUT    /api/items/<id>   — update item
DELETE /api/items/<id>   — delete item

All routes require Bearer JWT token.
Author: Gaurav Kumar
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.item import Item

items_bp = Blueprint("items", __name__)


@items_bp.get("")
@jwt_required()
def list_items():
    """
    List items for the authenticated user.
    Query params: page (default 1), per_page (default 20, max 100)
    """
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    pagination = (
        Item.query
        .filter_by(owner_id=user_id, is_deleted=False)
        .order_by(Item.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "items": [item.to_dict() for item in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    }), 200


@items_bp.post("")
@jwt_required()
def create_item():
    """
    Create a new item.
    Body: { "name": str, "description": str (optional), "tags": [str] (optional) }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "Field 'name' is required"}), 422

    item = Item(
        name=data["name"].strip(),
        description=data.get("description", ""),
        tags=data.get("tags", []),
        owner_id=user_id,
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 201


@items_bp.get("/<int:item_id>")
@jwt_required()
def get_item(item_id: int):
    user_id = get_jwt_identity()
    item = _get_owned_item(item_id, user_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict()), 200


@items_bp.put("/<int:item_id>")
@jwt_required()
def update_item(item_id: int):
    """Partial update — only provided fields are changed."""
    user_id = get_jwt_identity()
    item = _get_owned_item(item_id, user_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}
    if "name" in data:
        item.name = data["name"].strip()
    if "description" in data:
        item.description = data["description"]
    if "tags" in data:
        item.tags = data["tags"]

    db.session.commit()
    return jsonify(item.to_dict()), 200


@items_bp.delete("/<int:item_id>")
@jwt_required()
def delete_item(item_id: int):
    """Soft delete — record is kept in DB with is_deleted=True."""
    user_id = get_jwt_identity()
    item = _get_owned_item(item_id, user_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    item.is_deleted = True
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200


def _get_owned_item(item_id: int, user_id: int):
    """Helper: fetch item only if it belongs to the authenticated user."""
    return Item.query.filter_by(
        id=item_id, owner_id=user_id, is_deleted=False
    ).first()
