import gurobipy as gp
from gurobipy import GRB

def calcul_Bénéfice (Rendement,Prix_Vente,nbre_Ovriers,Heures_Machine,Eau,Salaire_ouvrier,gestion, prix_eau, prix_machine):
    return (Rendement*Prix_Vente-nbre_Ovriers*Salaire_ouvrier-Eau*prix_eau-Heures_Machine*prix_machine-gestion)
    
def Maximiser_Profit(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
    m = gp.Model("Maximisation du profit")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Bénéfice(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")

    # Résolution
    m.optimize()

    # Récupération des résultats
    benefice_total = m.objVal
    qtes_cultures = [(L_nbre_Ovriers[i], x[i].x, L_Rendement[i], L_Prix_Vente[i]) for i in range(nbre_cultures)]
    recommandation = "You should plant"
    for nb_ouvriers, qte, rendement, prix in qtes_cultures:
        culture = L_Rendement.index(rendement)
        recommandation += f" {qte} hectares of the crop {culture+1}\n"
    recommandation = recommandation[:-1] + "."
    
    
    return benefice_total, recommandation


def Q2(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
        m = gp.Model("Maximisation du profit")

        # Variables de décision
        x = {}
        for i in range(nbre_cultures):
            x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

        # Fonction objectif
        m.setObjective(gp.quicksum(calcul_Bénéfice(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

        # Contraintes
        m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie+1, "Contrainte superficie")
        m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre+1, "Contrainte main d'oeuvre")
        m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation+1, "Contrainte eau d'irrigation")
        m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine+1, "Contrainte heures machine")

        # Résolution
        m.optimize()
        
        salaire_annuel_payé = sum(x[i].x * L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures))

        return salaire_annuel_payé