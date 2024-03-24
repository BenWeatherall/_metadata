from pydantic import BaseModel
from typing import Optional

class Config(BaseModel):
    include_venv: Optional[bool] = False
