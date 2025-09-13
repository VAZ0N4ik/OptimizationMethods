from typing import Callable
from .common import SearchResult, MethodType


def create_search_result() -> SearchResult:
    """Создает пустую структуру SearchResult"""
    return SearchResult(
        method_type=MethodType.BISECT,
        iterations=0,
        function_probes=0,
        accuracy=0.0,
        result=0.0
    )


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
    
    res.method_type = MethodType.BISECT
    res.iterations = 0
    res.function_probes = 0
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