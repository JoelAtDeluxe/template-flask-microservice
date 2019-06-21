import os

from flask import Flask
from simplog import make_logger, refine_logger

from routes import v1, compliance, custom_exceptions
from state import State
from project_config import ProjectConfig
from constants import STATE_NAME


def remove_flask_logging(app: Flask) -> None:
    # See: https://gist.github.com/daryltucker/e40c59a267ea75db12b1
    import logging
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True


def build_initial_state() -> State:
    config = ProjectConfig.from_dict(os.environ)
    base_logger = refine_logger(make_logger(), app="log-reader")

    return State(config, base_logger)


def create_app() -> Flask:
    app = Flask(__name__)

    # Load environment config + access to other goodies
    app.config[STATE_NAME] = build_initial_state()

    app.register_blueprint(compliance.bp)  # Add standard apis
    app.register_blueprint(v1.bp)  # Add custom apis
    app.register_blueprint(custom_exceptions.bp)  # Add error handlers

    # tweak logging settings
    # remove_flask_logging(app)
    
    return app


if __name__ == "__main__":
    app = create_app()
    try:
        app.config[STATE_NAME].logger("App Starting")
        app.run(host="0.0.0.0", port=5000)
    finally:
        app.config[STATE_NAME].db.close()
        app.config[STATE_NAME].logger("App Exiting")
