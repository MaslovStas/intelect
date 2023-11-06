from math import cos, exp, pi


def test_bill(x: float, y: float) -> float:
    """Функция Била
        f(x, y) = (1.5 - x + x * y)^2 + (2.25 - x + x * y^2)^2 + (2.625 − x + x * y^3)^2
        f(3, 0.5) = 0
        -4.5 <= x, y <= 4.5"""
    return (1.5 - x + x * y) ** 2 + (2.25 - x + x * y * y) ** 2 + (2.625 - x + x * y * y * y) ** 2


def test_booth(x: float, y: float) -> float:
    """Функция Бута
        f(x, y) = (x + 2y - 7)^2 + (2x + y - 5)^2
        f(1, 3) = 0
        -10 <= x, y <= 10"""
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def test_himm(x: float, y: float) -> float:
    """Функция Бута
        f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2
        min = 0
        -5 <= x, y <= 5"""
    return (x * x + y - 11) ** 2 + (x + y * y - 7) ** 2


def test_izum(x: float, y: float) -> float:
    """Функция Изюма
        f(x, y) = -cos(x) * cos(y) * exp(-((x - pi)^2 + (y - pi)^2))}
        f(pi, pi) = 0
        -100 <= x, y <= 100"""
    return -cos(x) * cos(y) * exp(-((x - pi) ** 2 + (y - pi) ** 2))


def get_odds_for_linear_function(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    a: float = (y2 - y1) / (x2 - x1)
    b: float = y1 - a * x1
    return a, b
