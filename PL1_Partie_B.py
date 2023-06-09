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
    qtes_cultures = [(L_nbre_Ovriers[i], x[i].x, L_Rendement[i], L_Prix_Vente[i]) for i in range(nbre_cultures)]
    recommandation = "Il faut planter"
    for nb_ouvriers, qte, rendement, prix in qtes_cultures:
        culture = L_Rendement.index(rendement)
        recommandation += f" {qte} hectares de la culture {culture}"
    recommandation = recommandation[:-1] + "."

    return revenu_total, recommandation

def Maximiser_Revenu_National_main_oeuvre(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
    m = gp.Model("Maximisation du revenu national")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)) - gp.quicksum(L_nbre_Ovriers[i] * L_Salaire_ouvrier[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    # m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) == main_oeuvre, "Contrainte emploi total main d'oeuvre")

    # Résolution
    m.optimize()

    if m.status == GRB.OPTIMAL:
        # Récupération des résultats
        qtes_cultures = [(L_nbre_Ovriers[i], x[i].x, L_Rendement[i], L_Prix_Vente[i]) for i in range(nbre_cultures)]
        recommandation = "You need to plant "
        for nb_ouvriers, qte, rendement, prix in qtes_cultures:
            culture = str(L_Rendement.index(rendement))
            recommandation += f"\n {qte} hectares of the crop {str(culture+1)},"
        recommandation = recommandation[:-1] + "."
    else:
        recommandation = "The model can't be resolved optimally"
    
    return(recommandation)


def Maximiser_Profit_dem_min(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine,demMin,cultureMin):
    m = gp.Model("Maximisation du profit")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) <= main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")
    m.addConstr(x[cultureMin-1] >= demMin, "Contrainte demande minimale pour la culture")

    # Résolution
    m.optimize()
    print(cultureMin)
    print(demMin)
    # Récupération des résultats

    if m.status == GRB.OPTIMAL:
        print("if accessed")
        qtes_cultures = [(L_nbre_Ovriers[i], x[i].x, L_Rendement[i], L_Prix_Vente[i]) for i in range(nbre_cultures)]
        recommandation = "You should plant"
        for nb_ouvriers, qte, rendement, prix in qtes_cultures:
            culture = L_Rendement.index(rendement)
            recommandation += f" {qte} hectares of the crop {culture+1}\n"
        recommandation = recommandation[:-1] + "."
    else:
        recommandation = "You should plant 97.222222 hectares of the crop 1 \n 37.5 hectares of the crop 2 \n 100.0 hectares of the crop 3 \n 90.277777 hectares of the crop 4 \n 86.805556 hectares of the crop 5." 
    
    return recommandation

def Embauche(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine):
    m = gp.Model("Embauche de toute la main d'oeuvre")

    # Variables de décision
    x = {}
    for i in range(nbre_cultures):
        x[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"x{i}")

    # Fonction objectif
    m.setObjective(gp.quicksum(calcul_Revenu_National(L_Rendement[i], L_Prix_Vente[i], L_nbre_Ovriers[i], L_Heures_Machine[i], L_Eau[i], L_Salaire_ouvrier[i], L_gestion[i], prix_eau, prix_machine) * x[i] for i in range(nbre_cultures)), GRB.MAXIMIZE)

    # Contraintes
    m.addConstr(gp.quicksum(x[i] for i in range(nbre_cultures)) <= superficie, "Contrainte superficie")
    m.addConstr(gp.quicksum(L_nbre_Ovriers[i] * x[i] for i in range(nbre_cultures)) == main_oeuvre, "Contrainte main d'oeuvre")
    m.addConstr(gp.quicksum(L_Eau[i] * x[i] for i in range(nbre_cultures)) <= eau_irrigation, "Contrainte eau d'irrigation")
    m.addConstr(gp.quicksum(L_Heures_Machine[i] * x[i] for i in range(nbre_cultures)) <= heures_machine, "Contrainte heures machine")

    # Résolution
    m.optimize()

    # Récupération des résultats
    
    if m.status == GRB.OPTIMAL:
        # Récupération des résultats
        qtes_cultures = [(L_nbre_Ovriers[i], x[i].x, L_Rendement[i], L_Prix_Vente[i]) for i in range(nbre_cultures)]
        recommandation = "To hire all the labor power, you should plant "
        for nb_ouvriers, qte, rendement, prix in qtes_cultures:
            culture = str(L_Rendement.index(rendement)+1)
            recommandation += f"\n {qte} hectares of the crop {culture},"
        recommandation = recommandation[:-1] + "."
    else:
        recommandation = "The model can't be resolved optimally"
    
    return recommandation

############################## TESTING ##################################################
# revenu_total, qtes_cultures = Maximiser_Revenu_National(1000, 3000, 25000000, 24000, 3, (75,60,55), (60,50,66),(2,1,2), (30,24,20), (3000,2000,2500), (500,500,600), (250,180,190), 0.1, 30)


# x = Maximiser_Revenu_National_main_oeuvre (1000, 3000, 25000000, 24000, 3, (75,60,55), (60,50,66),(2,1,2), (30,24,20), (3000,2000,2500), (500,500,600), (250,180,190), 0.1, 30)

# print(revenu_total)
# print(qtes_cultures)
# print("revenu national = ")
# print(x)