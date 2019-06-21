from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Any


@dataclass(repr=False, frozen=True)
class ProjectConfig:
    app_version: str
    app_environment: str

    @classmethod
    def from_dict(cls, environment: Dict[str, str]):
        app_version = environment.get('APP_VERSION', 'unspecified')
        app_environment = environment.get('APP_ENVIRONMENT', 'local')

        return cls(app_version=app_version, app_environment=app_environment)

    def _is_secret(self):
        return []

    def get_config(self) -> Dict[str, Any]:
        d = asdict(self)
        secret_fields = self._is_secret()
        for k in secret_fields:
            d[k] = "***"
        return d

    def __repr__(self) -> str:
        fields = ", ".join([f"{k}:'{v}'" for k, v in self.get_config().items()])
        return f"{self.__class__.__name__}({fields})" 
