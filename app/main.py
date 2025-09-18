# app/distance.py
from __future__ import annotations
from typing import Union

Number = Union[int, float]


class Distance:
    """Representa uma distância em quilômetros."""

    def __init__(self, km: Number) -> None:
        self.km: float = float(km)

    # --------- helpers internos ---------
    @staticmethod
    def _fmt(value: float) -> str:
        # evita "20.0" em repr/str quando for inteiro exato
        return format(value, "g")

    @staticmethod
    def _to_km(other: Union["Distance", Number]) -> float:
        if isinstance(other, Distance):
            return other.km
        if isinstance(other, (int, float)):
            return float(other)
        raise TypeError(f"unsupported operand type: {type(other)!r}")

    # --------- representação ---------
    def __str__(self) -> str:
        return f"Distance: {self._fmt(self.km)} kilometers."

    def __repr__(self) -> str:
        return f"Distance(km={self._fmt(self.km)})"

    # --------- aritmética ---------
    def __add__(self, other: Union["Distance", Number]) -> "Distance":
        km = self.km + self._to_km(other)
        return Distance(km)

    def __radd__(self, other: Number) -> "Distance":
        # permite 10 + Distance(5)
        return self.__add__(other)

    def __iadd__(self, other: Union["Distance", Number]) -> "Distance":
        self.km += self._to_km(other)
        return self

    def __mul__(self, other: Number) -> "Distance":
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Distance(self.km * float(other))

    def __rmul__(self, other: Number) -> "Distance":
        # permite 3 * Distance(5)
        return self.__mul__(other)

    def __truediv__(self, other: Number) -> "Distance":
        if not isinstance(other, (int, float)):
            return NotImplemented
        if float(other) == 0.0:
            raise ZeroDivisionError("division by zero")
        # arredonda para 2 casas decimais como especificado
        return Distance(round(self.km / float(other), 2))

    # --------- comparações ---------
    def _cmp_value(self, other: Union["Distance", Number]) -> float:
        return self._to_km(other)

    def __lt__(self, other: Union["Distance", Number]) -> bool:
        return self.km < self._cmp_value(other)

    def __le__(self, other: Union["Distance", Number]) -> bool:
        return self.km <= self._cmp_value(other)

    def __gt__(self, other: Union["Distance", Number]) -> bool:
        return self.km > self._cmp_value(other)

    def __ge__(self, other: Union["Distance", Number]) -> bool:
        return self.km >= self._cmp_value(other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float, Distance)):
            return self.km == self._to_km(other)  # type: ignore[arg-type]
        return NotImplemented  # permite comparação simétrica com tipos estranhos
