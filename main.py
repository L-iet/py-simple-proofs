from pylogic.proposition.proposition import Proposition
from pylogic.proposition.quantified.forall import Forall
from pylogic.proposition.ordering.greaterthan import GreaterThan
from pylogic.proposition.ordering.lessthan import LessThan
from pylogic.proposition.relation.equals import Equals
from pylogic.proposition.or_ import Or
from pylogic.proposition.ordering.theorems import (
    order_axiom_bf,
    absolute_value_nonnegative_f,
)
from pylogic.proposition.not_ import Not, neg
from pylogic import symbol as ps
from pylogic.variable import Variable
import sympy as sp


x = Variable("x", real=True)
xnot0: Not[Equals] = neg(Equals(sp.Abs(x), 0), True)

Px = Proposition("P", args=[x])
Py = Proposition("P", args=[ps.Symbol("y", real=True)])
forallXPx = Forall(x, Px, is_assumption=True)

# print(Py, forallXPx)
py = Py.is_special_case_of(forallXPx)
print(py.is_proven)  # True

### proof that lim_x->0 x^2 = 0

eps = Variable("eps", real=True)
eps_positive = GreaterThan(eps, 0, is_assumption=True)

absolute_x_positive = GreaterThan.is_absolute(sp.Abs(x), xnot0)
root_eps_positive = GreaterThan.is_rational_power(sp.sqrt(eps), eps_positive)
absx_lt_sqrt_eps = LessThan(sp.Abs(x), sp.sqrt(eps), is_assumption=True)
xsq_lt_eps_t_absx = absx_lt_sqrt_eps.p_multiply_by_positive(
    abs(x), GreaterThan.is_absolute(abs(x), xnot0)
)
eps_t_absx_lt_eps = absx_lt_sqrt_eps.p_multiply_by_positive(
    sp.sqrt(eps), root_eps_positive
)
xsq_lt_eps = xsq_lt_eps_t_absx.transitive(eps_t_absx_lt_eps)
lim_x_sq_at_0 = (
    xsq_lt_eps.followed_from(absx_lt_sqrt_eps)
    .p_and_reverse(root_eps_positive)
    .thus_there_exists("delta", sp.sqrt(eps), [[0], [1, 0]])
    .followed_from(eps_positive)
    .thus_forall(eps)
    .thus_forall(x)
)
# note that we also assumed that |x| != 0 above

# forall x: forall eps: [eps > 0 -> exists delta: (delta > 0 /\ [Abs(x) < delta -> x**2 < delta**2])] True
print(lim_x_sq_at_0, lim_x_sq_at_0.is_proven)

# TODO
# Implement a way to determine what equations need to hold for two propositions
# to be equivalent


###  Proving Theorem 1.2.6 (the converse statement) Understanding Analysis, 2nd Edition
# if (forall eps>0, |a-b|<eps) then a = b
a = ps.Symbol("a", real=True)
b = ps.Symbol("b", real=True)
abs_a_minus_b = sp.Abs(a - b)  # type: ignore

# We assume forall eps, eps > 0 => |a-b| < eps
premise = Forall(
    eps, GreaterThan(eps, 0).implies(LessThan(abs_a_minus_b, eps)), is_assumption=True
)
premise2 = premise.in_particular(abs_a_minus_b)

# ~ |a-b| > 0
abs_a_minus_b_is_not_pos: Not[GreaterThan] = (
    Equals(abs_a_minus_b, abs_a_minus_b)
    .by_simplification()
    .modus_ponens(order_axiom_bf(abs_a_minus_b, abs_a_minus_b))
    .modus_tollens(premise2)
)

# |a-b| = 0
abs_a_minus_b_is_0: Equals = absolute_value_nonnegative_f(abs_a_minus_b).unit_resolve(
    abs_a_minus_b_is_not_pos
)  # type: ignore

# a-b = 0
print(abs_a_minus_b_is_0.zero_abs_is_0())
# need a tactic to convert this to a=b
