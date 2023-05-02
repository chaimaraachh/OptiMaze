import gurobipy as gp
def pertrolium_solver(input_array):
    quantities,qualities,prices,marketing_costs,Qmin,n=input_array
    types = range(n)
    # Création du modèle
    model = gp.Model()
    # Variables de décision
    x = model.addVars(types, lb=0, vtype=gp.GRB.CONTINUOUS, name="x")
    q = model.addVars(types, lb=0, ub=100, vtype=gp.GRB.CONTINUOUS, name="q")
    p = model.addVars(types, lb=0, vtype=gp.GRB.CONTINUOUS, name="p")
    # Objectif : maximiser le revenu total (revenus - coûts de marketing)
    model.setObjective(gp.quicksum(x[i] * p[i] for i in types) - gp.quicksum(x[i] * marketing_costs[i] for i in types), gp.GRB.MAXIMIZE)
    # Contraintes
    model.addConstr(gp.quicksum(x[i] for i in types) <= sum(quantities), "quantity_constraint")
    model.addConstr(gp.quicksum(x[i] * q[i] for i in types) >= Qmin, "quality_constraint")

    # Mise à jour des contraintes pour prendre en compte les valeurs de qualité et de prix
    for i in types:
        model.addConstr(x[i] <= quantities[i], f"quantity_value_{i}")
        model.addConstr(q[i] == qualities[i], f"quality_value_{i}")
        model.addConstr(p[i] == prices[i], f"price_value_{i}")

    # Résolution du modèle
    model.optimize()
    results=[]
    # Affichage des résultats
    if model.status == gp.GRB.OPTIMAL:
        
        for i in types:
            results.append(f"Type {i+1} : {x[i].x:.2f} barrels, quality {q[i].x:.2f}, prix {p[i].x:.2f} dt/barrel, marketing costs {marketing_costs[i]:.2f} dt/barrel \n")
        results.append(f"Total revenue : {model.objVal:.2f} dt")
        result_str = "\n".join(results)
        
        return result_str
    else:
        return 0
    

