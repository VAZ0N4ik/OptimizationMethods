from typing import Callable
from .common import SearchResult

# Константы золотого сечения
PSI = 0.61803398874989484820  # (√5 - 1) / 2
PHI = 1.61803398874989484820  # (√5 + 1) / 2

def golden_ratio(
    res: SearchResult,
    fun: Callable[[float], float],
    lhs: float,
    rhs: float,
    eps: float,
    max_iters: int
) -> None:

    if lhs > rhs:
        lhs, rhs = rhs, lhs

    
    # Определяем левую и правую точку разбиения отрезка
    x_r = lhs + PSI * (rhs - lhs)
    x_l = rhs - PSI * (rhs - lhs)
    
    # Измерения целевой функции в точках x_l и x_r
    f_l = fun(x_l)
    f_r = fun(x_r)
    res.function_probes += 2
    
    # Основной цикл поиска
    while abs(rhs - lhs) > 2 * eps and res.iterations < max_iters:
        if f_l > f_r:
            # Преобразуем промежуток неопределённости: [x_l, rhs]
            lhs = x_l
            x_l = x_r
            f_l = f_r
            x_r = lhs + PSI * (rhs - lhs)
            f_r = fun(x_r)
            res.function_probes += 1
        else:
            # Преобразуем промежуток неопределённости: [lhs, x_r]
            rhs = x_r
            x_r = x_l
            f_r = f_l
            x_l = rhs - PSI * (rhs - lhs)
            f_l = fun(x_l)
            res.function_probes += 1
            
        res.iterations += 1
    
    res.result = (lhs + rhs) / 2
    res.accuracy = rhs - lhs