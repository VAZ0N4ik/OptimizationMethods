from typing import Callable, Tuple
from .common import SearchResult

def get_fibonacci_numbers(length_ratio: float, eps: float) -> Tuple[int, int, int]:
    """
    Вычисляет пару чисел Фибоначчи для заданной длины отрезка и точности.

    Args:
        length_ratio: Отношение длины отрезка к точности |rhs - lhs| / eps
        eps: Точность поиска

    Returns:
        Tuple[n, L_n_minus_1, L_n]: номер и пара чисел Фибоначчи
    """
    # Генерация чисел Фибоначчи
    fib_prev = 1
    fib_curr = 1
    n = 2

    while fib_curr < length_ratio:
        fib_next = fib_prev + fib_curr
        fib_prev = fib_curr
        fib_curr = fib_next
        n += 1

    return n, fib_prev, fib_curr

def fibonacci(
    res: SearchResult,
    fun: Callable[[float], float],
    lhs: float,
    rhs: float,
    eps: float,
    max_iters: int
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

    res.accuracy = eps

    # Определяем пару чисел Фибоначчи
    length = rhs - lhs
    n, L_n_minus_1, L_n = get_fibonacci_numbers(length / eps, eps)

    # Ограничиваем количество итераций
    n = min(n, max_iters + 2)

    # Определяем левую и правую точки разбиения отрезка
    x_r = lhs + (L_n_minus_1 / L_n) * (rhs - lhs)
    x_l = lhs + ((L_n - L_n_minus_1) / L_n) * (rhs - lhs)

    # Измерения целевой функции в точках x_l и x_r
    f_l = fun(x_l)
    f_r = fun(x_r)
    res.function_probes += 2

    # Основной цикл поиска
    for _ in range(n - 2):
        if abs(rhs - lhs) < 2 * eps:
            break

        # Сдвиг пары чисел Фибоначчи: L_{n-1}, L_n → L_{n-2}, L_{n-1}
        L_n_minus_2 = L_n - L_n_minus_1
        L_n = L_n_minus_1
        L_n_minus_1 = L_n_minus_2

        if f_l > f_r:
            # Преобразуем промежуток неопределённости: [x_l, rhs]
            lhs = x_l
            x_l = x_r
            f_l = f_r
            x_r = lhs + (L_n_minus_1 / L_n) * (rhs - lhs)
            f_r = fun(x_r)
            res.function_probes += 1
        else:
            # Преобразуем промежуток неопределённости: [lhs, x_r]
            rhs = x_r
            x_r = x_l
            f_r = f_l
            x_l = lhs + ((L_n - L_n_minus_1) / L_n) * (rhs - lhs)
            f_l = fun(x_l)
            res.function_probes += 1

        res.iterations += 1

    res.result = (lhs + rhs) / 2