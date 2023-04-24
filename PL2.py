import gurobipy as gp

# Création du modèle
model = gp.Model()

# Données du problème
n = int(input("Entrez le nombre de types de pétrole : "))
types = range(n)

# Demander à l'utilisateur d'entrer les quantités, niveaux de qualité, les prix et les frais de marketing pour chaque type
quantities = []
qualities = []
prices = []
marketing_costs = []
for i in types:
    quantity = float(input(f"Entrez la quantité disponible pour le type {i+1} : "))
    quality = float(input(f"Entrez le niveau de qualité pour le type {i+1} : "))
    price = float(input(f"Entrez le prix par baril pour le type {i+1} : "))
    marketing_cost = float(input(f"Entrez les frais de marketing pour le type {i+1} : "))
    quantities.append(quantity)
    qualities.append(quality)
    prices.append(price)
    marketing_costs.append(marketing_cost)

# Demander à l'utilisateur d'entrer la qualité minimale requise
Qmin = float(input("Entrez la qualité minimale requise : "))

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

# Affichage des résultats
if model.status == gp.GRB.OPTIMAL:
    print("Solution optimale trouvée")
    for i in types:
        print(f"Type {i+1} : {x[i].x:.2f} barils, qualité {q[i].x:.2f}, prix {p[i].x:.2f} dt/baril, coût de marketing {marketing_costs[i]:.2f} dt/baril")
    print(f"Revenu total : {model.objVal:.2f} dt")
else:
    print("Aucune solution trouvée")

