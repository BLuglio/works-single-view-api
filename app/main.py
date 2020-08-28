from flask import Flask, session
import os
from pathlib import Path
import sys
import settings

def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret key"

    app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = settings.DOWNLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = settings.ALLOWED_EXTENSIONS

    # app.url_map.strict_slashes = False
    with app.app_context():
        import api

    return app

def run():
    app = create_app()
    app.run(debug=True)  # activates the reloader; set to False to deactivate it

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Error: " + str(e), flush=True)
