import math
from OneDimensionalMethods.fibonacci import fibonacci, get_fibonacci_numbers
from OneDimensionalMethods.common import MethodType, create_search_result


def test_fibonacci_generation():
    """Тест генерации чисел Фибоначчи"""
    n, L_n_minus_1, L_n = get_fibonacci_numbers(100, 0.01)
    print(f"Test Fibonacci generation for ratio 100:")
    print(f"n = {n}, L_{n-1} = {L_n_minus_1}, L_n = {L_n}")
    assert L_n >= 100, f"L_n should be >= 100, got {L_n}"
    assert L_n_minus_1 < L_n, f"L_{n-1} should be < L_n"
    print("✓ Passed\n")


def test_quadratic():
    """Тест на квадратичной функции f(x) = (x-2)^2"""
    def f(x: float) -> float:
        return (x - 2) ** 2

    res = create_search_result(method_type=MethodType.FIBONACCI)
    fibonacci(res, f, 0, 5, 1e-6, 1000)

    print("Test quadratic function f(x) = (x-2)^2:")
    print(res)
    assert abs(res.result - 2.0) < 1e-5, f"Expected result near 2.0, got {res.result}"
    print("✓ Passed\n")


def test_sine():
    """Тест на функции синуса f(x) = sin(x) на промежутке [2, 4]"""
    def f(x: float) -> float:
        return math.sin(x)

    res = create_search_result(method_type=MethodType.FIBONACCI)
    fibonacci(res, f, 2, 4, 1e-8, 1000)

    print("Test sine function f(x) = sin(x) on [2, 4]:")
    print(res)
    # На промежутке [2, 4] функция sin(x) убывает, поэтому минимум будет в точке x = 4
    assert abs(res.result - 4.0) < 1e-3, f"Expected result near 4.0, got {res.result}"
    print("✓ Passed\n")


def test_exponential():
    """Тест на экспоненциальной функции f(x) = e^x - 2x"""
    def f(x: float) -> float:
        return math.exp(x) - 2 * x

    res = create_search_result(method_type=MethodType.FIBONACCI)
    fibonacci(res, f, 0, 2, 1e-6, 1000)

    print("Test exponential function f(x) = e^x - 2x:")
    print(res)
    # Минимум находится при x = ln(2) ≈ 0.693
    assert abs(res.result - math.log(2)) < 1e-5, f"Expected result near ln(2) ≈ 0.693, got {res.result}"
    print("✓ Passed\n")


def test_reversed_bounds():
    """Тест с перевернутыми границами"""
    def f(x: float) -> float:
        return x ** 2

    res = create_search_result(method_type=MethodType.FIBONACCI)
    fibonacci(res, f, 2, -2, 1e-6, 1000)

    print("Test with reversed bounds (rhs < lhs):")
    print(res)
    assert abs(res.result) < 1e-5, f"Expected result near 0.0, got {res.result}"
    print("✓ Passed\n")


def test_efficiency_comparison():
    """Сравнение эффективности трех методов"""
    from OneDimensionalMethods.bisection import bisect
    from OneDimensionalMethods.golden_ratio import golden_ratio

    def f(x: float) -> float:
        return (x - 3.14159) ** 2 + math.sin(5 * x)

    # Тестируем метод Фибоначчи
    res_fib = create_search_result(method_type=MethodType.FIBONACCI)
    fibonacci(res_fib, f, 0, 6, 1e-6, 1000)

    # Тестируем метод золотого сечения
    res_golden = create_search_result(method_type=MethodType.GOLDEN_RATIO)
    golden_ratio(res_golden, f, 0, 6, 1e-6, 1000)

    # Тестируем метод дихотомии
    res_bisect = create_search_result(method_type=MethodType.BISECT)
    bisect(res_bisect, f, 0, 6, 1e-6, 1000)

    print("Efficiency comparison on f(x) = (x - π)² + sin(5x):")
    print(f"Fibonacci: {res_fib.iterations} iterations, {res_fib.function_probes} function calls")
    print(f"Golden ratio: {res_golden.iterations} iterations, {res_golden.function_probes} function calls")
    print(f"Bisection: {res_bisect.iterations} iterations, {res_bisect.function_probes} function calls")
    print(f"Fibonacci result: {res_fib.result:.6f}")
    print(f"Golden ratio result: {res_golden.result:.6f}")
    print(f"Bisection result: {res_bisect.result:.6f}")

    # Фибоначчи должен быть самым эффективным или сравнимым с золотым сечением
    assert res_fib.function_probes <= res_golden.function_probes + 1, \
        "Fibonacci should be comparable to golden ratio in efficiency"
    assert res_fib.function_probes < res_bisect.function_probes, \
        "Fibonacci should be more efficient than bisection"
    print("✓ Fibonacci is efficient\n")


if __name__ == "__main__":
    print("Running Fibonacci method tests...\n")
    test_fibonacci_generation()
    test_quadratic()
    test_sine()
    test_exponential()
    test_reversed_bounds()
    test_efficiency_comparison()
    print("All tests passed!")