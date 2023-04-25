import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np


def optimize_staffing(type, nbr_week, drq, nbr_work):
    # Type of optimization
    optimisation_type = type
    # The days have to be consecutive
    number_week_days = nbr_week
    # The minimal number of employees per day
    daily_requirement = np.array(drq)
    # Number of consecutive work days per employee
    work_days = nbr_work
    # Number of rest days per employee
    rest_days = 0

    # =========== Model creation =============
    m = gp.Model("staffing")

    # ============ Decision variables ==============
    X = []
    for i in range(number_week_days):
        if optimisation_type == "CONTINUOUS":
            X.append(m.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x' + str(i)))
        elif optimisation_type == "INTEGER":
            X.append(m.addVar(lb=0, vtype=GRB.INTEGER, name='x' + str(i)))
        else:
            return None

    # ============= Fonction objective ============
    m.setObjective(quicksum(X[i] for i in range(number_week_days)), GRB.MINIMIZE)

    # ============ Constraints ==============

    # Build (sparse) constraint matrix
    constraints = np.zeros(shape=(number_week_days, number_week_days))
    for col in range(7):
        row = col
        for i in range(work_days):
            constraints[row][col] = 1
            row += 1
            if row == 7:
                row = 0

    # Add constraints
    m.addConstrs((quicksum(constraints[j][i] * X[i] for i in range(number_week_days)) >= daily_requirement[j] for j in
                  range(len(daily_requirement))), "limitation")

    # =========== Optimize model =============
    m.optimize()

    for var in m.getVars():
        print(var.varName, '=', var.X)
    print("obj val = ", m.objVal)


# Example :
optimize_staffing("INTEGER", 7, [17, 13, 15, 19, 14, 16, 11], 5)
