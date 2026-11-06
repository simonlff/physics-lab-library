from scalar import Scalar
from vector import Vector, MeanOptions, PROPAGATED, SEM, BOTH
from typing import Any, Self, override


class Measurement(Vector):
    def __init__(
        self,
        data: float | Scalar | list[float] | list[Scalar],
        name: str | None = None,
        unit: str | None = None,
    ):
        super().__init__(data, name)
        self.unit: str | None = unit

        def hook(_self: Measurement, _other: Vector, out: Self, op: str):
            _other_unit = getattr(_other, "unit", None)
            match op:
                case "+":
                    if _self.unit != _other_unit:
                        print(
                            f"WARNING: Adding '{_self.name}' of unit '{_self.unit}' to '{_other.name}' of unit '{_other_unit}'."
                        )
                        out.unit = "Bad Unit"
                    else:
                        out.unit = _self.unit
                case "*":
                    # print("super().__mul__() called")
                    if _self.unit == None:
                        out.unit = _other_unit
                    elif _other_unit == None:
                        out.unit = _self.unit
                    else:
                        out.unit = f"{_self.unit} * {_other_unit}"
                case "/":
                    if _self.unit == None:
                        out.unit = f"1 / {_other_unit}"
                    elif _other_unit == None:
                        out.unit = _self.unit
                    else:
                        out.unit = f"{_self.unit} / {_other_unit}"
                case "**":
                    if _other_unit != None:
                        print(f"WARNING: Exponent '{_other.name}' has a unit '{_other_unit}'.")
                        out.unit = "Bad Unit"
                    else:
                        out.unit = f"{_self.unit}**{_other.name}"

        self._hook = hook

    def _new(self, items, name):
        obj = super()._new(items, name)
        obj.unit = None
        obj._hook = self._hook
        return obj

    @override
    def __repr__(self):
        if self.unit != None:
            return f"Measurement({self.name}: {self._value_repr()} ± {self._error_repr()}, [{self.unit}])"
        else:
            return f"Measurement({self.name}: {self._value_repr()} ± {self._error_repr()})"

    # def setError(self, error: float | list[float]):
    #     super().setError(error)
    #     return self

    def setUnit(self, unit: str):
        self.unit = unit
        return self

    # @override
    # def setError(self, error: float | list[float]):
    #     print(
    #         f"WARNING: Using method 'Vector.setError()' on object of derived Class 'Measurement'. Use 'randError()' instead."
    #     )
    #     super().setError(error)
    #     return self

    @override
    def __call__(self):
        out = super().__call__()
        out.unit = f"({out.unit})"
        return out

    @override
    def mean(self, mean_options: MeanOptions = MeanOptions.PROPAGATED):
        mean = super().mean(mean_options)
        out = self._new([mean], mean.name)
        out.unit = self.unit
        return out
