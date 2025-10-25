from typing import Callable
from .common import SearchResult

def bisect(
    res: SearchResult,
    fun: Callable[[float], float],
    lhs: float,
    rhs: float,
    eps: float,
    max_iters: int
) -> None:

    if lhs > rhs:
        lhs, rhs = rhs, lhs

    res.clear()

    while abs(rhs - lhs) > 2 * eps and res.iterations < max_iters:
        x_c = (lhs + rhs) / 2
        xl = x_c - eps/10
        xr = x_c + eps/10

        f_1 = fun(xl)
        f_2 = fun(xr)
        res.function_probes += 2

        if f_1 > f_2:
            lhs = xl
        else:
            rhs = xr

        res.iterations += 1

    res.result = (lhs + rhs) / 2
    res.accuracy = rhs - lhs