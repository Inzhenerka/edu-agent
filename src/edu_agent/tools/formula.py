import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    standard_transformations,
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
)
from sympy.core.sympify import SympifyError

_TRAILING_FORMULA_RE = re.compile(r"[0-9A-Za-z+\-*/^().,\s]+$")
_OPERATOR_RE = re.compile(r"[+\-*/^()]")


def extract_and_solve_trailing_formula(prompt: str) -> str | None:
    formula = _extract_trailing_formula(prompt)
    return _solve_formula(formula) if formula else None


def _extract_trailing_formula(prompt: str) -> str | None:
    match = _TRAILING_FORMULA_RE.search(prompt.strip())
    if match and _OPERATOR_RE.search(match.group(0)):
        return match.group(0)
    return None


def _solve_formula(formula_str: str) -> str | None:
    try:
        expression = parse_expr(
            formula_str.replace(",", "."),
            transformations=standard_transformations + (
                implicit_multiplication_application,
                convert_xor,
            ),
            evaluate=True,
        )
    except SympifyError:
        return None
    return sp.sstr(sp.simplify(expression))
