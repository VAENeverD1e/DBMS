"""
Label routes for label operations
"""

from flask import Blueprint, request, jsonify
from app.utils.decorators import guest_optional
from .services import LabelService


# Create Blueprint
labels_bp = Blueprint("labels", __name__, url_prefix="/api/labels")


@labels_bp.route("/", methods=["GET"])
@guest_optional
def get_labels(user_id=None):
    """
    Get all record labels

    Returns:
        200: List of labels
        500: Server error
    """
    try:
        success, result = LabelService.get_all_labels()

        if not success:
            return jsonify({"error": result}), 500

        return jsonify({"labels": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@labels_bp.route("/<int:label_id>", methods=["GET"])
@guest_optional
def get_label(label_id, user_id=None):
    """
    Get label details by label ID

    Returns:
        200: Label details
        404: Label not found
        500: Server error
    """
    try:
        success, result = LabelService.get_label_by_id(label_id)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify({"label": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@labels_bp.route("/<int:label_id>/artists", methods=["GET"])
@guest_optional
def get_label_artists(label_id, user_id=None):
    """
    Get all artists belonging to a label

    Returns:
        200: List of artists
        404: Label not found
        500: Server error
    """
    try:
        success, result = LabelService.get_label_artists(label_id)

        if not success:
            status_code = 404 if "not found" in result.lower() else 500
            return jsonify({"error": result}), status_code

        return jsonify({"artists": result}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

