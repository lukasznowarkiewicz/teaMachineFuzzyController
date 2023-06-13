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
        html.Label('Wybierz liczbę temperatur do wyświetlenia na wykresie:'),
        dcc.Dropdown(
            id='num-temperatures-dropdown',
            options=[{'label': str(i+1), 'value': str(i+1)} for i in range(4)],
            value='1'
        ),
        html.Div(id='selected-temperature'),
        #html.Div(id='num-temperatures'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1000),     #tu odświerza graf co sekundę
    ],
    style={'width': '100%', 'height': '100vh', 'margin': 'auto'}
)




# Initialize empty data
X = deque(maxlen=20)
Y = deque(maxlen=20)
Y2 = deque(maxlen=20)
Y3 = deque(maxlen=20)
Y4 = deque(maxlen=20)


# Define the callback function to update the graph      #, [Input('graph-update', 'n_intervals')]
@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')],[State('temperature-dropdown', 'value'), State('num-temperatures-dropdown', 'value')])   #,[State('temperature-dropdown', 'value')]
def update_graph(n, selected_temperature, num_temperatures):     #
    global X, Y, Y2, Y3, Y4

    #T4 = updateControl(selected_temperature)
    #Y.append(random.randint(23, 110)) #temp

    T1, T2, T3, T4 = updateControl(selected_temperature)

    X.append(datetime.datetime.now())
    Y.append(T1)
    Y2.append(T2)
    Y3.append(T3)
    Y4.append(T4)

    # Create the graph trace



    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='T1',
        mode='lines+markers'
    )

    data2 = go.Scatter(
        x=list(X),
        y=list(Y2),
        name='T2',
        mode='lines+markers'
    )

    data3 = go.Scatter(
        x=list(X),
        y=list(Y3),
        name='T3',
        mode='lines+markers'
    )

    data4 = go.Scatter(
        x=list(X),
        y=list(Y4),
        name='T4',
        mode='lines+markers'
    )

    # Set the graph layout
    layout = go.Layout(
        xaxis=dict(range=[min(X), max(X)], title='Time'),
        yaxis=dict(range=[23, 110], title='Temperature'),
    )

    # Create the figure
    figure = go.Figure(data=[data], layout=layout)

    if num_temperatures == '1':
        figure = go.Figure(data=[data], layout=layout)
    elif num_temperatures == '2':
        figure = go.Figure(data=[data, data2], layout=layout)
    elif num_temperatures == '3':
        figure = go.Figure(data=[data, data2, data3], layout=layout)
    elif num_temperatures == '4':
        figure = go.Figure(data=[data, data2, data3, data4], layout=layout)


    # figure = go.Figure(data=[data, data2], layout=layout)
    return figure


@app.callback(Output('selected-temperature', 'children'), Input('temperature-dropdown', 'value'))
def update_selected_temperature(selected_temperature):
        #tutaj przekaz zadaną temp po usb
        return html.H3(f'Wybrana temperatura: {selected_temperature}')

# @app.callback(Output('num-temperatures', 'children'), Input('num-temperatures-dropdown', 'value'))
# def update_num_temperatures(num_temperatures):
#         #tutaj przekaz zadaną temp po usb
#         return html.H6(f'Wybrana liczba pomiarów na wykresie: {num_temperatures}')


def updateControl(selected_temperature):
    #caly alogrytm sterowania
    #po czym odczytanie temperatury
    T1 = selected_temperature + random.randint(-2, 2)
    T2 = selected_temperature + random.randint(-2, 2)
    T3 = selected_temperature + random.randint(-2, 2)
    T4 = selected_temperature + random.randint(-5, 5)
    return T1, T2, T3, T4



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
