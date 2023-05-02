import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *

def shortest_path(inputs):
    distances, start_city, end_city, n = inputs
    start_city -= 1
    end_city -= 1
    model = Model()

    # Decision variables
    X = {}
    for i in range(n):
        for j in range(n):
            if distances[i][j] != 0:
                X[i,j] = model.addVar(vtype=GRB.BINARY, name=f'X_{i}_{j}')
    
    # Objective function
    model.setObjective(quicksum(distances[i][j] * X[i,j] for i in range(n) for j in range(n) if distances[i][j] != 0), GRB.MINIMIZE)

    # Constraints
    # Start node
    model.addConstr(quicksum(X[start_city,j] for j in range(n) if distances[start_city][j] != 0) == 1, name='start_node')
    # End node
    model.addConstr(quicksum(X[i,end_city] for i in range(n) if distances[i][end_city] != 0) == 1, name='end_node')
    # Intermediate nodes
    for i in range(n):
        if i != start_city and i != end_city:
            model.addConstr(quicksum(X[i,j] for j in range(n) if distances[i][j] != 0) == quicksum(X[j,i] for j in range(n) if distances[j][i] != 0), name=f'intermediate_node_{i}')

    model.optimize()

    # Solution
    path = []
    curr_node = start_city
    while curr_node != end_city:
        for j in range(n):
            if distances[curr_node][j] != 0 and X[curr_node,j].x > 0.5:
                path.append(curr_node+1)
                curr_node = j
                break
    path.append(end_city+1)
    return str(path)




"""
def shortest_path(inputs ):
    distances,start_city,end_city,n=inputs
    print(distances)
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
    model.addConstr(quicksum(x[start_city-1,j] for j in range(n) if start_city!=j) == 1)

    # Contrainte 4: la ville d'arrivée est la dernière ville visitée
    model.addConstr(quicksum(x[i,end_city-1] for i in range(n) if end_city!=i) == 1)

    # Objectif: minimiser la distance totale
    model.setObjective(quicksum(x[i,j]*distances[i][j] for i in range(n) for j in range(n)), GRB.MINIMIZE)

    # Résoudre le modèle
    model.optimize()

    # Récupération de la solution
    x_sol = model.getAttr('x', x)
   
    path_str = str(f"the shortest path available from {start_city} to {end_city} : {start_city}")
    
    node = start_city - 1
    while node != end_city - 1:
        path_str += str(f"-> {node+1}")
        
        for j in range(n):
            if node != j and x_sol[node, j] == 1:
                node = j
                break
        
        if node == end_city - 1:
            break
    
    path_str += str(f" -> {end_city}")
        
    if path_str == "":
        return("no path available")
    else:
        result= path_str
            
        return result
"""





"""
def plot_shortest_path(inputs):
    distances, start_city, end_city, n = inputs

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph
    for i in range(1, n+1):
        G.add_node(i)

    # Add edges to the graph
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j and distances[i-1][j-1] != 0:
                # Add the edge to the graph with the weight corresponding to the distance
                G.add_edge(i, j, weight=distances[i-1][j-1])

    # Calculate the shortest path between the start and end nodes
    try:
        shortest_path = nx.shortest_path(G, source=start_city, target=end_city, weight='weight')
    except nx.NetworkXNoPath:
        print("There is no path between the start and end nodes.")
        sys.exit(1)

    # Create dictionaries to store the colors of the nodes and edges
    node_colors = ['lightblue' if node not in shortest_path else 'green' for node in G.nodes()]
    edge_colors = ['black' if (u, v) not in zip(shortest_path, shortest_path[1:]) else 'green' for u, v, d in G.edges(data=True) if d['weight'] != 0]

    # Draw the graph with the colors of the shortest path
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=14, font_weight='bold', edge_color=edge_colors)
    labels = nx.get_edge_attributes(G, 'weight')
    filtered_labels = {k: v for k, v in labels.items() if v != 0}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=filtered_labels, font_size=14, font_weight='bold')

    return plt
"""

def plot_shortest_path(inputs):
    distances, start_city, end_city, n = inputs

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph
    for i in range(1, n+1):
        G.add_node(i)

    # Add edges to the graph
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j and distances[i-1][j-1] != 0:
                # Add the edge to the graph with the weight corresponding to the distance
                G.add_edge(i, j, weight=distances[i-1][j-1])

    # Calculate the shortest path between the start and end nodes
    try:
        shortest_path = nx.shortest_path(G, source=start_city, target=end_city, weight='weight')
    except nx.NetworkXNoPath:
        print("There is no path between the start and end nodes.")
        sys.exit(1)

    # Create dictionaries to store the colors of the nodes and edges
    node_colors = ['lightblue' if node not in shortest_path else 'green' for node in G.nodes()]
    edge_colors = ['black' if (u, v) not in zip(shortest_path, shortest_path[1:]) else 'green' for u, v, d in G.edges(data=True) if d['weight'] != 0]

    # Draw the graph with the colors of the shortest path
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=14, font_weight='bold', edge_color=edge_colors)
    labels = nx.get_edge_attributes(G, 'weight')
    filtered_labels = {k: v for k, v in labels.items() if v != 0}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=filtered_labels, font_size=14, font_weight='bold')

    return plt


inputs=([[0, 70, 63, 56, 0, 0, 0, 0, 0, 0], [0, 0, 25, 19, 73, 50, 79, 0, 0, 0], [0, 25, 0, 29, 69, 61, 0, 0, 0, 0], [0, 19, 29, 0, 67, 45, 0, 0, 85, 0], [0, 0, 0, 0, 0, 18, 67, 69, 54, 87], [0, 0, 0, 0, 18, 0, 72, 52, 51, 97], [0, 0, 0, 0, 0, 0, 0, 17, 31, 72], [0, 0, 0, 0, 0, 0, 17, 0, 15, 0], [0, 0, 0, 0, 0, 0, 31, 15, 0, 69], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 1, 10, 10)
#fig=plot_shortest_path(inputs)
#fig.show();
print (shortest_path(inputs))
