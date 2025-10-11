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

    res.accuracy = eps

    while abs(rhs - lhs) > 2 * eps and res.iterations < max_iters:
        x_c = (lhs + rhs) / 2
        x_1 = x_c - eps
        x_2 = x_c + eps
        
        f_1 = fun(x_1)
        f_2 = fun(x_2)
        res.function_probes += 2
        
        if f_1 > f_2:
            lhs = x_c
        else:
            rhs = x_c
            
        res.iterations += 1
    
    res.result = (lhs + rhs) / 2