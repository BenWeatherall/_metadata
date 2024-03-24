from pydantic import BaseModel, model_validator, computed_field
from typing import Optional, Any

class EnvVar(BaseModel):
    name: str

    @property
    def is_required(self) -> bool:
        return True

    @property
    def has_default(self) -> bool:
        return False

    @property
    def default(self) -> Optional[str]:
        return None

    def __hash__(self) -> int:
        return self.name.__hash__()


class EnvironVar(EnvVar):
    pass


class GetEnvVar(EnvVar):
    default: Optional[str] = 'None'

    @property
    def is_required(self) -> bool:
        return False

    @property
    def has_default(self) -> bool:
        return True
