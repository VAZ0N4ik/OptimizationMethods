import math
from typing import Callable
from OneDimensionalMethods import *

def target_function(x: float) -> float:
    """Целевая функция для оптимизации f(x) = (x - 2)^2 + sin(5x)"""
    return (x - 2) ** 2


def main():
    """Главная функция - запуск всех трех методов на одной функции"""

    # Параметры задачи
    lhs = -2.0
    rhs = 6.0
    eps = 1e-6
    max_iters = 1000

    print("\n" + "=" * 80)
    print("МЕТОДЫ ОДНОМЕРНОГО ПОИСКА")
    print("=" * 80)
    print(f"Целевая функция: f(x) = (x - 2)² + sin(5x)")
    print(f"Промежуток: [{lhs}, {rhs}]")
    print(f"Точность: {eps}")
    print(f"Макс. итераций: {max_iters}")
    print("=" * 80)

    # Метод дихотомии (половинного деления)
    print("\n1. МЕТОД ДИХОТОМИИ")
    print("-" * 40)
    res_bisect = create_search_result(MethodType.BISECT)
    bisect(res_bisect, target_function, lhs, rhs, eps, max_iters)
    print(res_bisect)

    # Метод золотого сечения
    print("\n2. МЕТОД ЗОЛОТОГО СЕЧЕНИЯ")
    print("-" * 40)
    res_golden = create_search_result(MethodType.GOLDEN_RATIO)
    golden_ratio(res_golden, target_function, lhs, rhs, eps, max_iters)
    print(res_golden)

    # Метод Фибоначчи
    print("\n3. МЕТОД ФИБОНАЧЧИ")
    print("-" * 40)
    res_fibonacci = create_search_result(MethodType.FIBONACCI)
    fibonacci(res_fibonacci, target_function, lhs, rhs, eps*2.5)
    print(res_fibonacci)

    # Сравнительная таблица
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ МЕТОДОВ")
    print("=" * 80)
    print(f"{'Метод':<20} {'Результат':<15} {'Итерации':<12} {'Вызовы f(x)':<12}")
    print("-" * 80)
    print(f"{'Дихотомия':<20} {res_bisect.result:<15.10f} {res_bisect.iterations:<12} {res_bisect.function_probes:<12}")
    print(f"{'Золотое сечение':<20} {res_golden.result:<15.10f} {res_golden.iterations:<12} {res_golden.function_probes:<12}")
    print(f"{'Фибоначчи':<20} {res_fibonacci.result:<15.10f} {res_fibonacci.iterations:<12} {res_fibonacci.function_probes:<12}")
    print("=" * 80)

    # Эффективность
    print("\nЭффективность относительно дихотомии:")
    print(f"Золотое сечение: {(1 - res_golden.function_probes/res_bisect.function_probes)*100:.1f}% экономии вызовов функции")
    print(f"Фибоначчи:       {(1 - res_fibonacci.function_probes/res_bisect.function_probes)*100:.1f}% экономии вызовов функции")
    print()


if __name__ == "__main__":
    main()