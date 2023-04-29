import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from gurobipy import *

# Demander à l'utilisateur la taille du tableau
n = int(input("Entrez le nombre de villes: "))

# Créer un tableau vide de taille n x n
distances = np.zeros((n, n))

# Demander à l'utilisateur les distances et directions des déplacements entre les villes
for i in range(n):
    for j in range(i+1, n):
        d = input("Distance entre la ville {} et la ville {}: ".format(i+1, j+1))
        if d == "":
            distances[i][j] = 1e6
            distances[j][i] = 1e6
        else:
            distances[i][j] = float(d)
            distances[j][i] = float(d)

if np.isnan(distances).any() or np.isinf(distances).any():
    print("Valeur de distance invalide trouvée dans le tableau distances.")
print(distances)
# Demander à l'utilisateur la ville de départ et la ville d'arrivée
start_city = int(input("Entrez la ville de départ: ")) - 1
end_city = int(input("Entrez la ville d'arrivée: ")) - 1

# Créer le modèle Gurobi
model = Model()

# Créer les variables de décision
x = {}
for i in range(n):
    for j in range(n):
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x_%d_%d" % (i,j))

# Contrainte 1: chaque ville est visitée exactement une fois
for i in range(n):
    model.addConstr(quicksum(x[i,j] for j in range(n) if i!=j) == 1)

# Contrainte 2: pas de sous-tours
for i in range(n):
    for j in range(n):
        if i!=j:
            model.addConstr(x[i,j] + x[j,i] <= 1)

# Contrainte 3: la ville de départ est la première ville visitée
model.addConstr(quicksum(x[start_city,j] for j in range(n) if start_city!=j) == 1)

# Contrainte 4: la ville d'arrivée est la dernière ville visitée
model.addConstr(quicksum(x[i,end_city] for i in range(n) if end_city!=i) == 1)

# Objectif: minimiser la distance totale
model.setObjective(quicksum(x[i,j]*distances[i][j] for i in range(n) for j in range(n)), GRB.MINIMIZE)


# Résoudre le modèle
model.optimize()

# Récupération de la solution
x_sol = model.getAttr('x', x)

# Affichage du plus court chemin
print("Le plus court chemin de la ville {} à la ville {} est:".format(start_city+1, end_city+1))
node = start_city
while node != end_city:
    print(" -> ", node+1, end='')
    for j in range(n):
        if node != j and x_sol[node, j] == 1:
            node = j
            break
print(" -> ", end_city+1)
# Créer un graphe
G = nx.DiGraph()
# Ajouter les nœuds au graphe
for i in range(1, n+1):
    G.add_node(i)

# Ajouter les arcs au graphe
for i in range(1, n+1):
    for j in range(1, n+1):
        if i != j and distances[i-1][j-1] != float('inf'):
            # Ajouter l'arc au graphe avec le poids correspondant
            G.add_edge(i, j, weight=distances[i-1][j-1])

# Calculer le chemin le plus court entre le nœud de départ et le nœud d'arrivée
try:
    shortest_path = nx.shortest_path(G, source=start_city+1, target=end_city+1, weight='weight')
except nx.NetworkXNoPath:
    print("Il n'y a pas de chemin entre le nœud de départ et le nœud d'arrivée.")
    sys.exit(1)

# Créer un dictionnaire pour stocker les couleurs des nœuds et des arcs
node_colors = ['lightblue' if node not in shortest_path else 'green' for node in G.nodes()]
edge_colors = ['black' if (u, v) not in zip(shortest_path, shortest_path[1:]) else 'green' for u, v in G.edges()]

# Dessiner le graphe avec les couleurs du meilleur chemin
pos = nx.spring_layout(G)
nx.draw(G,pos, with_labels=True, node_size=800, node_color=node_colors, font_size=14, font_weight='bold', edge_color=edge_colors)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=14, font_weight='bold')
plt.show()

