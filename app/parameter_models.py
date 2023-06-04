from typing import Literal

from pydantic import BaseModel


class Channel(BaseModel):
    id: Literal[1, 2, 3, 4]
    current: str
    voltage: str
