from flask import (
    Blueprint, request, redirect, url_for, current_app, jsonify, Response
)
from constants import STATE_NAME

bp = Blueprint('compliance', __name__, url_prefix='')


@bp.route("/")
def index() -> Response:
    return oapi_docs()


@bp.route('/about/docs')
def oapi_docs() -> Response:
    return redirect(url_for('static', filename='swagger/index.html'))

@bp.route('/about/docs/swagger.json')
def swagger_json() -> Response:
    # Option 1: To return an external file:
    return redirect(url_for('static', filename="swagger.yaml"))

    # Option 2: To read from docstrings (currently doesn't work -- but this is possible)
    # return jsonify(current_app)

@bp.route('/about')
def about() -> Response:
    return jsonify({
        "version": current_app.config[STATE_NAME].config.app_version
    })


@bp.route("/config")
def echo_config() -> Response:
    """Returns a json reprensentation of the loaded configuration
    """
    return jsonify(current_app.config[STATE_NAME].config.get_config())
    