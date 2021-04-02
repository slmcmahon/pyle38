from __future__ import annotations

import json
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Union

from ..client import Client
from ..client import Command
from ..client import SubCommand
from ..responses import JSONResponse
from .executable import Compiled
from .executable import Executable


class Set(Executable):
    _key: str
    _id: str
    _ex: Optional[int] = None
    _nx_or_xx: Optional[Union[Literal["NX", "XX"]]] = None
    _input: Optional[
        Sequence[
            Union[
                Literal["POINT", "OBJECT", "BOUNDS", "HASH", "STRING"], str, float, int
            ]
        ]
    ]

    def __init__(self, client: Client, key: str, id: str) -> None:
        super().__init__(client)

        self.key(key).id(id)

    def key(self, value: str) -> Set:
        self._key = value

        return self

    def id(self, value: str) -> Set:
        self._id = value

        return self

    def ex(self, seconds: int) -> Set:
        if seconds:
            self._ex = seconds

        return self

    def nx(self, flag: bool = True) -> Set:
        if flag:
            self._nx_or_xx = "NX"

        return self

    def xx(self, flag: bool = True) -> Set:
        if flag:
            self._nx_or_xx = "XX"

        return self

    def object(self, value: dict) -> Set:
        self._input = ["OBJECT", json.dumps(value)]

        return self

    def point(self, lat: float, lon: float) -> Set:
        self._input = ["POINT", lat, lon]

        return self

    def bounds(self, min_lat: float, min_lon: float, max_lat: float, max_lon) -> Set:
        self._input = ["BOUNDS", min_lat, min_lon, max_lat, max_lon]

        return self

    def hash(self, value: str) -> Set:
        self._input = ["HASH", value]

        return self

    def string(self, value: str) -> Set:
        self._input = ["STRING", value]

        return self

    def compile(self) -> Compiled:

        return [
            Command.SET.value,
            [
                self._key,
                self._id,
                *([SubCommand.EX.value, self._ex] if self._ex else []),
                *([self._nx_or_xx] if self._nx_or_xx else []),
                *(self._input if self._input else []),
            ],
        ]

    async def exec(self) -> JSONResponse:  # type: ignore
        return JSONResponse(**(await self.client.command(*self.compile())))
