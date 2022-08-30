import pandas as pd
import pulp as plp
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import webbrowser
from threading import Timer

dataset = pd.read_csv('CTech.csv')

# Variables
population = [27954, 34043, 15081, 43242, 14143]
current_staff = [21.0, 52.0, 43.0, 9.0, 64.0]
ratio = 2808
Max_Set = 189

g = 0
for i in population:
    g += int(i / ratio)
y = Max_Set / g
maxr = []
minr = []
for i in population:
    minr.append(int(i / (ratio)))
    maxr.append(int(i / (ratio / y)))

location_df = pd.DataFrame({'zip': ['A', 'B', 'C', 'D', 'E'],
                            'max_resource': maxr,
                            'min_resource': minr
                            })

staff_df = pd.DataFrame({'staff': ['current_staff'],
                         'fixed': [Max_Set],
                         })

resource_cost = np.array(population)
model = plp.LpProblem("Resource_allocation_prob", plp.LpMaximize)

no_of_location = location_df.shape[0]
no_of_work = staff_df.shape[0]
x_vars_list = []
for l in range(1, no_of_location + 1):
    for w in range(1, no_of_work + 1):
        temp = str(l) + str(w)
        x_vars_list.append(temp)
x_vars = plp.LpVariable.matrix("R", x_vars_list, cat="Integer", lowBound=0)
final_allocation = np.array(x_vars).reshape(5, 1)
res_equation = plp.lpSum(final_allocation * resource_cost)
model += res_equation

for l1 in range(no_of_location):
    model += plp.lpSum(final_allocation[l1][w1] for w1 in range(no_of_work)) <= location_df['max_resource'].tolist()[l1]
    model += plp.lpSum(final_allocation[l1][w1] for w1 in range(no_of_work)) >= location_df['min_resource'].tolist()[l1]

for w1 in range(no_of_work):
    model += plp.lpSum(final_allocation[l1][w1] for l1 in range(no_of_location)) == staff_df['fixed'].tolist()[w1]

model.solve()

r = []
for x in model.variables():
    r.append(x.value())

new = []
for i in range(5):
    new.append(int(population[i] / r[i]))

app = Dash("Resource Optimization")
sites = ['Site A', 'Site B', 'Site C', "Site D", "Site E"]

fig = go.Figure(data=[
    go.Bar(name='Current Staff Members', x=sites, y=current_staff),
    go.Bar(name='Optimized Staff Members', x=sites, y=r)
])
fig.update_layout(barmode='group')


def get_chart():
    barChart = dcc.Graph(figure=go.Figure().add_trace(go.Bar(x=sites, y=new)))
    return barChart


app.layout = html.Div(
    children=[
        html.H1(children="Optimization Model Results", ),
        html.P(
            children="This model reallocates health professionals"
                     "in Washington State so that each hospital has "
                     "a fair amount of health staff members based"
                     "on a designated population-staff ratio.",
        ),
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        html.P(
            children="The graph above compares the amount of current staff members"
                     " at each site (in blue) to the optimized number of staff members"
                     " at each site (in orange), thus showing how many staff members"
                     " should be moved at each site."
        ),
        get_chart(),
        html.P(
            children="The graph above shows the new population to health care "
                     "staff member ratio at each site after each site was optimized, "
                     "and compares each new ratio to show how similar they are."
        ),
    ]
)

port = 5000
def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=port)
