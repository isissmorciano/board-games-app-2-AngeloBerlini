from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

bp = Blueprint("main", __name__)

def init_app(app):
    app.register_blueprint(bp)

@bp.route("/")
def index():
    return render_template("index.html")

#L'app deve permettere di: 1. Creare nuovi giochi da tavolo 2. Registrare partite per un gioco esistente 3. Visualizzare la lista dei giochi 4. Visualizzare la lista delle partite di un gioco

@bp.route("/giochi")
def giochi():
    from .db import get_db
    db = get_db()
    giochi = db.execute("SELECT * FROM giochi").fetchall()
    return render_template("giochi.html", giochi=giochi)

@bp.route("/giochi/crea", methods=["GET", "POST"])
def crea_gioco():
    if request.method == "POST":
        nome = request.form["nome"]
        numero_giocatori_massimo = request.form["numero_giocatori_massimo"]
        durata_media = request.form["durata_media"]
        categoria = request.form["categoria"]

        if not nome:
            flash("Il nome è obbligatorio.")
            return redirect(url_for("main.crea_gioco"))

        from .db import get_db
        db = get_db()
        db.execute(
            "INSERT INTO giochi (nome, numero_giocatori_massimo, durata_media, categoria) VALUES (?, ?, ?, ?)",
            (nome, numero_giocatori_massimo, durata_media, categoria)
        )
        db.commit()
        flash("Gioco creato con successo!")
        return redirect(url_for("main.giochi"))

    return render_template("crea_gioco.html")

@bp.route("/giochi/<int:gioco_id>/partite")
def partite(gioco_id):
    from .db import get_db
    db = get_db()
    gioco = db.execute("SELECT * FROM giochi WHERE id = ?", (gioco_id,)).fetchone()
    if gioco is None:
        abort(404, "Gioco non trovato.")
    
    partite = db.execute("SELECT * FROM partite WHERE gioco_id = ?", (gioco_id,)).fetchall()
    return render_template("partite.html", gioco=gioco, partite=partite)

@bp.route("/giochi/<int:gioco_id>/partite/crea", methods=["GET", "POST"])
def crea_partita(gioco_id):
    from .db import get_db
    db = get_db()
    gioco = db.execute("SELECT * FROM giochi WHERE id = ?", (gioco_id,)).fetchone()
    if gioco is None:
        abort(404, "Gioco non trovato.")

    if request.method == "POST":
        data = request.form["data"]
        vincitore = request.form["vincitore"]
        punteggio_vincitore = request.form["punteggio_vincitore"]

        if not data or not vincitore or not punteggio_vincitore:
            flash("Tutti i campi sono obbligatori.")
            return redirect(url_for("main.crea_partita", gioco_id=gioco_id))

        db.execute(
            "INSERT INTO partite (gioco_id, data, vincitore, punteggio_vincitore) VALUES (?, ?, ?, ?)",
            (gioco_id, data, vincitore, punteggio_vincitore)
        )
        db.commit()
        flash("Partita registrata con successo!")
        return redirect(url_for("main.partite", gioco_id=gioco_id))

    return render_template("crea_partita.html", gioco=gioco)


