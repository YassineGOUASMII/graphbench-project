import random
import time
import networkx as nx

from generator import generate_initial_graph
from mutations import mutate
from invariants import compute_invariants
from scoring import heuristic_score


def search_counterexample(conjecture, time_limit=30):
    start = time.time()

    population_size = 20
    population = []

    for _ in range(population_size):
        G = generate_initial_graph(conjecture)

        if not is_valid_for_conjecture(G, conjecture):
            continue

        invariants = compute_invariants(G)

        heuristic = heuristic_score(G, invariants, conjecture)
        real_violation = conjecture.violation(invariants)

        population.append((heuristic, real_violation, G, invariants))

    if not population:
        G = generate_initial_graph(conjecture)
        invariants = compute_invariants(G)

        heuristic = heuristic_score(G, invariants, conjecture)
        real_violation = conjecture.violation(invariants)

        population.append((heuristic, real_violation, G, invariants))

    population.sort(key=lambda x: x[0], reverse=True)

    best_heuristic, best_real_violation, best_graph, best_invariants = population[0]

    print("Score initial :", best_real_violation)

    while time.time() - start < time_limit:
        _, _, parent_graph, _ = random.choice(population[:5])

        child = mutate(parent_graph)

        if not is_valid_for_conjecture(child, conjecture):
            continue

        invariants = compute_invariants(child)

        heuristic = heuristic_score(child, invariants, conjecture)
        real_violation = conjecture.violation(invariants)

        population.append((heuristic, real_violation, child, invariants))
        population.sort(key=lambda x: x[0], reverse=True)
        population = population[:population_size]

        if real_violation > best_real_violation:
            best_heuristic = heuristic
            best_real_violation = real_violation
            best_graph = child
            best_invariants = invariants

            print("Nouveau meilleur score :", best_real_violation)

        if real_violation > 0:
            return {
                "found": True,
                "graph": child,
                "invariants": invariants,
                "score": real_violation,
                "heuristic_score": heuristic,
                "time": time.time() - start,
            }

    return {
        "found": False,
        "graph": best_graph,
        "invariants": best_invariants,
        "score": best_real_violation,
        "heuristic_score": best_heuristic,
        "time": time.time() - start,
    }


def is_valid_for_conjecture(G, conjecture):
    subgroup = str(conjecture.subgroup).lower()

    if G.number_of_nodes() == 0:
        return False

    if "connected" in subgroup:
        if not nx.is_connected(G):
            return False

    if "tree" in subgroup:
        if not nx.is_tree(G):
            return False

    if "bipartite" in subgroup:
        if not nx.is_bipartite(G):
            return False

    if "planar" in subgroup:
        is_planar, _ = nx.check_planarity(G)
        if not is_planar:
            return False

    if "claw" in subgroup:
        if not is_claw_free(G):
            return False

    return True


def is_claw_free(G):
    """
    Vérifie si le graphe est sans griffe.
    Une griffe = K1,3 induit.
    """

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