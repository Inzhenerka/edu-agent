import sympy as sp
from sympy.parsing.sympy_parser import (
    standard_transformations,
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
)
from sympy.core.sympify import SympifyError
from langchain.tools import tool
from loguru import logger


@tool
def solve_formula(formula_str: str) -> str:
    """Вычисляет или преобразует, упрощает математическое выражение.
    Используй этот инструмент, когда пользователь прислал математическое выражение или пример:
    арифметика, дроби, степени, корни, скобки и символьные выражения.
    Не используй для обычных теоретических вопросов без формулы.

    Аргументы:
        formula_str: математическое выражение, которое нужно вычислить или преобразовать
    """
    logger.debug('Solving formula: ' + formula_str)
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
        return "Не удалось разобрать формулу"
    return sp.sstr(sp.simplify(expression))
