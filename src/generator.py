import random
import networkx as nx


def generate_initial_graph(conjecture):
    """
    Génère un graphe initial selon la classe de la conjecture.
    """

    subgroup = str(conjecture.subgroup).lower()

    if "tree" in subgroup:
        return generate_tree_graph()

    if "bipartite" in subgroup:
        return generate_bipartite_graph()

    if "planar" in subgroup:
        return generate_planar_graph()

    # Par défaut : graphe connexe général
    return generate_random_graph()


def generate_random_graph():
    choice = random.choice([
        "erdos",
        "complete",
        "cycle_plus_chords",
        "clique_chain"
    ])

    if choice == "erdos":
        return generate_erdos_graph()

    if choice == "complete":
        return generate_complete_graph()

    if choice == "cycle_plus_chords":
        return generate_cycle_plus_chords()

    if choice == "clique_chain":
        return generate_clique_chain()


def generate_erdos_graph():
    n = random.randint(5, 30)
    p = random.uniform(0.2, 0.8)

    G = nx.erdos_renyi_graph(n, p)
    return make_connected(G)


def generate_complete_graph():
    n = random.randint(4, 12)
    return nx.complete_graph(n)


def generate_cycle_plus_chords():
    n = random.randint(6, 30)
    G = nx.cycle_graph(n)

    extra_edges = random.randint(1, 2 * n)

    for _ in range(extra_edges):
        u, v = random.sample(list(G.nodes()), 2)

        if not G.has_edge(u, v):
            G.add_edge(u, v)

    return G


def generate_clique_chain():
    number_of_cliques = random.randint(2, 6)
    clique_size = random.randint(3, 7)

    G = nx.Graph()
    previous_connector = None
    current_node = 0

    for _ in range(number_of_cliques):
        nodes = list(range(current_node, current_node + clique_size))
        current_node += clique_size

        for i in nodes:
            for j in nodes:
                if i < j:
                    G.add_edge(i, j)

        if previous_connector is not None:
            G.add_edge(previous_connector, nodes[0])

        previous_connector = nodes[-1]

    return G


def generate_tree_graph():
    n = random.randint(5, 40)

    # Génère un arbre aléatoire
    G = nx.random_labeled_tree(n)

    return G


def generate_bipartite_graph():
    n1 = random.randint(3, 15)
    n2 = random.randint(3, 15)

    p = random.uniform(0.2, 0.8)

    G = nx.bipartite.random_graph(n1, n2, p)

    return make_connected(G)


def generate_planar_graph():
    n = random.randint(5, 30)

    # Un cycle est planaire
    G = nx.cycle_graph(n)

    # On ajoute quelques arêtes seulement si le graphe reste planaire
    attempts = random.randint(n, 3 * n)

    for _ in range(attempts):
        u, v = random.sample(list(G.nodes()), 2)

        if G.has_edge(u, v):
            continue

        G.add_edge(u, v)

        is_planar, _ = nx.check_planarity(G)

        if not is_planar:
            G.remove_edge(u, v)

    return G


def make_connected(G):
    if G.number_of_nodes() == 0:
        return G

    if nx.is_connected(G):
        return G

    components = list(nx.connected_components(G))

    for i in range(len(components) - 1):
        u = random.choice(list(components[i]))
        v = random.choice(list(components[i + 1]))

        G.add_edge(u, v)

    return G