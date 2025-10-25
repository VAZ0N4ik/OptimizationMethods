from typing import Callable, Tuple
from .common import SearchResult


def fibonacci_next(fib_curr: float, fib_next: float) -> tuple[float, float]:
    return fib_next, fib_next + fib_curr


def fibonacci_prev(fib_curr: float, fib_next: float) -> tuple[float, float]:
    return fib_next - fib_curr, fib_curr


def get_fibonacci_numbers(length_ratio: float) -> Tuple[int, float, float]:
    """
    Вычисляет пару чисел Фибоначчи для заданной длины отрезка и точности.

    Args:
        length_ratio: Отношение длины отрезка к точности |rhs - lhs| / eps
        eps: Точность поиска

    Returns:
        Tuple[n, L_n_minus_1, L_n]: номер и пара чисел Фибоначчи
    """
    # Генерация чисел Фибоначчи
    fib_curr, fib_next = 1.0, 1.0
    iterations = 0

    while fib_curr < length_ratio:
        fib_curr, fib_next = fibonacci_next(fib_curr, fib_next)
        iterations += 1

    return iterations, fib_curr, fib_next

def fibonacci(
    res: SearchResult,
    fun: Callable[[float], float],
    lhs: float,
    rhs: float,
    eps: float
) -> None:
    """
    Метод Фибоначчи для поиска экстремума функции.

    Args:
        res: Структура для сохранения результатов поиска
        fun: Целевая функция для минимизации
        lhs: Левая граница промежутка неопределённости
        rhs: Правая граница промежутка неопределённости
        eps: Точность поиска
        max_iters: Максимальное количество итераций
    """
    if lhs > rhs:
        lhs, rhs = rhs, lhs
    res.clear()
    # Определяем пару чисел Фибоначчи
    length = rhs - lhs
    n, fib_curr, fib_next = get_fibonacci_numbers(length / eps)

    # Определяем левую и правую точки разбиения отрезка
    x_r = lhs + (fib_curr / fib_next) * (rhs - lhs)
    x_l = lhs + ((fib_next - fib_curr) / fib_next) * (rhs - lhs)

    # Измерения целевой функции в точках x_l и x_r
    f_l = fun(x_l)
    f_r = fun(x_r)
    res.function_probes += 2

    # Основной цикл поиска
    for _ in range(n):
        # Сдвиг пары чисел Фибоначчи: L_{n-1}, L_n → L_{n-2}, L_{n-1}
        fib_curr, fib_next = fibonacci_prev(fib_curr, fib_next)

        if f_l > f_r:
            # Преобразуем промежуток неопределённости: [x_l, rhs]
            lhs = x_l
            x_l = x_r
            f_l = f_r
            x_r = lhs + (fib_curr / fib_next) * (rhs - lhs)
            f_r = fun(x_r)
        else:
            # Преобразуем промежуток неопределённости: [lhs, x_r]
            rhs = x_r
            x_r = x_l
            f_r = f_l
            x_l = lhs + ((fib_next - fib_curr) / fib_next) * (rhs - lhs)
            f_l = fun(x_l)
        res.function_probes += 1
        res.iterations += 1

    res.result = (lhs + rhs) * 0.5
    res.accuracy = rhs - lhs