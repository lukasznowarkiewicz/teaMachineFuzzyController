import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from collections import deque
import random
import datetime
from dash.dependencies import Output, Input, State


temperatures = list(range(65, 101, 5))

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the layout
app.layout = html.Div(
    children=[
        html.H1(children="Sterownik przepływowym podgrzewaniem wody", style={'text-align': 'center', 'margin-bottom': '30px'}),

        html.Label('Wybierz temperaturę, do której chcesz podgrzać wodę:'),
        dcc.Dropdown(
            id='temperature-dropdown',
            options=[{'label': str(temp), 'value': temp} for temp in temperatures],
            value=temperatures[0]
        ),
        html.Div(id='selected-temperature'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1000),     #tu odświerza graf co sekundę
    ],
    style={'width': '100%', 'height': '100vh', 'margin': 'auto'}
)




# Initialize empty data
X = deque(maxlen=20)
Y = deque(maxlen=20)

# Define the callback function to update the graph      #, [Input('graph-update', 'n_intervals')]
@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')],[State('temperature-dropdown', 'value')])   #,[State('temperature-dropdown', 'value')]
def update_graph(n, selected_temperature):     #
    global X, Y

    #T4 = updateControl(selected_temperature)

    X.append(datetime.datetime.now())
    Y.append(updateControl(selected_temperature))
    #Y.append(random.randint(23, 110)) #temp

    # Create the graph trace
    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Temperature',
        mode='lines+markers'
    )

    # Set the graph layout
    layout = go.Layout(
        xaxis=dict(range=[min(X), max(X)], title='Time'),
        yaxis=dict(range=[23, 110], title='Temperature'),
    )

    # Create the figure
    figure = go.Figure(data=[data], layout=layout)
    return figure


@app.callback(Output('selected-temperature', 'children'), Input('temperature-dropdown', 'value'))
def update_selected_temperature(selected_temperature):
        #tutaj przekaz zadaną temp po usb
        return html.H3(f'Wybrana temperatura: {selected_temperature}')


def updateControl(selected_temperature):
    #caly alogrytm sterowania
    #po czym odczytanie temperatury
    T1 = selected_temperature + random.randint(-2, 2)
    T2 = selected_temperature + random.randint(-2, 2)
    T3 = selected_temperature + random.randint(-2, 2)
    T4 = selected_temperature + random.randint(-5, 5)
    return T4



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
