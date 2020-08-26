
from flask import Flask, session
import os
from pathlib import Path
import sys

UPLOAD_FOLDER = '/Users/biagio/Desktop/works-single-view-api/app/upload'
ALLOWED_EXTENSIONS = {'csv'}

def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret key"

    # set up configuration
    # secret_config = Path(os.getcwd() + "/app/configuration/secret.conf")
    # if not secret_config.exists():
    #     raise Exception(
    #         "Configuration error: secret.conf not found in " + os.getcwd() + "/app/configuration/secret.conf")
    # else:
    #     app.config.from_pyfile(os.path.join(
    #         ".", "configuration/secret.conf"), silent=False)
    #     app.config.from_pyfile(os.path.join(
    #         ".", "configuration/settings.conf"), silent=False)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    with app.app_context():
        import routes

    return app


def run():
    app = create_app()
    app.run(debug=True)  # activates the reloader; set to False to deactivate it


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Error: " + str(e), flush=True)
