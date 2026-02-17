import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuriamo il percorso del database
    app.config["DATABASE"] = os.path.join(app.instance_path, "video_app.sqlite")

    # Assicuriamoci che la cartella instance esista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Importiamo e inizializziamo il modulo per il database
    from . import main
    main.init_app(app)

    # Importiamo e registriamo i blueprint (le "sezioni" dell'app)
    from . import routes
    app.register_blueprint(routes.bp)

    return app

