from flask import jsonify, Blueprint, Response
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


@bp.app_errorhandler(InvalidArgument)
def handle_generic_error(err: BaseException) -> Response:
    resp = jsonify(err.to_dict())
    resp.status_code = err.status_code
    return resp
