def heuristic_score(G, invariants, conjecture):
    violation = conjecture.violation(invariants)

    x = invariants.get(conjecture.x_name, 0)
    y = invariants.get(conjecture.y_name, 0)

    n = invariants.get("order", 0)
    m = invariants.get("size", 0)

    density = invariants.get("density", 0)
    max_degree = invariants.get("maximum_degree", 0)
    avg_degree = invariants.get("average_degree", 0)

    triangles = invariants.get("triangle_number", 0)
    clique = invariants.get("clique_number", 0)

    domination = invariants.get("domination_number", 0)
    total_domination = invariants.get("total_domination_number", 0)
    independence = invariants.get("independence_number", 0)
    matching = invariants.get("matching_number", 0)
    vertex_cover = invariants.get("vertex_cover_number", 0)

    score = 100000.0 * violation

    if conjecture.sign == "<=":
        score += 2.0 * y
        score -= 0.5 * x
    elif conjecture.sign == ">=":
        score -= 2.0 * y
        score += 0.5 * x

    score += 0.08 * triangles
    score += 0.4 * clique
    score += 0.08 * max_degree
    score += 0.05 * avg_degree

    score += 0.08 * domination
    score += 0.08 * total_domination
    score += 0.06 * independence
    score += 0.06 * matching
    score += 0.06 * vertex_cover

    score -= 0.01 * n
    score -= 0.05 * abs(density - 0.5)

    return score