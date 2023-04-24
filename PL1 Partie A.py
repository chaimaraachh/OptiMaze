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
    qtes_cultures = [x[i].x for i in range(nbre_cultures)]

    return benefice_total, qtes_cultures



def facteurs():
    return("Les facteurs de production qui réalisent le plein emploi sont la superficie de terrain, le nombre d'ouvriers, le nombre d'heures de machine et la quantité d'eau d'irrigation")

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
        
        salaire_annuel_payé = [x[i].x * L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures)]

        return salaire_annuel_payé

revenu_total, qtes_cultures = Maximiser_Profit(1000, 3000, 25000000, 24000, 3, (75,60,55), (60,50,66),(2,1,2), (30,24,20), (3000,2000,2500), (500,500,600), (250,180,190), 0.1, 30)

print(revenu_total)
print(qtes_cultures)