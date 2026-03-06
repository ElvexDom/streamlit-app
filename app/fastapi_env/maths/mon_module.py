def add(a: float, b: float) -> float:
    """Additionner deux nombres."""
    return a + b


def sub(a: float, b: float) -> float:
    """Soustraire deux nombres."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiplier deux nombres."""
    return a * b


def divide(a: float, b: float) -> float:
    """Diviser deux nombres avec gestion de l'erreur par zéro."""
    if b == 0:
        raise ValueError("Division par zéro impossible")
    return a / b
