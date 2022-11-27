from flask import Blueprint, render_template, redirect, url_for, jsonify, request, send_from_directory, flash, make_response
from flask_jwt import jwt_required, current_identity
from flask_login import login_user, login_required, LoginManager

from App.controllers import (
    create_user,
    get_user,
    get_all_users,
    get_all_users_json,
    get_users_by_access,
    delete_user,
    get_user_by_email,
    authenticate,
    login_user
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


@user_views.route("/users", methods=["GET"])
def get_user_page():
    users = get_all_users()
    return render_template("users.html", users=users)


@user_views.route("/static/users", methods=["GET"])
def static_user_page():
    return send_from_directory("static", "static-user.html")


@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify_user_action():
    return jsonify(
        {
            "message": f"email: {current_identity.email}, id : {current_identity.id}"
        }
    )


# Sign up route
@user_views.route("/api/users", methods=["POST"])
def signup_action():
    data = request.json
    if data:
        if get_user_by_email(data["email"]):
            return jsonify({"message": "email taken."}), 400
        user = create_user(
            email=data["email"], password=data["password"], firstName=data["firstName"], lastName=data["lastName"], access=data["access"]
        )
        if user:
            return jsonify({"message": f"user {data['email']} created"}), 201
        return jsonify({"message": "User not created"}), 400


# Sign up route
@user_views.route("/signup", methods=["POST"])
def signup_page():
    data = request.form
    if get_user_by_email(data["email"]):
        flash("email taken")
    else:
        user = create_user(
            email=data["email"], password=data["password"], firstName=data["firstName"], lastName=data["lastName"], access=1
        )   
        if user:
            flash("user " + data["email"] + " created")
            current_identity=user
            login_user(current_identity)
            return render_template("dashboard", data=data, user=user)
        else:
            flash("User not created")
    return render_template("auth/signup.html", data=data)


# Login route
@user_views.route('/login', methods=['POST', 'GET'])
def login():
    data =None
    if request.method == "POST":
        data = request.form
        user = authenticate(data["email"], data["password"])
        if not user:
            flash("Invalid Credentials!")
        else:
            login_user(user, remember=True)
            current_identity=user
            return render_template('index.html', user=current_identity)
    return render_template("/auth/login.html", data=data)


# Get all users route
# Must be an admin to access this route
@user_views.route("/api/users", methods=["GET"])
@jwt_required()
def get_users_action():
    if current_identity.is_admin():
        users = get_all_users_json()
        return jsonify(users), 200
    return jsonify({"message": "Access denied"}), 403


# Get all users route
# Must be an admin to access this route
@user_views.route("/admin", methods=["GET"])
@login_required
def get_users_page():
    users=None
    if current_identity.is_admin():
        users = get_all_users_json()
    return render_template("admin.html", users=users)


# Get user by id route
# Must be an admin to access this route
@user_views.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_action(user_id):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    user = get_user(user_id)
    if user:
        return jsonify(user.to_json()), 200
    return jsonify({"message": "User not found"}), 404


# Delete user route
# Must be an admin to access this route
@user_views.route("/api/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_action(user_id):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    user = get_user(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# Get user by access level route
# Must be an admin to access this route
@user_views.route("/api/users/access/<int:access_level>", methods=["GET"])
@jwt_required()
def get_user_by_access_action(access_level):
    if not current_identity.is_admin():
        return jsonify({"message": "Access denied"}), 403
    users = get_users_by_access(access_level)
    if users:
        return jsonify([user.to_json() for user in users]), 200
    return jsonify({"message": "No users found"}), 404
