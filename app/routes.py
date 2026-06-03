from flask import Blueprint, render_template, jsonify, request
from .database import get_schema_info

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    """Render the dashboard UI."""
    return render_template("index.html")

@bp.route("/api/schema", methods=["GET"])
def get_schema():
    """API endpoint to retrieve the analytical database schema."""
    schema = get_schema_info()
    return jsonify({
        "status": "success",
        "tables": schema
    })

@bp.route("/api/query", methods=["POST"])
def query():
    """API endpoint to parse, validate, execute, and visualize queries."""
    data = request.get_json() or {}
    nl_query = data.get("query", "")
    
    if not nl_query:
        return jsonify({"status": "error", "message": "Query parameter is required"}), 400
        
    return jsonify({
        "status": "success",
        "sql": "SELECT * FROM olist_orders_dataset LIMIT 5; -- Skeleton placeholder",
        "explanation": "This is a placeholder explanation of the SQL translation.",
        "results": [],
        "visualization": None
    })
