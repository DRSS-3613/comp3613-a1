from flask import Blueprint, redirect, url_for, render_template, request, send_from_directory

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index_page():
    return render_template("auth/signup.html")

@index_views.route("/signup", methods=["GET"])
def signup_page():
    return render_template("auth/signup.html")

