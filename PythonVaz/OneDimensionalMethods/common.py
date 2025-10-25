from pydantic import BaseModel
from enum import Enum


class MethodType(Enum):
    BISECT = "bisect"
    GOLDEN_RATIO = "golden_ratio"
    FIBONACCI = "fibonacci"
    NOPE = "NoMethod"


class SearchResult(BaseModel):
    method_type: MethodType
    iterations: int
    function_probes: int
    accuracy: float
    result: float

    def clear(self) -> None:
        ...

    def __str__(self) -> str:
        return (f"Method: {self.method_type.value}\n"
                f"Iterations: {self.iterations}\n"
                f"Function probes: {self.function_probes}\n"
                f"Accuracy: {self.accuracy:.2e}\n"
                f"Result: {self.result:.10f}")


def create_search_result(method_type, accuracy=0.0) -> SearchResult:
    """Создает пустую структуру SearchResult"""
    return SearchResult(
        method_type=method_type,
        iterations=0,
        function_probes=0,
        accuracy=accuracy,
        result=0.0
    )