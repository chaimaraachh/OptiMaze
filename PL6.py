import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np


def optimize_distribution(cost_lt, fact_prd, client_d, nbr_wh, cap_trsp):
    # cost list
    cost_list = np.array(cost_lt)

    # production capacity
    fact_prod_cap = np.array(fact_prd)

    # demande des clients
    client_demands = np.array(client_d)

    # max capacity of transport between nodes
    cap_trans_nd = cap_trsp

    # number of factories
    number_factories = len(fact_prod_cap)
    # number of clients
    number_clients = len(client_demands)
    # number of warehouses
    number_warehouse = nbr_wh

    # total number of nodes
    tot_nodes = number_factories + number_clients + number_warehouse

    # =========== Model creation =============
    m = gp.Model("distribution")

    # ============ Decision variables ==============
    X = []
    Clients = [[] for i in range(number_clients)]
    Factories = [[] for i in range(number_factories)]
    Warehouse = [[] for i in range(number_warehouse)]

    for i in range(number_factories):
        for j in range(tot_nodes - 1):
            X.append(m.addVar(vtype=GRB.CONTINUOUS, name='factory' + str(i) + str(j)))
            Factories[i].append(X[-1])

    for i in range(number_warehouse):
        for j in range((number_warehouse - 1) + number_clients):
            X.append(m.addVar(vtype=GRB.CONTINUOUS, name='warehouse' + str(i) + str(j)))
            Warehouse[i].append(X[-1])

    for i in range(number_clients):
        for j in range(number_clients - 1):
            X.append(m.addVar(vtype=GRB.CONTINUOUS, name='client' + str(i) + str(j)))
            Clients[i].append(X[-1])

    # ============= Fonction objective ============
    m.setObjective(quicksum(cost_list[i] * X[i] for i in range(len(X))), GRB.MINIMIZE)

    # ============ Constraints ==============

    # Max production capacity of factories
    for i in range(number_factories):
        m.addConstr((quicksum(z for z in Factories[i])) <= fact_prod_cap[i],
                    name='constr factory ' + str(i))

        # Max client demands
    for i in range(number_clients):
        sum_fact = quicksum(Factories[j][number_factories - 1 + number_warehouse + i] for j in range(len(Factories)))
        sum_wh = quicksum(Warehouse[j][number_warehouse - 1 + i] for j in range(len(Warehouse)))
        sum_clt = 0
        for k in range(number_clients):
            if k == i:
                continue
            elif k < i:
                sum_clt += Clients[k][i - 1]
            else:
                sum_clt += Clients[k][i]
        sum_entrant = sum_fact + sum_wh + sum_clt
        sum_sortant = quicksum(t for t in Clients[i])
        m.addConstr((sum_entrant - sum_sortant) == client_demands[i], 'constr client ' + str(i))

    # Max capacity transport
    for i in range(len(X)):
        m.addConstr(X[i] <= cap_trans_nd, 'constr transport limit')

        # Equilibre sortant - entrant warehouse

    for i in range(number_warehouse):
        sum_fact = quicksum(Factories[j][number_factories - 1 + i] for j in range(len(Factories)))
        sum_wh = 0
        for k in range(number_warehouse):
            if k == i:
                continue
            elif k < i:
                sum_wh += Warehouse[k][i - 1]
            else:
                sum_wh += Warehouse[k][i]
        sum_entrant = sum_fact + sum_wh
        sum_sortant = quicksum(t for t in Warehouse[i])
        m.addConstr(sum_sortant - sum_entrant <= 0, 'constr warehouse ' + str(i))

    # =========== Optimize model =============
    m.optimize()

    # Check status of optimization model
    status = m.status
    print('*************************')
    print(m.status)
    if status == GRB.OPTIMAL:
        print('Optimal objective value found.')
    elif status == GRB.INFEASIBLE:
        print('Model is infeasible.')
    elif status == GRB.TIME_LIMIT:
        print('Reached time limit.')
    else:
        print('Optimization ended with status %d' % status)

    for var in m.getVars():
        print(var.varName, '=', var.X)
    print("obj val = ", m.objVal)

    # Example


cost_lt = [5, 3, 5, 5, 20, 20,
           9, 9, 1, 1, 8, 15,
           0.4, 8, 1, 0.5, 10, 12,
           1.2, 2, 12,
           0.8, 2, 12,
           1,
           7]
fact_prd = [200, 300, 100]
client_d = [400, 180]
nbr_wh = 2
cap_trsp = 200
optimize_distribution(cost_lt, fact_prd, client_d, nbr_wh, cap_trsp)
