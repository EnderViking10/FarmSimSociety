from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from functools import wraps
from models import Admin, User, Transaction, Properties, Asset, Server, Auction, Log, db
from utils.forms import ServerForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Utility functions
def create_entity(model, **kwargs):
    """Helper to create a new entity and commit to the database."""
    entity = model(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity

def delete_entity(model, entity_id):
    """Helper to delete an entity and commit to the database."""
    entity = model.query.get_or_404(entity_id)
    db.session.delete(entity)
    db.session.commit()

# Admin authentication decorator
def admin_required(function):
    """Decorator to restrict access to admin users."""
    @wraps(function)
    def decorated_view(*args, **kwargs):
        if not current_user.admin:
            flash("You must be an admin to access this page.")
            return redirect(url_for("main.index"))
        return function(*args, **kwargs)
    return decorated_view

# Admin Login
@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(username=data.get("username")).first()
    if admin and check_password_hash(admin.password, data.get("password", "")):
        return jsonify({"message": "Login successful", "admin_id": admin.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Ban User and Move Assets to Auction
@admin_bp.route("/ban", methods=["POST"])
@login_required
@admin_required
def ban_user():
    data = request.json
    try:
        # Fetch the user to be banned
        user = User.query.get(data["player_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Add a log entry for the ban action
        log = Log(action="Ban User", admin_id=data["admin_id"], details=f"User {user.id} banned")
        db.session.add(log)

        # Handle user assets: Move all assets to auction
        for asset in user.assets:  # Assuming a relationship between User and Asset models
            auction_item = Auction(
                asset_id=asset.id,
                starting_bid=asset.estimated_value or 100,  # Default bid value if not available
                status="active",
            )
            db.session.add(auction_item)
            asset.user_id = None  # Remove ownership from user

        # Commit all changes
        db.session.commit()

        return jsonify({"message": f"User {data['player_id']} banned successfully. All assets moved to auction."}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of any failure
        return jsonify({"error": str(e)}), 500

# Admin Dashboard
@admin_bp.route("/", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    # Users Section
    user_search = request.args.get("user_search", "")
    user_page = request.args.get("user_page", 1, type=int)
    users = User.query.filter(
        or_(
            User.username.ilike(f"%{user_search}%"),
            User.display_name.ilike(f"%{user_search}%")
        )
    ).paginate(page=user_page, per_page=5)

    # Servers Section
    server_search = request.args.get("server_search", "")
    server_page = request.args.get("server_page", 1, type=int)
    servers = Server.query.filter(
        Server.name.ilike(f"%{server_search}%")
    ).paginate(page=server_page, per_page=5)

    return render_template(
        "admin_index.html",
        users=users,
        user_search=user_search,
        servers=servers,
        server_search=server_search,
    )

# Edit User
@admin_bp.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        action = request.form.get("action")
        amount = int(request.form.get("balance", 0))

        if action == "add_balance":
            user.balance += amount
        elif action == "remove_balance":
            user.balance -= amount
        elif action == "add_property":
            property_item = Properties.query.get(int(request.form["property_id_to_add"]))
            property_item.user_id = user.id
        elif action == "remove_property":
            property_item = Properties.query.get(int(request.form["property_id"]))
            property_item.user_id = None
        elif action == "add_asset":
            asset_item = Asset.query.get(int(request.form["asset_id_to_add"]))
            asset_item.user_id = user.id
        elif action == "remove_asset":
            asset_item = Asset.query.get(int(request.form["asset_id"]))
            asset_item.user_id = None
        elif action == "add_server":
            server_item = Server.query.get(int(request.form["server_id_to_add"]))
            user.servers.append(server_item)
        elif action == "remove_server":
            server_item = Server.query.get(int(request.form["server_id"]))
            user.servers.remove(server_item)

        db.session.commit()
        return redirect(url_for("admin.edit_user", user_id=user_id))

    available_properties = Properties.query.filter(Properties.user_id.is_(None)).all()
    available_assets = Asset.query.filter(Asset.user_id.is_(None)).all()
    available_servers = Server.query.all()

    return render_template(
        "edit_user.html",
        user=user,
        available_properties=available_properties,
        available_assets=available_assets,
        available_servers=available_servers,
    )

# Manage Servers
@admin_bp.route("/manage_servers", methods=["POST"])
@login_required
@admin_required
def manage_servers():
    action = request.form.get("server_action")
    if action == "add_server":
        create_entity(Server, name=request.form["server_name"], map=request.form["server_map"])
    elif action == "delete_server":
        delete_entity(Server, request.form["server_id"])
    return redirect(url_for("admin.index"))

# Manage Properties
@admin_bp.route("/manage_properties", methods=["POST"])
@login_required
@admin_required
def manage_properties():
    action = request.form.get("property_action")
    if action == "add_property":
        create_entity(
            Properties,
            price=request.form["property_price"],
            size=request.form["property_size"],
            server_id=None,
            user_id=None,
        )
    elif action == "delete_property":
        delete_entity(Properties, request.form["property_id"])
    return redirect(url_for("admin.index"))

# Add Server
@admin_bp.route("/add_server", methods=["GET", "POST"])
@login_required
@admin_required
def add_server():
    form = ServerForm()
    if form.validate_on_submit():
        create_entity(Server, name=form.name.data, map=form.map.data)
        return redirect(url_for("admin.index"))
    return render_template("add_server.html", form=form)
