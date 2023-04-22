from gurobipy import Model, GRB


def optimize_transportation(offres, couts_production_transport, couts_transport_clients, quantite_requise, couts_fixes):
    usines = range(len(offres))
    depots = range(len(couts_transport_clients))
    clients = range(len(quantite_requise))

    # Create model
    m = Model()

    # Variables
    x = {(i, j): m.addVar(vtype=GRB.INTEGER, name=f"x_{i}_{j}") for i in usines for j in depots}
    y = {(j, k): m.addVar(vtype=GRB.INTEGER, name=f"y_{j}_{k}") for j in depots for k in clients}
    z = [m.addVar(vtype=GRB.BINARY, name=f"z_{i}") for i in range(len(couts_fixes))]

    # Objective
    m.setObjective(sum(couts_production_transport[i][j] * x[i, j] for i in usines for j in depots)
                   + sum(couts_transport_clients[j][k] * y[j, k] for j in depots for k in clients)
                   + sum(couts_fixes[i] * z[i] for i in range(len(couts_fixes))), GRB.MINIMIZE)

    # Constraints
    for i in usines:
        m.addConstr(sum(x[i, j] for j in depots) <= offres[i] * z[i])

    for k in clients:
        m.addConstr(sum(y[j, k] for j in depots) == quantite_requise[k])

    for j in depots:
        m.addConstr(sum(x[i, j] for i in usines) == sum(y[j, k] for k in clients))

    # Optimize
    m.optimize()

    result_text = ""

    # Extract results
    if m.status == GRB.OPTIMAL:
        result_text += f"Optimal solution found with total cost: {m.objVal}\n"
        result_text += "Usine to Depot transport:\n"
        for i, j in x:
            if x[i, j].x > 0:
                result_text += f"Usine {i + 1} to Depot {j + 1}: {x[i, j].x} tonnes\n"
        result_text += "Depot to Client transport:\n"
        for j, k in y:
            if y[j, k].x > 0:
                result_text += f"Depot {j + 1} to Client {k + 1}: {y[j, k].x} tonnes\n"
        result_text += "Facilities used:\n"
        for i in range(len(couts_fixes)):
            if z[i].x > 0:
                result_text += f"Use facility {i + 1}\n"
    else:
        result_text += "No optimal solution found\n"

    return result_text




# Data
offres = [300, 200, 300, 200, 400]
couts_production_transport = [
    [800, 1000, 1200],
    [700, 500, 700],
    [800, 600, 500],
    [500, 600, 700],
    [700, 600, 500]
]

couts_transport_clients = [
    [40, 80, 90, 50],
    [70, 40, 60, 80],
    [80, 30, 50, 60]
]

quantite_requise = [200, 300, 150, 250]
couts_fixes = [35000, 45000, 40000, 42000, 40000, 40000, 20000, 60000]

# Example test
result_text = optimize_transportation(offres, couts_production_transport, couts_transport_clients, quantite_requise, couts_fixes)
print(result_text)
