import gurobipy as gp
from gurobipy import GRB

def calcul_Revenu_National(Rendement, Prix_Vente, nbre_Ovriers, Heures_Machine, Eau, Salaire_ouvrier, gestion, prix_eau, prix_machine):
    return (Rendement * Prix_Vente - Eau * prix_eau - Heures_Machine * prix_machine - gestion)

def Maximiser_Revenu_National(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
    m = gp.Model("Maximisation du revenu national")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)) - gp.quicksum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")

    # Résolution
    m.optimize()

    # Récupération des résultats
    revenu_total = m.objVal + sum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures))
    qtes_cultures = [x[i].x for i in range(nbre_cultures)]

    return revenu_total, qtes_cultures



#Comment sera modifié l’exploitation optimale de cette zone agricole si l’état cherche de plus à satisfaire une demande minimale de 37500 quintaux de blé.
def Maximiser_Revenu_National_demande_minimale(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine, demande_minimale):
    m = gp.Model("Maximisation du revenu national")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)) - gp.quicksum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")
    m.addConstr(gp.quicksum(L_Rendement[i] * x[i] for i in range(nbre_cultures)) >= demande_minimale, "Contrainte demande minimale")

    # Résolution
    m.optimize()

    # Récupération des résultats
    revenu_total = m.objVal + sum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures))
    qtes_cultures = [x[i].x for i in range(nbre_cultures)]

    return revenu_total, qtes_cultures





#L’état peut il développer un programme d’exploitation qui lui permette d’embaucher toute la main d’œuvre agricole
def Maximiser_Revenu_National_main_oeuvre (superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
    m = gp.Model("Maximisation du revenu national")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)) - gp.quicksum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) == main_oeuvre, "Contrainte emploi total main d'oeuvre")

    # Résolution
    m.optimize()

    # Récupération des résultats
    revenu_total = m.objVal + sum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures))
    qtes_cultures = [x[i].x for i in range(nbre_cultures)]

    return revenu_total, qtes_cultures


revenu_total, qtes_cultures = Maximiser_Revenu_National(1000, 3000, 25000000, 24000, 3, (75,60,55), (60,50,66),(2,1,2), (30,24,20), (3000,2000,2500), (500,500,600), (250,180,190), 0.1, 30)

print(revenu_total)
print(qtes_cultures)