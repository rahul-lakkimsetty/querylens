from flask import Blueprint, render_template, jsonify, request

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """Render the dashboard UI."""
    return render_template("index.html")

@bp.route("/api/query", methods=["POST"])
def query():
    """Handle English-to-SQL requests."""
    return jsonify({"status": "not_implemented", "message": "API endpoint skeleton"})
