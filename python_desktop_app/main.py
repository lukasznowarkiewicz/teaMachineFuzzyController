import time
import serial
import serial.tools.list_ports
import plotly.graph_objects as go
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import threading
import collections
import queue

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

def update_data():
    while True:
        for command in commands:
            ser.write((command + '\n').encode())
            time.sleep(1)
            response = ser.readline().decode().strip()  # Odczytaj potwierdzenie
            print('Odpowiedź: ', response)
            data_queue.append((time.time(), command, response))

threading.Thread(target=update_data).start()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Arduino GPIO states",),
        dcc.Graph(id="live-chart",),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ]
)

@app.callback(Output("live-chart", "figure"), Input("interval-component", "n_intervals"))
def update_graph(n):
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
