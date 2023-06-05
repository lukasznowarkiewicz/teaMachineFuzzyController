#include <OneWire.h>
#include <DallasTemperature.h>

#define H1 18
#define H2 19
#define H3 20
#define P1 21
#define ONE_WIRE_BUS 6 // Pin dla DS18B20

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(H1, OUTPUT);
  pinMode(H2, OUTPUT);
  pinMode(H3, OUTPUT);
  pinMode(P1, OUTPUT);

  digitalWrite(H1, LOW);
  digitalWrite(H2, LOW);
  digitalWrite(H3, LOW);
  digitalWrite(P1, LOW);

//  sensors.begin();
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }
}

void handleCommand(String command) {
  command.trim();
  String module = command.substring(0, 2);
  String action = command.substring(3);

  int pin;

  if (module == "H1") {
    pin = H1;
  } else if (module == "H2") {
    pin = H2;
  } else if (module == "H3") {
    pin = H3;
  } else if (module == "P1") {
    pin = P1;
  } else if (module == "T1" && action == "?") {
    readTemperature(0);
    return;
  } else if (module == "T2" && action == "?") {
    readTemperature(1);
    return;
  } else {
    Serial.println("Nieznany moduł: " + module);
    return;
  }

  if (action == "ON") {
    digitalWrite(pin, HIGH);
    Serial.println(command + "-OK"); // potwierdzenie akcji
  } else if (action == "OFF") {
    digitalWrite(pin, LOW);
    Serial.println(command + "-OK"); // potwierdzenie akcji
  } else {
    Serial.println("Nieznana akcja: " + action);
  }
}

void readTemperature(int sensorIndex) {
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(sensorIndex); 
  Serial.print("T" + String(sensorIndex + 1) + "-");
  Serial.print(tempC);
  Serial.println("C");
  Serial.println("T" + String(sensorIndex + 1) + "-?-OK"); // potwierdzenie akcji
}
