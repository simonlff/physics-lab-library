from scalar import Scalar
from typing import Callable, Self, Any
from enum import Enum
from math import sqrt


class MeanOptions(Enum):
    PROPAGATED = 1
    SEM = 2
    BOTH = 3


PROPAGATED = MeanOptions.PROPAGATED
SEM = MeanOptions.SEM
BOTH = MeanOptions.BOTH


class Vector:
    def __init__(self, items: float | Scalar | list[float] | list[Scalar], name: str | None = None):
        _items = items if isinstance(items, list) else [items]
        self.length: int = len(_items)
        self.items: list[Scalar] = [
            (
                item
                if isinstance(item, Scalar)
                else Scalar(item, f"{name}_{i}" if isinstance(name, str) else str(item))
            )
            for (i, item) in enumerate(_items)
        ]
        if self.length == 1:
            self.name: str = _items[0].name if isinstance(_items[0], Scalar) else str(_items[0])
        else:
            self.name = "vec"
        self.name = name if isinstance(name, str) else self.name
        self._hook: Callable[[Self, Vector, Self, str], None] = lambda self, other, out, op: None

    @classmethod
    def _new(cls, items: list[Scalar], name: str) -> Self:
        obj = cls.__new__(cls)
        obj.length = len(items)
        obj.items = items
        obj.name = name
        obj._hook = lambda self, other, out, op: None
        return obj

    @classmethod
    def _flex_new(cls, items: float | Scalar | list[float] | list[Scalar], name: str | None = None):
        obj = cls.__new__(cls)
        _items = items if isinstance(items, list) else [items]
        obj.length = len(_items)
        obj.items = [
            (
                item
                if isinstance(item, Scalar)
                else Scalar(item, f"{name}_{i}" if isinstance(name, str) else str(item))
            )
            for (i, item) in enumerate(_items)
        ]
        if obj.length == 1:
            obj.name = _items[0].name if isinstance(_items[0], Scalar) else str(_items[0])
        else:
            obj.name = "vec"
        obj.name = name if isinstance(name, str) else obj.name
        obj._hook = lambda self, other, out, op: None
        return obj

    def setError(self, error: float | list[float]):
        _error = error if isinstance(error, list) else [error]
        if len(_error) == self.length:
            for i, e in zip(self.items, _error):
                i.setError(e)
        elif len(_error) == 1:
            for i in self.items:
                i.setError(_error[0])
        else:
            raise ValueError(
                f"Error must be of length 1 or same as Vector. Expected 1 or {self.length}, got {len(_error)}."
            )
        return self

    def setName(self, name: str):
        self.name = name
        return self

    def broadcast(self, length: int):
        if self.length == length:
            return self
        elif self.length == 1:
            return Vector([self.items[0]] * length, self.name)
        else:
            raise ValueError(
                f'Self of length "{self.length}" not broadcastable to length: "{length}". Own length must be "1" or "{length}".'
            )

    def _value_repr(self):
        return f"[{" ".join([i._value_repr() for i in self.items])}]"

    def _error_repr(self):
        return f"[{" ".join([i._error_repr() for i in self.items])}]"

    def _name_repr(self):
        return [i._name_repr() for i in self.items]

    def __repr__(self):
        return f"Vector({self.name}: {self._value_repr()} ± {self._error_repr()})"

    def _rename_items(self, rename: Callable[[int, Scalar], str]):
        for i, item in enumerate(self.items):
            item.name = rename(i, item)
        return self

    def __call__(self):
        self.name = f"({self.name})"
        return self

    def __add__(self, other) -> Self:
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        if self.length >= other.length:
            out_value = [
                (s + o)() for (s, o) in zip(self.items, other.broadcast(self.length).items)
            ]
        else:
            out_value = [
                (s + o)() for (s, o) in zip(self.broadcast(other.length).items, other.items)
            ]
        out_name = f"{self.name} + {other.name}"
        out = self._new(out_value, out_name)
        self._hook(self, other, out, "+")
        return out

    def __radd__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        out = self + other
        out.name = f"{other.name} + {self.name}"
        return out

    def __mul__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        if self.length >= other.length:
            out_value = [
                (s * o)() for (s, o) in zip(self.items, other.broadcast(self.length).items)
            ]
        else:
            out_value = [
                (s * o)() for (s, o) in zip(self.broadcast(other.length).items, other.items)
            ]

        out_name = f"{self.name} * {other.name}"
        out = self._new(out_value, out_name)
        self._hook(self, other, out, "*")
        return out

    def __rmul__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        out = self * other
        out.name = f"{other.name} * {self.name}"
        return out

    def __neg__(self):
        out = self * (-1)
        out.name = f"- {self.name}"
        return out

    def __sub__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        out = self + (-other)
        out.name = f"{self.name} - {other.name}"
        return out

    def __rsub__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        out = other + (-self)
        out.name = f"{other.name} - {self.name}"
        return out

    def __truediv__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        if self.length >= other.length:
            out_value = [
                (s / o)() for (s, o) in zip(self.items, other.broadcast(self.length).items)
            ]
        else:
            out_value = [
                (s / o)() for (s, o) in zip(self.broadcast(other.length).items, other.items)
            ]

        out_name = f"{self.name} / {other.name}"
        out = self._new(out_value, out_name)
        self._hook(self, other, out, "/")
        return out

    def __rtruediv__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        out = other / self
        out.name = f"{other.name} / {self.name}"
        return out

    def __pow__(self, other):
        if not isinstance(other, Vector):
            other = self._flex_new(
                other, name=other.name if isinstance(other, Scalar) else str(other)
            )

        if self.length >= other.length:
            out_value = [(s**o)() for (s, o) in zip(self.items, other.broadcast(self.length).items)]
        else:
            out_value = [
                (s**o)() for (s, o) in zip(self.broadcast(other.length).items, other.items)
            ]
        out_name = f"{self.name} ** {other.name}"
        out = self._new(out_value, out_name)
        self._hook(self, other, out, "**")
        return out

    def sum(self):
        out = sum(self.items)
        if isinstance(out, Scalar):
            return out.setName(f"Σ({self.name})")
        else:
            return Scalar(0, "Σ0")

    def mean(self, mean_options: MeanOptions = MeanOptions.PROPAGATED):
        match mean_options:
            case MeanOptions.PROPAGATED:
                return (self.sum() / self.length).setName(f"μ{self.name}")
            case MeanOptions.SEM:
                mean = sum([i.value for i in self.items]) / self.length
                stat = sqrt(
                    sum([(i.value - mean) ** 2 for i in self.items])
                    / (self.length**2 - self.length)
                )
                out = self.sum() / self.length
                out._dep = {}
                return out.setError(stat).setName(f"μ{self.name}")
            case MeanOptions.BOTH:
                mean = sum([i.value for i in self.items]) / self.length
                stat = sqrt(
                    sum([(i.value - mean) ** 2 for i in self.items])
                    / (self.length**2 - self.length)
                )
                return (self.sum() / self.length).setError(stat).setName(f"μ{self.name}")
