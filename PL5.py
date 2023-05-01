import gurobipy as gp
from gurobipy import GRB

def Politique(offres = [35, 50, 40], demandes = [45, 20, 30, 30], couts = [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]]):
    
    res=""
    m = gp.Model("electricity_assignment")

    # Define decision variables
    x = {}
    for i in range(len(offres)):
        for j in range(len(demandes)):
            x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=offres[i], name=f'x_{i}_{j}')

    # Define objective function
    obj = gp.quicksum(couts[i][j] * x[i, j] for i in range(len(offres)) for j in range(len(demandes)))
    m.setObjective(obj, GRB.MINIMIZE)

    # Define constraints
    for j in range(len(demandes)):
        m.addConstr(gp.quicksum(x[i, j] for i in range(len(offres))) == demandes[j])

    # Solve the problem
    m.optimize()

    # Print the solution
    if m.status == GRB.OPTIMAL:
       print(f"Total transport cost: {m.objVal}")
       for i in range(len(offres)):
           for j in range(len(demandes)):
               if x[i, j].x > 0:
                res = res + f"Amount transported from power plant {i+1} to city {j+1}: {x[i,j].x} \n"
    else:
        return "No optimal solution found."
    return res

def Politique_avec_penaltie(penalty=[20, 25, 22, 35], offres = [35, 50, 40], demandes = [45, 20, 30, 30], couts = [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]]):
    nb_sources = len(offres)
    nb_destinations = len(demandes)
    m = gp.Model('electricity_assignment_with_penalty')
    
    # Create variables
    x = m.addVars(nb_sources, nb_destinations, vtype=GRB.CONTINUOUS, lb=0, name='x')
    z = m.addVars(nb_destinations, vtype=GRB.BINARY, name='z')
    
    # Set objective function
    m.setObjective(gp.quicksum(x[i,j]*couts[i][j] for i in range(nb_sources) for j in range(nb_destinations)), GRB.MINIMIZE)
    
    # Add supply constraints
    for i in range(nb_sources):
        m.addConstr(gp.quicksum(x[i,j] for j in range(nb_destinations)) <= offres[i], f'supply_{i}')
        
    # Add demand constraints
    for j in range(nb_destinations):
        m.addConstr(gp.quicksum(x[i,j] for i in range(nb_sources)) >= demandes[j], f'demand_{j}')
        
    # Add penalty for unsatisfied demand
    for j in range(nb_destinations):
        m.addConstr(gp.quicksum(x[i,j] for i in range(nb_sources)) - demandes[j] <= 10000 * (1 - z[j]), f'penalty_{j}')
    
    # Optimize the model
    m.optimize()
    
    # Retrieve the solution
    if m.status == GRB.OPTIMAL:
        result = "Optimal solution found:\n"
        for i in range(nb_sources):
            for j in range(nb_destinations):
               result += f'x_{i}_{j} = {x[i,j].x:.2f} (city {i+1} supplies {x[i,j].x:.2f} units of electricity to demand {j+1})\n'
        result += f"Total cost = {m.objVal:.2f}"
        return result
    else:
        return "No solution found."