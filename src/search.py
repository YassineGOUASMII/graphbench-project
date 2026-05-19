import random
import time
import networkx as nx

from generator import generate_initial_graph
from mutations import mutate
from invariants import compute_invariants
from scoring import heuristic_score


def search_counterexample(conjecture, time_limit=60):
    start = time.time()

    population_size = 40
    population = []
    cache = {}

    required = [
        conjecture.x_name,
        conjecture.y_name,
        "order",
        "size",
        "density",
        "maximum_degree",
        "average_degree",
        "triangle_number",
        "clique_number",
        "domination_number",
        "total_domination_number",
        "independence_number",
        "matching_number",
        "vertex_cover_number",
    ]

    def get_invariants(G):
        graph6 = nx.to_graph6_bytes(G, header=False).decode().strip()

        if graph6 not in cache:
            cache[graph6] = compute_invariants(G, required)

        return cache[graph6]

    for _ in range(population_size):
        G = generate_initial_graph(conjecture)

        if not is_valid_for_conjecture(G, conjecture):
            continue

        invariants = get_invariants(G)
        real_score = conjecture.violation(invariants)
        heuristic = heuristic_score(G, invariants, conjecture)

        population.append((real_score, heuristic, G, invariants))

    if not population:
        G = generate_initial_graph(conjecture)
        invariants = get_invariants(G)
        real_score = conjecture.violation(invariants)
        heuristic = heuristic_score(G, invariants, conjecture)
        population.append((real_score, heuristic, G, invariants))

    population.sort(key=lambda x: x[0], reverse=True)

    best_score, best_heuristic, best_graph, best_invariants = population[0]

    print("Score initial :", best_score)

    while time.time() - start < time_limit:
        by_real = sorted(population, key=lambda x: x[0], reverse=True)[:8]
        by_heuristic = sorted(population, key=lambda x: x[1], reverse=True)[:8]

        candidate_pool = by_real + by_heuristic

        _, _, parent_graph, _ = random.choice(candidate_pool)

        child = parent_graph.copy()

# Nombre de mutations adaptatif
        if random.random() < 0.7:
          mutations_count = random.randint(1, 3)
        else:
          mutations_count = random.randint(4, 8)

        for _ in range(mutations_count):
          child = mutate(child)

        if not is_valid_for_conjecture(child, conjecture):
            continue

        invariants = get_invariants(child)
        real_score = conjecture.violation(invariants)
        heuristic = heuristic_score(child, invariants, conjecture)

        population.append((real_score, heuristic, child, invariants))

        top_real = sorted(population, key=lambda x: x[0], reverse=True)[:15]
        top_heuristic = sorted(population, key=lambda x: x[1], reverse=True)[:15]

        merged = top_real + top_heuristic

        unique = {}
        for item in merged:
            _, _, G, _ = item
            key = nx.to_graph6_bytes(G, header=False).decode().strip()
            unique[key] = item

        population = list(unique.values())[:population_size]

        if real_score > best_score:
            best_score = real_score
            best_heuristic = heuristic
            best_graph = child
            best_invariants = invariants

        if real_score > 0:
            return {
                "found": True,
                "graph": child,
                "invariants": invariants,
                "score": real_score,
                "heuristic_score": heuristic,
                "time": time.time() - start,
            }

    return {
        "found": False,
        "graph": best_graph,
        "invariants": best_invariants,
        "score": best_score,
        "heuristic_score": best_heuristic,
        "time": time.time() - start,
    }


def is_valid_for_conjecture(G, conjecture):
    subgroup = str(conjecture.subgroup).lower()

    if G.number_of_nodes() == 0:
        return False

    if "connected" in subgroup and not nx.is_connected(G):
        return False

    if "tree" in subgroup and not nx.is_tree(G):
        return False

    if "bipartite" in subgroup and not nx.is_bipartite(G):
        return False

    if "planar" in subgroup:
        is_planar, _ = nx.check_planarity(G)
        if not is_planar:
            return False

    if "claw" in subgroup and not is_claw_free(G):
        return False

    return True


def is_claw_free(G):
    for center in G.nodes():
        neighbors = list(G.neighbors(center))

        if len(neighbors) < 3:
            continue

        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                for k in range(j + 1, len(neighbors)):
                    a = neighbors[i]
                    b = neighbors[j]
                    c = neighbors[k]

                    if (
                        not G.has_edge(a, b)
                        and not G.has_edge(a, c)
                        and not G.has_edge(b, c)
                    ):
                        return False

    return True