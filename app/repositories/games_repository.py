from app.db import get_db


def get_all_games():
    """
    Recupera tutti i giochi.
    """
    db = get_db()
    query = """
        SELECT giochi.id, giochi.nome, giochi.numero_giocatori_massimo, giochi.durata_media, giochi.categoria
        FROM giochi
    """
    games = db.execute(query).fetchall()
    return [dict(game) for game in games]


def get_channel_by_id(channel_id):
    """Recupera un singolo canale per ID."""
    db = get_db()
    query = """
        SELECT id, nome, numero_iscritti, categoria
        FROM giochi
        WHERE id = ?
    """
    channel = db.execute(query, (channel_id,)).fetchone()
    if channel:
        return dict(channel)
    return None


def create_channel(nome, numero_iscritti, categoria):
    """Crea un nuovo canale."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO giochi (nome, numero_iscritti, categoria) VALUES (?, ?, ?)", (nome, numero_iscritti, categoria)
    )
    db.commit()
    return cursor.lastrowid
