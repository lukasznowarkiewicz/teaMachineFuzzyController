####################### - IMPORT - #######################
import time
import serial
from serial.tools import list_ports
import plotly.graph_objects as go
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import collections
import random
import time
import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mb
import matplotlib.pyplot as plt

####################### - Połączenie z PICO LINUX/macOS version - #######################
ports = serial.tools.list_ports.comports() #serial.tools.list_ports.comports()
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

####################### - Połączenie z PICO Windows version (manual) - #######################
# ser = serial.Serial('COM3')  # Zastąp 'COM3' właściwym portem
# try:
#     ser.write(b'hello world')
# except Exception as e:
#     print("Error occurred:", str(e))


####################### - Functions for sending and receiving data over UART - #######################
def send_command(command): # for example: 'H1-ON'
    ser.write((command + '\n').encode())
    # time.sleep(0.5)
    # time.sleep(0.1)  # Ogranicz do 100ms
    # response = ser.readline().decode().strip()  # Odczytaj potwierdzenie
    # print('Wyslano: ', command)

def read_temperature(n):        #n - numer porządkowy czujnika: 0,1,2,3
    command = 'T'+str(n)+'-?\n'
    ser.write(command.encode())  # Wysłanie komendy odczytu temperatury T0
    # time.sleep(0.1)
    response = ser.readline().decode().strip()
    # print('Odpowiedź T'+str(n)+':', response)
    if response.startswith('T'+str(n)+'-'):
        temperature = int(response.split('-')[1])
    return temperature


####################### - Control functions - #######################

def fuzzyCtrl(setTemp, T0, T1, T2, T3):
    # Inicjalizacja
    temp_max = 120.0
    heater_power = 10
    desired_temperature = setTemp  # zmienna do zdefiniowania temperatury zadanej
    inlet_temperature = T0
    desired_t0 = (desired_temperature - inlet_temperature) / 3 * 1
    desired_t1 = (desired_temperature - inlet_temperature) / 3 * 2
    desired_t2 = (desired_temperature - inlet_temperature) / 3 * 3
    desired_t3 = desired_temperature
    # print("Desired T0: " + str(round(desired_t0)) + " Desired T1: " + str(round(desired_t1)) + " Desired T2: " + str(round(desired_t2)) + " Desired T3: " + str(round(desired_t3)))

    read_t0 = T0  # zmienne na przyszłość do przypisywania wartości odczytywanych z czujników temperatury
    read_t1 = T1
    read_t2 = T2
    read_t3 = T3

    # Zmienne
    x_t0 = np.arange(0, temp_max, 1)
    x_t1 = np.arange(0, temp_max, 1)
    x_t2 = np.arange(0, temp_max, 1)
    x_t3 = np.arange(0, temp_max, 1)
    # print("Read T0: " + str(round(read_t0)) + " READ T1: " + str(round(read_t1)) + " READ T2: " + str(round(read_t2)) + " READ T3: " + str(round(read_t3)))
    y_t_desired = np.arange(0, temp_max, 1)

    # Funkcje członkowstwa - powinny być tablicami floatów
    t0_cold = mb.trapmf(x_t0, [-20, -10, desired_t0 - 10, desired_t0 - 5])
    t0_ok = mb.trapmf(x_t0, [desired_t0 - 10, desired_t0 - 5, desired_t0 + 5, desired_t0 + 10])
    t0_hot = mb.trapmf(x_t0, [desired_t0 + 5, desired_t0 + 10, 110, 120])

    t1_cold = mb.trapmf(x_t1, [-20, -10, desired_t1 - 10, desired_t1 - 5])
    t1_ok = mb.trapmf(x_t1, [desired_t1 - 10, desired_t1 - 5, desired_t1 + 5, desired_t1 + 10])
    t1_hot = mb.trapmf(x_t1, [desired_t1 + 5, desired_t1 + 10, 110, 120])

    t2_cold = mb.trapmf(x_t2, [-20, -10, desired_t2 - 10, desired_t2 - 5])
    t2_ok = mb.trapmf(x_t2, [desired_t2 - 10, desired_t2 - 5, desired_t2 + 5, desired_t2 + 10])
    t2_hot = mb.trapmf(x_t2, [desired_t2 + 5, desired_t2 + 10, 110, 120])

    t3_cold = mb.trapmf(x_t3, [-20, -10, desired_t3 - 10, desired_t3 - 5])
    t3_ok = mb.trapmf(x_t3, [desired_t3 - 10, desired_t3 - 5, desired_t3 + 5, desired_t3 + 10])
    t3_hot = mb.trapmf(x_t3, [desired_t3 + 5, desired_t3 + 10, 110, 120])

    # Funkcje członkowstwa dla wyjścia - równie tablice floatów

    # wersja ze skalowaniem zakresow jak są powyzej 70 stopni zeby nie przekroczyc 100 stopni
    temp_step = 2 * desired_temperature / 7.5

    temp_very_very_low = mb.trapmf(y_t_desired, [0, 0, temp_step, 1.5 * temp_step])
    temp_very_low = mb.trapmf(y_t_desired, [temp_step, 1.5 * temp_step, 2 * temp_step, 2.5 * temp_step])
    temp_low = mb.trapmf(y_t_desired, [2 * temp_step, 2.5 * temp_step, 3 * temp_step, 3.5 * temp_step])
    temp_ok = mb.trapmf(y_t_desired, [3 * temp_step, 3.5 * temp_step, 4 * temp_step, 4.5 * temp_step])

    if desired_temperature > 60:
        temp_high_pivot = (temp_max - desired_temperature) / 4
        temp_very_high_pivot = 2 * (temp_max - desired_temperature) / 4
        temp_very_very_high_pivot = 3 * (temp_max - desired_temperature) / 4
        temp_high = mb.trapmf(y_t_desired, [desired_temperature + temp_high_pivot - temp_high_pivot * 0.5,
                                            desired_temperature + temp_high_pivot - temp_high_pivot * 0.25,
                                            desired_temperature + temp_high_pivot + temp_high_pivot * 0.25,
                                            desired_temperature + temp_high_pivot + temp_high_pivot * 0.5])
        temp_very_high = mb.trapmf(y_t_desired,
                                   [desired_temperature + temp_very_high_pivot - temp_very_high_pivot * 0.5,
                                    desired_temperature + temp_very_high_pivot - temp_very_high_pivot * 0.25,
                                    desired_temperature + temp_very_high_pivot + temp_very_high_pivot * 0.25,
                                    desired_temperature + temp_very_high_pivot + temp_very_high_pivot * 0.5])
        temp_very_very_high = mb.trapmf(y_t_desired, [
            desired_temperature + temp_very_very_high_pivot - temp_very_very_high_pivot * 0.5,
            desired_temperature + temp_very_very_high_pivot - temp_very_very_high_pivot * 0.25,
            desired_temperature + temp_very_very_high_pivot + temp_very_high_pivot * 0.25,
            desired_temperature + temp_very_very_high_pivot + temp_very_very_high_pivot * 0.5])
    else:
        scaling_factor = 1
        temp_high = mb.trapmf(y_t_desired, [scaling_factor * 4 * temp_step, scaling_factor * 4.5 * temp_step,
                                            scaling_factor * 5 * temp_step, scaling_factor * 5.5 * temp_step])
        temp_very_high = mb.trapmf(y_t_desired, [scaling_factor * 5 * temp_step, scaling_factor * 5.5 * temp_step,
                                                 scaling_factor * 6 * temp_step, scaling_factor * 6.5 * temp_step])
        temp_very_very_high = mb.trapmf(y_t_desired, [scaling_factor * 5.5 * temp_step, scaling_factor * 6 * temp_step,
                                                      2 * min(desired_temperature, 100) - 1,
                                                      2 * min(desired_temperature, 100)])

    # Odrozmywanie

    # Stopień członkowstwa - rozmywanie - wyrzuca pojedyncze floaty
    t0_fit_cold = fuzz.interp_membership(x_t0, t0_cold, read_t0)
    t0_fit_ok = fuzz.interp_membership(x_t0, t0_ok, read_t0)
    t0_fit_hot = fuzz.interp_membership(x_t0, t0_hot, read_t0)

    t1_fit_cold = fuzz.interp_membership(x_t1, t1_cold, read_t1)
    t1_fit_ok = fuzz.interp_membership(x_t1, t1_ok, read_t1)
    t1_fit_hot = fuzz.interp_membership(x_t1, t1_hot, read_t1)

    t2_fit_cold = fuzz.interp_membership(x_t2, t2_cold, read_t2)
    t2_fit_ok = fuzz.interp_membership(x_t2, t2_ok, read_t2)
    t2_fit_hot = fuzz.interp_membership(x_t2, t2_hot, read_t2)

    t3_fit_cold = fuzz.interp_membership(x_t3, t3_cold, read_t3)
    t3_fit_ok = fuzz.interp_membership(x_t3, t3_ok, read_t3)
    t3_fit_hot = fuzz.interp_membership(x_t3, t3_hot, read_t3)

    # print(f"T0 fits: Cold: {t0_fit_cold}, OK: {t0_fit_ok}, Hot: {t0_fit_hot}")
    # print(f"T1 fits: Cold: {t1_fit_cold}, OK: {t1_fit_ok}, Hot: {t1_fit_hot}")
    # print(f"T2 fits: Cold: {t2_fit_cold}, OK: {t2_fit_ok}, Hot: {t2_fit_hot}")
    # print(f"T3 fits: Cold: {t3_fit_cold}, OK: {t3_fit_ok}, Hot: {t3_fit_hot}")

    # Zasady - powinny byc jako array floatów
    # # 3 za zimno
    rule1 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_cold, t1_fit_cold), t2_fit_cold), t3_fit_cold), temp_very_very_low)

    # 2 za zimno
    rule2 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t1_fit_cold), np.fmin(t2_fit_ok, t3_fit_ok)), temp_very_low)
    rule3 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t2_fit_cold), np.fmin(t1_fit_ok, t3_fit_ok)), temp_very_low)
    rule4 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t3_fit_cold), np.fmin(t1_fit_ok, t2_fit_ok)), temp_very_low)
    rule5 = np.fmin(np.fmin(np.fmin(t1_fit_cold, t2_fit_cold), np.fmin(t0_fit_ok, t3_fit_ok)), temp_very_low)
    rule6 = np.fmin(np.fmin(np.fmin(t1_fit_cold, t3_fit_cold), np.fmin(t0_fit_ok, t2_fit_ok)), temp_very_low)
    rule7 = np.fmin(np.fmin(np.fmin(t2_fit_cold, t3_fit_cold), np.fmin(t0_fit_ok, t1_fit_ok)), temp_very_low)

    # 1 za zimno
    rule8 = np.fmin(np.fmin(t0_cold, np.fmin(np.fmin(t1_fit_ok, t2_fit_ok), t3_fit_ok)), temp_low)
    rule9 = np.fmin(np.fmin(t1_fit_cold, np.fmin(np.fmin(t0_fit_ok, t2_fit_ok), t3_fit_ok)), temp_low)
    rule10 = np.fmin(np.fmin(t2_fit_cold, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t3_fit_ok)), temp_low)
    rule11 = np.fmin(np.fmin(t3_fit_cold, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok)), temp_low)

    # wszystkie ok
    rule12 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok), t3_fit_ok), temp_ok)

    # 1 za ciepło
    rule13 = np.fmin(np.fmin(t0_fit_hot, np.fmin(np.fmin(t1_fit_ok, t2_fit_ok), t3_fit_ok)), temp_high)
    rule14 = np.fmin(np.fmin(t1_fit_hot, np.fmin(np.fmin(t0_fit_ok, t2_fit_ok), t3_fit_ok)), temp_high)
    rule15 = np.fmin(np.fmin(t2_fit_hot, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t3_fit_ok)), temp_high)
    rule16 = np.fmin(np.fmin(t3_fit_hot, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok)), temp_high)

    # 2 za ciepło
    rule17 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t1_fit_hot), np.fmin(t2_fit_ok, t3_fit_ok)), temp_very_high)
    rule18 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t2_fit_hot), np.fmin(t1_fit_ok, t3_fit_ok)), temp_very_high)
    rule19 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t3_fit_hot), np.fmin(t1_fit_ok, t2_fit_ok)), temp_very_high)
    rule20 = np.fmin(np.fmin(np.fmin(t1_fit_hot, t2_fit_hot), np.fmin(t0_fit_ok, t3_fit_ok)), temp_very_high)
    rule21 = np.fmin(np.fmin(np.fmin(t1_fit_hot, t3_fit_hot), np.fmin(t0_fit_ok, t2_fit_ok)), temp_very_high)
    rule22 = np.fmin(np.fmin(np.fmin(t2_fit_hot, t3_fit_hot), np.fmin(t0_fit_ok, t1_fit_ok)), temp_very_high)

    # 3 za ciepło
    rule23 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_hot, t1_fit_hot), t2_fit_hot), t3_fit_hot), temp_very_very_high)

    rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
             rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21,
             rule22, rule23]


    # Zestawy zaagregowane
    out_very_very_cold = rule1
    out_very_cold = np.fmax(rule2, np.fmax(rule3, np.fmax(rule4, np.fmax(rule5, np.fmax(rule6, rule7)))))
    out_cold = np.fmax(rule8, np.fmax(rule9, np.fmax(rule10, rule11)))
    out_ok = rule12
    out_hot = np.fmax(rule13, np.fmax(rule14, np.fmax(rule15, rule16)))
    out_very_hot = np.fmax(rule17, np.fmax(rule18, np.fmax(rule19, np.fmax(rule20, np.fmax(rule21, rule22)))))
    out_very_very_hot = rule23


    if max(t1_fit_cold, t1_fit_ok, t1_fit_hot) == t1_fit_cold:
        H1ctrlcmd = 'H1-ON'
    elif max(t1_fit_cold, t1_fit_ok, t1_fit_hot) == t1_fit_ok:
        H1ctrlcmd = 'H1-OFF'
    else:
        H1ctrlcmd = 'H1-OFF'
    # print(H1ctrlcmd)

    if max(t2_fit_cold, t2_fit_ok, t2_fit_hot) == t2_fit_cold:
        H2ctrlcmd = 'H2-ON'
    elif max(t2_fit_cold, t2_fit_ok, t2_fit_hot) == t2_fit_ok:
        H2ctrlcmd = 'H2-OFF'
    else:
        H2ctrlcmd = 'H2-OFF'
    # print(H2ctrlcmd)

    if max(t3_fit_cold, t3_fit_ok, t3_fit_hot) == t3_fit_cold:
        H3ctrlcmd = 'H3-ON'
    elif max(t3_fit_cold, t3_fit_ok, t3_fit_hot) == t3_fit_ok:
        H3ctrlcmd = 'H3-OFF'
    else:
        H3ctrlcmd = 'H3-OFF'
    # print(H3ctrlcmd)

    return H1ctrlcmd, H2ctrlcmd, H3ctrlcmd

def updateControl(setTemperature):
    # Turning on pump:
    P1ctrlcmd = 'P1-ON'
    send_command(P1ctrlcmd)

    # Reading temperatures
    T0 = read_temperature(0)
    T1 = read_temperature(1)
    T2 = read_temperature(2)
    T3 = read_temperature(3)

    # Fuzzy controller implementation
    H1ctrlcmd, H2ctrlcmd, H3ctrlcmd = fuzzyCtrl(setTemperature, T0, T1, T2, T3)

    # H1ctrlcmd = "H1-OFF"
    # H2ctrlcmd = "H2-OFF"
    # H3ctrlcmd = "H3-OFF"
    # Sending control commands based on current system state
    send_command(H1ctrlcmd)
    send_command(H2ctrlcmd)
    send_command(H3ctrlcmd)

    # Reading temperatures swcond time -  for debug purposes
    T0 = read_temperature(0)
    T1 = read_temperature(1)
    T2 = read_temperature(2)
    T3 = read_temperature(3)
    T3 = read_temperature(3)
    T3 = read_temperature(3)


    # For testing purposes - rand temperatures
    # T0 = random.randint(10, 20)
    # T1 = random.randint(20, 40)
    # T2 = random.randint(40, 50)
    # T3 = random.randint(50, 60)

    # For debug purposes write all states on terminal
    print(f"Stany urządzeń: P1: {P1ctrlcmd}, H1: {H1ctrlcmd}, H2: {H2ctrlcmd}, H3: {H3ctrlcmd} Odczyty temperatur: T0: {T0}°C, T1: {T1}°C, T2: {T2}°C, T3: {T3}°C")

    return T3 # returns temperature on the output

####################### - Debugging loop - #######################
while True:
    cos=updateControl(70)
