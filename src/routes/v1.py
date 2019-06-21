from flask import (
    Blueprint, request, current_app, jsonify, Response, make_response, g
)

from routes.custom_exceptions import InvalidArgument
from constants import STATE_NAME

from uuid import uuid4
from simplog import refine_logger
from state import RequestState


import http


bp = Blueprint('v1', __name__, url_prefix='/v1')


@bp.before_request
def on_request_received():
    # you may want to copy this if/when you do a v2 (or switch to before_app_request to capture all requests)
    ctx = str(uuid4())
    req_log = refine_logger(current_app.config[STATE_NAME].logger, context=ctx)
    req_log("Received Request", method=request.method, endpoint=request.full_path, 
            query=request.query_string, body=request.get_json())
    g._request_state = RequestState(req_log)


@bp.after_request
def on_request_complete(resp):
    g._request_state.req_log("Request Complete", response_code=resp.status_code, body=resp.data)

    return resp


def jsonify_no_content() -> Response:
    # from https://www.erol.si/2018/03/flask-return-204-no-content-response/
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
 
    return response
