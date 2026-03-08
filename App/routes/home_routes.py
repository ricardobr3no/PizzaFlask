from flask import request, render_template, Blueprint

home_bp = Blueprint("home", __name__)


@home_bp.route("/home", methods=["GET"])
def home():
    return render_template("home.html")
