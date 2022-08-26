import pandas as pd
import pulp as plp
import numpy as np

dataset=pd.read_csv('CTech.csv')

#Your variables
population = [27954, 34043, 15081, 43242, 14143]
ratio = 2808
Max_Set = 189

g = 0
for i in population:
    g += int(i/ratio)
y = Max_Set/g
print(y)
maxr = []
minr = []
for i in population:
    minr.append(int(i/(ratio)))
    maxr.append(int(i/(ratio/y)))
print(minr)
print(maxr)

location_df = pd.DataFrame({'zip': ['A', 'B', 'C', 'D', 'E'],
                             'max_resource': maxr,
                            'min_resource': minr
                             })

staff_df = pd.DataFrame({'staff': ['current_staff'],
                             'fixed':[Max_Set],
                             })

resource_cost = np.array(population)
model = plp.LpProblem("Resource_allocation_prob", plp.LpMaximize)

no_of_location = location_df.shape[0]
no_of_work = staff_df.shape[0]
x_vars_list = []
for l in range(1,no_of_location+1):
    for w in range(1,no_of_work+1):
        temp = str(l)+str(w)
        x_vars_list.append(temp)
x_vars = plp.LpVariable.matrix("R", x_vars_list, cat = "Integer", lowBound = 0)
final_allocation = np.array(x_vars).reshape(len(population),1)
print(final_allocation)
res_equation = plp.lpSum(final_allocation*resource_cost)
model += res_equation

for l1 in range(no_of_location):
    model += plp.lpSum(final_allocation[l1][w1] for w1 in range(no_of_work)) <= location_df['max_resource'].tolist()[l1]
    model += plp.lpSum(final_allocation[l1][w1] for w1 in range(no_of_work)) >= location_df['min_resource'].tolist()[l1]

for w1 in range(no_of_work):
    model += plp.lpSum(final_allocation[l1][w1] for l1 in range(no_of_location)) == staff_df['fixed'].tolist()[w1]

print(model)
model.solve()
status = plp.LpStatus[model.status]
print(status)
print("Optimal overall resouce cost: ",str(plp.value(model.objective)))
for each in model.variables():
    print("Optimal cost of ", each, ": "+str(each.value()))

r = []
for x in model.variables():
    r.append(x.value())

print(r)

for i in range(5):
    r[i] = int(population[i]/r[i])

print('New population to healthcare staff ratios:')
print(r)
