import time
import serial
import serial.tools.list_ports
import plotly.graph_objects as go
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import collections

# Wyszukaj urządzenia podłączone do komputera przez port szeregowy
ports = serial.tools.list_ports.comports()
device = None

for port in ports:
    if 'Pico' in port.description:
        device = port.device
        break

if device is None:
    print("Nie znaleziono urządzenia")
else:
    print("Znaleziono urządzenie: ", device)

ser = serial.Serial(device, 9600)

commands = ['H1-ON', 'H2-ON', 'H3-ON', 'P1-ON', 'H1-OFF', 'H2-OFF', 'H3-OFF', 'P1-OFF']

# Queue to store history of data
data_queue = collections.deque(maxlen=1000)

def send_command(command):
    ser.write((command + '\n').encode())
    time.sleep(1)
    response = ser.readline().decode().strip()  # Odczytaj potwierdzenie
    print('Odpowiedź: ', response)
    data_queue.append((time.time(), command, response))

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Sterownik przepływowym podgrzewaniem wody",),
        html.Button('Zmiana stanu', id='toggle-button', n_clicks=0),
        dcc.Graph(id="live-chart",),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ]
)

@app.callback(Output("toggle-button", "children"), Input("toggle-button", "n_clicks"))
def toggle_devices(n_clicks):
    if n_clicks % 2 == 0:
        for command in commands[0:4]:  # Turn on devices
            send_command(command)
        return 'Wyłącz grzanie'
    else:
        for command in commands[4:]:  # Turn off devices
            send_command(command)
        return 'Włącz grzanie'

@app.callback(Output("live-chart", "figure"), [Input("toggle-button", "n_clicks"), Input("interval-component", "n_intervals")])
def update_graph(n_clicks, n_intervals):
    data = {'time': [], 'pin': [], 'state': []}
    for item in list(data_queue):
        time_val, command, response = item
        pin, state = command.split('-')
        state_val = 1 if state == 'ON' else 0
        data['time'].append(time_val)
        data['pin'].append(pin)
        data['state'].append(state_val)

    fig = go.Figure()

    device_names = {'H1': 'Grzałka 1', 'H2': 'Grzałka 2', 'H3': 'Grzałka 3', 'P1': 'Pompka'}

    for pin in ['H1', 'H2', 'H3', 'P1']:
        pin_data = [state for t, p, state in zip(data['time'], data['pin'], data['state']) if p == pin]
        pin_time = [t for t, p, state in zip(data['time'], data['pin'], data['state']) if p == pin]
        fig.add_trace(go.Scatter(x=pin_time, y=pin_data, mode='lines+markers', name=device_names[pin]))

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
