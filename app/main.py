from flask import Blueprint, render_template



bp = Blueprint("main", __name__)

def init_app(app):
    app.register_blueprint(bp)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/games")
def games():
    return render_template("games.html")

@bp.route("/about")
def about():
    return render_template("about.html")

