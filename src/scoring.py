def heuristic_score(G, invariants, conjecture):
    violation = conjecture.violation(invariants)

    x = invariants.get(conjecture.x_name, 0)
    y = invariants.get(conjecture.y_name, 0)

    n = invariants.get("order", 0)
    m = invariants.get("size", 0)
    triangles = invariants.get("triangle_number", 0)
    clique = invariants.get("clique_number", 0)
    max_degree = invariants.get("maximum_degree", 0)
    avg_degree = invariants.get("average_degree", 0)
    domination = invariants.get("domination_number", 0)
    total_domination = invariants.get("total_domination_number", 0)
    independence = invariants.get("independence_number", 0)
    matching = invariants.get("matching_number", 0)
    vertex_cover = invariants.get("vertex_cover_number", 0)

    density = 0
    if n > 1:
        density = 2 * m / (n * (n - 1))

    score = 1000.0 * violation

    if conjecture.sign == "<=":
        score += 0.2 * y
        score -= 0.05 * x
    elif conjecture.sign == ">=":
        score -= 0.2 * y
        score += 0.05 * x

    score += 0.03 * triangles
    score += 0.15 * clique
    score += 0.04 * max_degree
    score += 0.03 * avg_degree

    score += 0.05 * domination
    score += 0.05 * total_domination
    score += 0.04 * independence
    score += 0.04 * matching
    score += 0.04 * vertex_cover

    score -= 0.002 * n
    score -= 0.02 * abs(density - 0.5)

    return score