from gurobipy import *
import numpy as np

def chaussetous_solver(input_array):
    demand, initial_stock, initial_workers, worker_salary, max_overtime, overtime_pay, hours_per_shoe, material_cost, recruitment_cost, layoff_cost, storage_cost = input_array

    num_months = len(demand)

    # Create the model
    model = Model("ChausseTous")

    # Decision variables
    shoes_produced = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="shoes_produced")
    workers = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="workers")
    overtime = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="overtime")
    recruitment = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="recruitment")
    layoff = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="layoff")
    stock = model.addVars(num_months, lb=0, vtype=GRB.INTEGER, name="stock")

    # Constraints
    model.addConstr(stock[0] == initial_stock)
    model.addConstr(workers[0] == initial_workers)

    for month in range(num_months):
        # Production constraint
        model.addConstr(shoes_produced[month] == hours_per_shoe * (160 * workers[month] + overtime[month]))
        
        # Overtime constraint
        model.addConstr(overtime[month] <= max_overtime * workers[month])
        
        # Stock and demand constraints
        if month > 0:
            model.addConstr(stock[month] == stock[month - 1] + shoes_produced[month] - demand[month])
            model.addConstr(workers[month] == workers[month - 1] + recruitment[month] - layoff[month])

    # Objective function
    objective = quicksum(worker_salary * workers[month] + overtime_pay * overtime[month] + material_cost * shoes_produced[month] + recruitment_cost * recruitment[month] + layoff_cost * layoff[month] + storage_cost * stock[month] for month in range(num_months))
    model.setObjective(objective, GRB.MINIMIZE)

    # Solve the model
    model.optimize()

    # Extract results
    production_plan = [v.x for v in shoes_produced.values()]
    worker_management = [w.x for w in workers.values()]
    total_cost = model.objVal

    return np.array([production_plan, worker_management, total_cost], dtype=object)

# Example usage:
input_array = (
    [3000, 5000, 2000, 1000],
    500,
    100,
    1500,
    20,
    13,
    4,
    15,
    1600,
    2000,
    3
)

result = chaussetous_solver(input_array)
print("Optimal production plan:", result[0])
print("Optimal worker management:", result[1])
print("Total cost:", result[2])
