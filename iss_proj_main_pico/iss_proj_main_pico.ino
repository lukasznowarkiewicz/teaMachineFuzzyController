#include "Arduino.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include "Adafruit_PCF8575.h" // library for IO expanders on I2C line
Adafruit_PCF8575 pcf;

#define H1 2
#define H2 3
#define H3 0
#define P1 1
#define T0 6
#define T1 22
#define T2 22
#define T3 22
//#define ONE_WIRE_BUS 6 // Pin dla DS18B20

void setup() {
  pinMode(H1, OUTPUT);
  pinMode(H2, OUTPUT);
  pcf.begin(0x21, &Wire);
  pcf.pinMode(H3, OUTPUT);
  pcf.pinMode(P1, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
//  pinMode(T0, OUTPUT);
//  pinMode(TO, INPUT_PULLUP)

  pcf.digitalWrite(H3, HIGH);
  pcf.digitalWrite(P1, HIGH);
  digitalWrite(H1, HIGH);
  digitalWrite(H2, HIGH);
  digitalWrite(T0, LOW);  
  //  sensors.begin();
  
  Serial.begin(9600);
  digitalWrite(LED_BUILTIN, HIGH);
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
    if (action == "ON") {
      digitalWrite(pin, LOW);
    } else if (action == "OFF") {
      digitalWrite(pin, HIGH);
    } else {
      Serial.println("Nieznana akcja: " + action);
    }
  } else if (module == "H2") {
    pin = H2;
    if (action == "ON") {
      digitalWrite(pin, LOW);
    } else if (action == "OFF") {
      digitalWrite(pin, HIGH);
    } else {
      Serial.println("Nieznana akcja: " + action);
    }
  } else if (module == "H3") {
    pin = H3;
    
    if (action == "ON") {
      pcf.digitalWrite(pin, LOW);
    } else if (action == "OFF") {
      pcf.digitalWrite(pin, HIGH);
    } else {
      Serial.println("Nieznana akcja: " + action);
    }
  } else if (module == "P1") {
    pin = P1;
    if (action == "ON") {
      pcf.digitalWrite(pin, LOW);
    } else if (action == "OFF") {
      pcf.digitalWrite(pin, HIGH);
    } else {
      Serial.println("Nieznana akcja: " + action);
    }
  } else if (module == "T1" && action == "?") {
//    readTemperature(0);
    return;
  } else if (module == "T2" && action == "?") {
//    readTemperature(1);
    return;
  } else {
    Serial.println("Nieznany moduł: " + module);
    return;
  }

}
