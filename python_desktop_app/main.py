import time
import serial
from serial.tools import list_ports
import plotly.graph_objects as go
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import collections
import pandas as pd

# Wyszukaj urządzenia podłączone do komputera przez port szeregowy
ports = serial.tools.list_ports.comports() #serial.tools.list_ports.comports()
device = None


for port in ports:
    #print("port", port)
    if 'Pico' in port.description:
        device = port.device
        break

if device is None:
    print("Nie znaleziono urządzenia")
else:
    print("Znaleziono urządzenie: ", device)

ser = serial.Serial(device, 9600)

commands = ['H1-ON', 'H2-ON', 'H3-ON', 'P1-ON', 'H1-OFF', 'H2-OFF', 'H3-OFF', 'P1-OFF', 'T0-?', 'T1-?', 'T2-?', 'T3-?']
temperatures = list(range(65, 101, 5))
# Queue to store history of data
data_queue = collections.deque(maxlen=120*2)  # store data for last 2 minutes (120s * 2 per second)

def send_command(command):
    ser.write((command + '\n').encode())
    time.sleep(0.1)  # Ogranicz do 100ms
    response = ser.readline().decode().strip()  # Odczytaj potwierdzenie
    print('Odpowiedź: ', response)
    data_queue.append((pd.Timestamp.now(), command.split('-')[0], 100 if 'ON' in response else 0))

app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(children="Sterownik przepływowym podgrzewaniem wody", style={'text-align': 'center', 'margin-bottom': '30px'}),
        html.Button('Zmień stan', id='toggle-button', n_clicks=0,
            style={
                'background': '#FF4742',
                'border': '1px solid #FF4742',
                'borderRadius': '6px',
                'boxShadow': 'rgba(0, 0, 0, 0.1) 1px 2px 4px',
                'color': '#FFFFFF',
                'cursor': 'pointer',
                'display': 'inline-block',
                'fontFamily': 'nunito, roboto, proxima-nova, "proxima nova", sans-serif',
                'fontSize': '16px',
                'fontWeight': '800',
                'lineHeight': '16px',
                'minHeight': '40px',
                'outline': '0',
                'padding': '12px 14px',
                'textAlign': 'center',
                'userSelect': 'none',
                'verticalAlign': 'middle',
                'width': '200px',
                'marginBottom': '30px'
            }
        ),
        html.Label('Wybierz temperaturę, do której chcesz podgrzać wodę:'),
        dcc.Dropdown(
            id='temperature-dropdown',
            options=[{'label': str(temp), 'value': temp} for temp in temperatures],
            value=temperatures[0]
        ),
        html.Div(id='selected-temperature'),
        dcc.Graph(id="live-chart", style={'height': '80vh', 'width': '100%'}),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ],
    style={'width': '100%', 'height': '100vh', 'margin': 'auto'}
)


@app.callback(Output("toggle-button", "children"), Input("toggle-button", "n_clicks"))
def toggle_devices(n_clicks):
    if n_clicks % 2 == 0:
        for command in commands[:4]:
            send_command(command)
        return 'Wyłącz wszystko'
    else:
        for command in commands[4:8]:
            send_command(command)
        return 'Włącz wszystko'

@app.callback(Output('selected-temperature', 'children'), Input('temperature-dropdown', 'value'))
def update_selected_temperature(selected_temperature):
    return html.H3(f'Wybrana temperatura: {selected_temperature}')

@app.callback(Output("live-chart", "figure"), Input("interval-component", "n_intervals"))
def update_graph(n_intervals):
    data = pd.DataFrame(data_queue, columns=['time', 'pin', 'state'])

    fig = go.Figure()
    device_names = {'H1': 'Grzałka 1', 'H2': 'Grzałka 2', 'H3': 'Grzałka 3', 'P1': 'Pompka'}
    for pin in ['H1', 'H2', 'H3', 'P1']:
        pin_data = data[data.pin == pin]
        fig.add_trace(go.Scatter(x=pin_data.time, y=pin_data.state, mode='lines+markers', name=device_names[pin]))

    fig.update_layout(
        yaxis=dict(
            range=[0, 100],
            tickvals=[0, 100],
            ticktext=['Wyłączone', 'Włączone'],
            title='Stan urządzeń'
        ),
        xaxis=dict(
            title='Czas'
        )
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
