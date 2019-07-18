from flask import jsonify, Blueprint, Response, g, current_app
import traceback
from typing import Dict, Any

bp = Blueprint('errors', __name__)


class BaseException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if k != 'status_code'}


class InvalidArgument(BaseException):
    def __init__(self, msg: str, got: str, expected: str, status_code: int=400):
        super().__init__(status_code)
        self.error: str = msg
        self.got: str = got
        self.expected: str = expected


class ServerErrorException(BaseException):
    def __init__(self, exc):
        super().__init__(500)
        self.error = str(exc)
        tb = traceback.format_exc().replace('\n', '>>>')
        if hasattr(g, '_request_state'):
            logger = g._request_state.req_log
        else:
            logger = current_app.config[STATE_NAME].logger

        logger("Unexpected exception", traceback=tb)


@bp.app_errorhandler(InvalidArgument)
def handle_generic_error(err: BaseException) -> Response:
    resp = jsonify(err.to_dict())
    resp.status_code = err.status_code
    return resp


@bp.app_errorhandler(500)
def handle_500_response(exc):
    return handle_generic_error(ServerErrorException(exc))
