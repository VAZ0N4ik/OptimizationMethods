import math
from OneDimensionalMethods.bisection import bisect
from OneDimensionalMethods.common import MethodType, create_search_result


def test_quadratic():
    """Тест на квадратичной функции f(x) = (x-2)^2"""
    def f(x: float) -> float:
        return (x - 2) ** 2


    res = create_search_result(method_type=MethodType.BISECT)

    bisect(res, f, 0, 5, 1e-6, 1000)

    print("Test quadratic function f(x) = (x-2)^2:")
    print(res)
    assert abs(res.result - 2.0) < 1e-5, f"Expected result near 2.0, got {res.result}"
    print("✓ Passed\n")


def test_sine():
    """Тест на функции синуса f(x) = sin(x) на промежутке [2, 4]"""
    def f(x: float) -> float:
        return math.sin(x)

    res = create_search_result(method_type=MethodType.BISECT)

    bisect(res, f, 2, 4, 1e-8, 1000)

    print("Test sine function f(x) = sin(x) on [2, 4]:")
    print(res)
    # На промежутке [2, 4] функция sin(x) убывает, поэтому минимум будет в точке x = 4
    assert abs(res.result - 4.0) < 1e-3, f"Expected result near 4.0, got {res.result}"
    print("✓ Passed\n")


def test_exponential():
    """Тест на экспоненциальной функции f(x) = e^x - 2x"""
    def f(x: float) -> float:
        return math.exp(x) - 2 * x

    res = create_search_result(method_type=MethodType.BISECT)

    bisect(res, f, 0, 2, 1e-6, 1000)

    print("Test exponential function f(x) = e^x - 2x:")
    print(res)
    # Минимум находится при x = ln(2) ≈ 0.693
    assert abs(res.result - math.log(2)) < 1e-5, f"Expected result near ln(2) ≈ 0.693, got {res.result}"
    print("✓ Passed\n")


def test_reversed_bounds():
    """Тест с перевернутыми границами"""
    def f(x: float) -> float:
        return x ** 2

    res = create_search_result(method_type=MethodType.BISECT)

    bisect(res, f, 2, -2, 1e-6, 1000)

    print("Test with reversed bounds (rhs < lhs):")
    print(res)
    assert abs(res.result) < 1e-5, f"Expected result near 0.0, got {res.result}"
    print("✓ Passed\n")


def test_accuracy():
    """Тест точности алгоритма"""
    def f(x: float) -> float:
        return (x - 1.5) ** 2

    for eps in [1e-3, 1e-6, 1e-9]:
        res = create_search_result(method_type=MethodType.BISECT)

        bisect(res, f, 0, 3, eps, 1000)

        print(f"Test accuracy with eps = {eps}:")
        print(f"Result: {res.result}, Iterations: {res.iterations}")
        assert abs(res.result - 1.5) < eps * 10, f"Result {res.result} is not within tolerance {eps * 10}"
        print("✓ Passed\n")


if __name__ == "__main__":
    print("Running bisection method tests...\n")
    test_quadratic()
    test_sine()
    test_exponential()
    test_reversed_bounds()
    test_accuracy()
    print("All tests passed!")