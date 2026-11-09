from math import sqrt, log


class Scalar:
    def __init__(self, value: float, name: str | None = None):
        self.value: float = float(value)
        self.name: str = name if isinstance(name, str) else str(value)
        self._error: float = 0.0
        self.error: float = 0.0
        self._dep: dict[Scalar, float] = {}

    def __repr__(self):
        return f"Scalar({self.name}: {self.value:.3g} ± {self.error:.3g})"

    def _value_repr(self):
        return f"{self.value:.3g}"

    def _error_repr(self):
        return f"{self.error:.3g}"

    def _name_repr(self):
        return self.name

    def _parentheses(self):
        self.name = f"({self.name})"
        return self

    def __call__(self):
        self._parentheses()
        return self

    def setError(self, error: float):
        self._error = error
        self._dep[self] = 1.0
        self._update_error()
        return self

    def setName(self, name: str) -> Scalar:
        self.name = name
        return self

    def _update_error(self):
        new = sqrt(
            sum(
                [
                    (dependencie._error * round(diff, 14)) ** 2
                    for (dependencie, diff) in self._dep.items()
                ]
            )
        )
        self.error = new
        return new

    def __add__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out_value = self.value + other.value
        out_name = f"{self.name} + {other.name}"
        out = Scalar(out_value, out_name)

        uniques = set(self._dep.keys()) | set(other._dep.keys())
        for u in uniques:
            out._dep[u] = self._dep.get(u, 0.0) + other._dep.get(u, 0.0)
        out._update_error()
        return out

    def __radd__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out = self + other
        out.name = f"{other.name} + {self.name}"
        return out

    def __mul__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out_value = self.value * other.value
        out_name = f"{self.name} * {other.name}"
        out = Scalar(out_value, out_name)

        uniques = set(self._dep.keys()) | set(other._dep.keys())
        for u in uniques:
            out._dep[u] = (other.value * self._dep.get(u, 0.0)) + (
                self.value * other._dep.get(u, 0.0)
            )
        out._update_error()
        return out

    def __rmul__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out = self * other
        out.name = f"{other.name} * {self.name}"
        return out

    def __neg__(self):
        out = self * (-1)
        out.name = f"- {self.name}"
        return out

    def __sub__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out = self + (-other)
        out.name = f"{self.name} - {other.name}"
        return out

    def __rsub__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out = other + (-self)
        out.name = f"{other.name} - {self.name}"
        return out

    def __truediv__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out_value = self.value / other.value
        out_name = f"{self.name} / {other.name}"
        out = Scalar(out_value, out_name)

        uniques = set(self._dep.keys()) | set(other._dep.keys())
        for u in uniques:
            out._dep[u] = (self._dep.get(u, 0.0) / other.value) - (
                self.value * other._dep.get(u, 0.0) / other.value**2
            )
        out._update_error()
        return out

    def __rtruediv__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out = other / self
        out.name = f"{other.name} / {self.name}"
        return out

    def __pow__(self, other):
        if not isinstance(other, Scalar):
            other = Scalar(other, name=str(other))

        out_value = self.value**other.value
        out_name = f"{self.name} ** {other.name}"
        out = Scalar(out_value, out_name)

        uniques = set(self._dep.keys()) | set(other._dep.keys())
        for u in uniques:
            out._dep[u] = other.value * (self.value ** (other.value - 1)) * self._dep.get(
                u, 0.0
            ) + log(self.value) * (self.value**other.value) * other._dep.get(u, 0.0)

        out._update_error()
        return out
