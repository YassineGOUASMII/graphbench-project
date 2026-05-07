import random
import networkx as nx


def mutate_add_edge(G):
    H = G.copy()
    nodes = list(H.nodes())

    if len(nodes) < 2:
        return H

    for _ in range(20):
        u, v = random.sample(nodes, 2)

        if not H.has_edge(u, v):
            H.add_edge(u, v)
            return H

    return H


def mutate_remove_edge(G):
    H = G.copy()
    edges = list(H.edges())

    if not edges:
        return H

    edge = random.choice(edges)
    H.remove_edge(*edge)

    if H.number_of_nodes() > 0 and not nx.is_connected(H):
        H.add_edge(*edge)

    return H


def mutate_add_vertex(G):
    H = G.copy()

    new_node = max(H.nodes()) + 1 if len(H.nodes()) > 0 else 0
    H.add_node(new_node)

    if G.number_of_nodes() > 0:
        old_node = random.choice(list(G.nodes()))
        H.add_edge(new_node, old_node)

    return H


def mutate_remove_vertex(G):
    H = G.copy()

    if H.number_of_nodes() <= 3:
        return H

    node = random.choice(list(H.nodes()))
    H.remove_node(node)

    if H.number_of_nodes() > 0 and not nx.is_connected(H):
        return G.copy()

    return H


def mutate_add_leaf(G):
    H = G.copy()

    if H.number_of_nodes() == 0:
        H.add_node(0)
        return H

    new_node = max(H.nodes()) + 1
    parent = random.choice(list(H.nodes()))

    H.add_node(new_node)
    H.add_edge(new_node, parent)

    return H


def mutate_subdivide_edge(G):
    H = G.copy()
    edges = list(H.edges())

    if not edges:
        return H

    u, v = random.choice(edges)
    H.remove_edge(u, v)

    new_node = max(H.nodes()) + 1
    H.add_node(new_node)

    H.add_edge(u, new_node)
    H.add_edge(new_node, v)

    return H


def mutate_add_path(G):
    H = G.copy()

    if H.number_of_nodes() == 0:
        return H

    start = random.choice(list(H.nodes()))
    length = random.randint(2, 5)

    previous = start

    for _ in range(length):
        new_node = max(H.nodes()) + 1
        H.add_node(new_node)
        H.add_edge(previous, new_node)
        previous = new_node

    return H


def mutate_add_clique(G):
    H = G.copy()

    if H.number_of_nodes() == 0:
        return H

    size = random.randint(3, 6)
    connector = random.choice(list(H.nodes()))

    new_nodes = []

    for _ in range(size):
        new_node = max(H.nodes()) + 1
        H.add_node(new_node)
        new_nodes.append(new_node)

    for i in range(len(new_nodes)):
        for j in range(i + 1, len(new_nodes)):
            H.add_edge(new_nodes[i], new_nodes[j])

    H.add_edge(connector, new_nodes[0])

    return H


def mutate_add_false_twin(G):
    """
    Ajoute un faux jumeau :
    nouveau sommet avec les mêmes voisins qu'un sommet existant,
    mais non relié au sommet original.
    """
    H = G.copy()

    if H.number_of_nodes() == 0:
        return H

    original = random.choice(list(H.nodes()))
    new_node = max(H.nodes()) + 1

    H.add_node(new_node)

    for neighbor in list(H.neighbors(original)):
        H.add_edge(new_node, neighbor)

    return H


def mutate_local_densification(G):
    """
    Ajoute plusieurs arêtes autour d'une zone locale.
    Utile pour augmenter triangles et cliques.
    """
    H = G.copy()

    if H.number_of_nodes() < 3:
        return H

    center = random.choice(list(H.nodes()))
    candidates = list(H.neighbors(center)) + [center]

    if len(candidates) < 3:
        return mutate_add_edge(H)

    attempts = random.randint(2, 6)

    for _ in range(attempts):
        u, v = random.sample(candidates, 2)

        if u != v and not H.has_edge(u, v):
            H.add_edge(u, v)

    return H


def mutate(G):
    mutations = [
        mutate_add_edge,
        mutate_remove_edge,
        mutate_add_vertex,
        mutate_remove_vertex,
        mutate_add_leaf,
        mutate_subdivide_edge,
        mutate_add_path,
        mutate_add_clique,
        mutate_add_false_twin,
        mutate_local_densification,
    ]

    mutation = random.choice(mutations)
    return mutation(G)