#include <OneWire.h>
#include <DallasTemperature.h>

#define H1 18
#define H2 19
#define H3 20
#define P1 21
#define ONE_WIRE_BUS 6 // Pin dla DS18B20
#define T1 22

//ile stopni C ogrzewa przekrów wody w jednostce czasu (tu jedna pętla loop)
#define DELTA_H1 1
#define DELTA_H2 3
#define DELTA_H3 5

//maksymalna temperatura w jakiej grzałka wciaż grzeje
#define MAX_TEMP 120
#define ROOM_TEMP 23

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(H1, OUTPUT);
  pinMode(H2, OUTPUT);
  pinMode(H3, OUTPUT);
  pinMode(P1, OUTPUT);
  
  pinMode(22, INPUT_PULLUP); //built -in input resistance
  pinMode(T1, OUTPUT);
  
  pinMode(LED_BUILTIN, OUTPUT);
  DeviceAddress insideThermometer;

  digitalWrite(H1, LOW);
  digitalWrite(H2, LOW);
  digitalWrite(H3, LOW);
  digitalWrite(P1, LOW);

//  sensors.begin();
  
  Serial.begin(9600);
}

int tempC = ROOM_TEMP;
//jeśli grałka ile zmienia się temperatura
int deltaTemp(){
  return digitalRead(H1)* DELTA_H1 + digitalRead(H2)* DELTA_H1 + digitalRead(H3)* DELTA_H1;
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    //stopniowe grzanie sie/ chłodzenie wody
    int delta = 0;
    if(tempC <MAX_TEMP)
    {
      delta = deltaTemp();
      if(delta == 0 && tempC>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta = -2;
    }
    tempC += delta;
    
    handleCommand(command, tempC);
  }
}

void handleCommand(String command, int tempC) {
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
    readTemperature(0, tempC);
    return;
  } else if (module == "T2" && action == "?") {
    readTemperature(1, tempC);
    return;
  } else if (module == "SE"){
    const char * c = action.c_str();
    int a =atoi(c);
    setTemp(a, tempC, 20);
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

void setTemp(int desiredTemp, int tempC, int timecount){  //String
  if(timecount == 0)
    return;
  //za zimne
  desiredTemp = int(desiredTemp);
  if(desiredTemp>tempC)
  {
    if(digitalRead(H1)==0)
      handleCommand("H1-ON", tempC);
      //digitalWrite(H1, HIGH);
    else if(digitalRead(H2)==0)
      handleCommand("H2-ON", tempC);
    else if(digitalRead(H3)==0)
      handleCommand("H3-ON", tempC);
  }
   //za cieple 
   else if(desiredTemp<tempC)
   {
     if(digitalRead(H1)==1)
      handleCommand("H1-OFF", tempC);
      else if(digitalRead(H2)==1)
        handleCommand("H2-OFF", tempC);
      else if(digitalRead(H3)==1)
        handleCommand("H3-OFF", tempC);
   }
   setTemp(desiredTemp, tempC, timecount-1); 
}

int setDesiredTemperature(int desiredTemp) {
  //read it/ pass from a tea-choice button
  return desiredTemp;
}

void readTemperature(int sensorIndex, int tempC) {
  sensors.requestTemperatures();
  //float tempC = sensors.getTempCByIndex(sensorIndex); 
  Serial.print("T" + String(sensorIndex + 1) + "-");
  Serial.print(tempC);
  Serial.println("C");
  Serial.println("T" + String(sensorIndex + 1) + "-?-OK"); // potwierdzenie akcji
}

// function to print the temperature for a device
void printTemperature(int tempC)
{
  
  Serial.print("Temp C: ");
  Serial.print(tempC);
}
