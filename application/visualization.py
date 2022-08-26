from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash("Resource Optimization")
sites=['Site A', 'Site B', 'Site C', "Site D", "Site E"]

fig = go.Figure(data=[
    go.Bar(name='Current Staff Members', x=sites, y=[21.0, 52.0, 43.0, 9.0, 64.0]),
    go.Bar(name='Optimized Staff Members', x=sites, y=[35.0, 49.0, 22.0, 63.0, 20.0])
])
fig.update_layout(barmode='group')


def get_chart():
    barChart = dcc.Graph(figure=go.Figure().add_trace(go.Bar(x=sites, y=[798, 694, 685, 686, 707])))
    return barChart


app.layout = html.Div(
    children=[
        html.H1(children="Optimization Model Results",),
        html.P(
            children="This model reallocates health professionals"
                     "in Washington State so that each hospital has "
                     "a fair amount of health staff members based"
                     "on a designated population-staff ratio.",
        ),
        get_chart(),
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
