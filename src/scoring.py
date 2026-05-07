def heuristic_score(G, invariants, conjecture):
    """
    Conservative adaptive scoring.

    The real violation remains the most important signal.
    X and Y are only used as small tie-breakers.
    """

    violation = conjecture.violation(invariants)

    x = invariants.get(conjecture.x_name, 0)
    y = invariants.get(conjecture.y_name, 0)

    n = invariants.get("order", 0)
    m = invariants.get("size", 0)

    density = 0
    if n > 1:
        density = 2 * m / (n * (n - 1))

    score = 10000.0 * violation

    # For Y <= f(X), we want Y high
    if conjecture.sign == "<=":
        score += 0.1 * y

    # For Y >= f(X), we want Y low
    elif conjecture.sign == ">=":
        score -= 0.1 * y

    # Encourage exploration of useful X values, but very slightly
    score += 0.01 * x

    # Avoid graphs that are too large
    score -= 0.001 * n

    # Avoid extreme density
    score -= 0.01 * abs(density - 0.5)

    return score