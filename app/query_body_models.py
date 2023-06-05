from typing import Literal

from pydantic import BaseModel


class Channel(BaseModel):
    id: Literal[1, 2, 3, 4]


class TurnOnChannel(Channel):
    current: str
    volt: str


class TurnOffChannel(Channel):
    pass
