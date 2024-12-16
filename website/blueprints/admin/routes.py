from functools import wraps

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from blueprints.admin import bp
from utils import User, Transaction, Properties
from utils.models import Asset, db, Server


def admin_required(function):
    @wraps(function)
    def decorated_view(*args, **kwargs):
        if not current_user.admin:
            flash('You must be an admin to see this page')
            return redirect(url_for('main.index'))
        return function(*args, **kwargs)

    return decorated_view


@bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    # Users section
    user_search = request.args.get('user_search', '')
    user_page = request.args.get('user_page', 1, type=int)
    user_query = User.query.filter(
        or_(User.username.ilike(f'%{user_search}%'), User.display_name.ilike(f'%{user_search}%'))
    )
    users = user_query.paginate(page=user_page, per_page=5)  # Adjust per_page as needed

    # Servers section
    server_search = request.args.get('server_search', '')
    server_page = request.args.get('server_page', 1, type=int)
    server_query = Server.query.filter(Server.name.ilike(f'%{server_search}%'))
    servers = server_query.paginate(page=server_page, per_page=5)  # Adjust per_page as needed

    return render_template(
        'admin_index.html',
        users=users,
        user_search=user_search,
        servers=servers,
        server_search=server_search
    )


@bp.route('/admin/edit_user/<int:user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_balance":
            amount = int(request.form["balance"])
            user.balance += amount

        elif action == "remove_balance":
            amount = int(request.form["balance"])
            user.balance -= amount

        elif action == "add_property":
            property_id = int(request.form["property_id_to_add"])
            property_item = Properties.query.get(property_id)
            property_item.user_id = user.id

        elif action == "remove_property":
            property_id = int(request.form["property_id"])
            property_item = Properties.query.get(property_id)
            property_item.user_id = None

        elif action == "add_asset":
            asset_id = int(request.form["asset_id_to_add"])
            asset_item = Asset.query.get(asset_id)
            asset_item.user_id = user.id

        elif action == "remove_asset":
            asset_id = int(request.form["asset_id"])
            asset_item = Asset.query.get(asset_id)
            asset_item.user_id = None

        elif action == "add_server":
            server_id = int(request.form["server_id_to_add"])
            server_item = Server.query.get(server_id)
            user.servers.append(server_item)

        elif action == "remove_server":
            server_id = int(request.form["server_id"])
            server_item = Server.query.get(server_id)
            user.servers.remove(server_item)

        db.session.commit()
        return redirect(url_for("admin.test_edit_user", user_id=user_id))

    # Load available properties, assets, and servers for management
    available_properties = Properties.query.filter(Properties.user_id.is_(None)).all()
    available_assets = Asset.query.filter(Asset.user_id.is_(None)).all()
    available_servers = Server.query.all()

    return render_template(
        "edit_user.html",
        user=user,
        available_properties=available_properties,
        available_assets=available_assets,
        available_servers=available_servers
    )


@bp.route('/manage_servers', methods=['POST'])
def manage_servers():
    action = request.form.get('server_action')

    if action == 'add_server':
        # Create a new server
        server_name = request.form['server_name']
        server_map = request.form['server_map']
        new_server = Server(name=server_name, map=server_map)
        db.session.add(new_server)
        db.session.commit()
        return redirect(url_for('admin.index'))

    elif action == 'delete_server':
        # Remove a server
        server_id = request.form['server_id']
        server = Server.query.get_or_404(server_id)
        db.session.delete(server)
        db.session.commit()
        return redirect(url_for('admin.index'))


@bp.route('/manage_properties', methods=['POST'])
def manage_properties():
    action = request.form.get('property_action')

    if action == 'add_property':
        # Create a new property
        property_price = request.form['property_price']
        property_size = request.form['property_size']
        new_property = Properties(price=property_price, size=property_size, server_id=None, user_id=None)
        db.session.add(new_property)
        db.session.commit()
        return redirect(url_for('admin.index'))

    elif action == 'delete_property':
        # Remove a property
        property_id = request.form['property_id']
        property_item = Properties.query.get_or_404(property_id)
        db.session.delete(property_item)
        db.session.commit()
        return redirect(url_for('admin.index'))


@bp.route('/add_server', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        name = request.form.get('name')
        map = request.form.get('map')  # Assuming 'map' is a field in your Server model

        if name and map:  # Basic validation
            new_server = Server(name=name, map=map)
            db.session.add(new_server)
            db.session.commit()
            return redirect(url_for('admin.index'))  # Redirect back to admin dashboard

    return render_template('add_server.html')  # Template for the add server form


