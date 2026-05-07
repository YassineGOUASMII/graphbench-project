import networkx as nx

from invariants import compute_invariants
from generator import generate_random_graph
from mutations import mutate


G = generate_random_graph()
H = mutate(G)

print("=== Test rapide du moteur ===")
print("Graphe initial :", G.number_of_nodes(), "sommets,", G.number_of_edges(), "arêtes")
print("Graphe muté :", H.number_of_nodes(), "sommets,", H.number_of_edges(), "arêtes")
print("Connexe :", nx.is_connected(H))

print()
print("Quelques invariants :")
invariants = compute_invariants(H)

print("order =", invariants["order"])
print("size =", invariants["size"])
print("maximum_degree =", invariants["maximum_degree"])
print("triangle_number =", invariants["triangle_number"])
print("clique_number =", invariants["clique_number"])