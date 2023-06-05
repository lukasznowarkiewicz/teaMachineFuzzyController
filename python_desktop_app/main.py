import time
import serial
import serial.tools.list_ports

# Wyszukaj urządzenia podłączone do komputera przez port szeregowy
ports = serial.tools.list_ports.comports()
device = None

for port in ports:
    # W tym miejscu wprowadź odpowiednią nazwę swojego urządzenia lub jego ID
    # W zależności od systemu operacyjnego, może to wyglądać inaczej
    # Na przykład, na Windowsie może to być 'COM3', na Linuxie '/dev/ttyACM0', itp.
    if 'Pico' in port.description:
        device = port.device
        break

if device is None:
    print("Nie znaleziono urządzenia")
else:
    print("Znaleziono urządzenie: ", device)

    # Otwórz połączenie szeregowe z urządzeniem
    ser = serial.Serial(device, 9600)

    commands = ['H1-ON', 'H2-ON', 'H3-ON', 'H1-OFF', 'H2-OFF', 'H3-OFF']

    # Sekwencyjnie włącz i wyłącz H1-H3 co jedną sekundę
    while True:
        for command in commands:
            ser.write((command + '\n').encode())
            time.sleep(1)
            response = ser.readline().decode().strip()  # Odczytaj potwierdzenie
            print('Odpowiedź: ', response)
