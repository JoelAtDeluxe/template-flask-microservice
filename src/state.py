from project_config import ProjectConfig


class State(object):
    def __init__(self, config: ProjectConfig, logger):
        self.config = config
        self.logger = logger


class RequestState(object):
    def __init__(self, request_logger):
        self.req_log = request_logger