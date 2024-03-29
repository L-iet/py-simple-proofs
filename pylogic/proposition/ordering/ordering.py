from typing import Protocol, TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pylogic.proposition.ordering.greaterthan import GreaterThan
    from pylogic.proposition.ordering.lessthan import LessThan
from sympy import Basic

SympyExpression = Basic | int | float


class _Ordering(Protocol):
    @classmethod
    def _multiply_by(
        cls,
        instance: "GreaterThan | LessThan",
        x: SympyExpression,
        p: "GreaterThan | LessThan",
        _sign: str = "positive",
    ) -> Self:
        from pylogic.proposition.ordering.greaterthan import GreaterThan
        from pylogic.proposition.ordering.lessthan import LessThan

        assert p.is_proven, f"{p} is not proven"
        if (_sign == "positive" and isinstance(p, LessThan)) or (
            _sign == "negative" and isinstance(p, GreaterThan)
        ):
            assert p.left == 0 and p.right == x, f"{p} does not say that {x} is {_sign}"
        elif (_sign == "positive" and isinstance(p, GreaterThan)) or (
            _sign == "negative" and isinstance(p, LessThan)
        ):
            assert p.left == x and p.right == 0, f"{p} does not say that {x} is {_sign}"
        if _sign == "positive":
            new_p = cls(x * instance.left, x * instance.right)  # type: ignore
        elif _sign == "negative":
            new_p = cls(x * instance.right, x * instance.left)  # type: ignore
        else:
            raise ValueError(f"Invalid sign: {_sign}")
        return new_p

    @classmethod
    def _mul(
        cls, instance: "GreaterThan | LessThan", other: SympyExpression
    ) -> "LessThan":
        if isinstance(other, int) or isinstance(other, float):
            sign = "positive" if other > 0 else "negative"
            proof = (
                GreaterThan(other, 0, _is_proven=True)
                if sign == "positive"
                else LessThan(other, 0, _is_proven=True)
            )
            return cls._multiply_by(instance, other, proof, _sign=sign)  # type: ignore
        else:
            raise ValueError(
                f"Cannot multiply {instance} by {other}, use multiply_by_positive or multiply_by_negative"
            )
