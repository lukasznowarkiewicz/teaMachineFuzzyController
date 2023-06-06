

#define H1 18
#define H2 19
#define H3 20
#define P1 21
#define T1 22

//ile stopni C ogrzewa przekrów wody w jednostce czasu (tu jedna pętla loop)
#define DELTA_H1 6
#define DELTA_H2 6
#define DELTA_H3 6  //można zrobic jedna delte
//maksymalna temperatura w jakiej grzałka wciaż grzeje
#define MAX_TEMP 120
#define ROOM_TEMP 23

void setup() {
  pinMode(H1, OUTPUT);
  pinMode(H2, OUTPUT);
  pinMode(H3, OUTPUT);
  pinMode(P1, OUTPUT);
  
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(H1, LOW);
  digitalWrite(H2, LOW);
  digitalWrite(H3, LOW);
  digitalWrite(P1, LOW);
  
  Serial.begin(9600);
}

int tempC1 = ROOM_TEMP;
int tempC2 = ROOM_TEMP;
int tempC3 = ROOM_TEMP;

//jeśli grałka ile zmienia się temperatura
int deltaTemp1(){
  return digitalRead(H1)* DELTA_H1;
}

int deltaTemp2(){
  return digitalRead(H1)* DELTA_H1 + digitalRead(H2)* DELTA_H2;
}

int deltaTemp3(){
  return digitalRead(H1)* DELTA_H1 + digitalRead(H2)* DELTA_H2 + digitalRead(H3)* DELTA_H3;
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    //stopniowe grzanie sie/ chłodzenie wody
    int delta = 0;
    if(tempC1 <MAX_TEMP)
    {
      delta = deltaTemp1();
      if(delta == 0 && tempC1>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta = -2;
    }
    tempC1 += delta;

    delta = 0;
    if(tempC2 <MAX_TEMP)
    {
      delta = deltaTemp2();
      if(delta == 0 && tempC2>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta = -2;
    }
    tempC2 += delta;

    delta = 0;
    if(tempC3 <MAX_TEMP)
    {
      delta = deltaTemp3();
      if(delta == 0 && tempC3>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta = -2;
    }
    tempC3 += delta;
    
    handleCommand(command, tempC1, tempC2, tempC3);
  }
}

void handleCommand(String command, int tempC1, int tempC2, int tempC3) {
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
  } else if (module == "T0" && action == "?") {
    printTemperature(ROOM_TEMP);
    return;
  } else if (module == "T1" && action == "?") {
    printTemperature(tempC1);
    return;
  } else if (module == "T2" && action == "?") {
    printTemperature(tempC2);
    return;
   } else if (module == "T3" && action == "?") {
    printTemperature(tempC3);
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

// function to print the temperature for a device
void printTemperature(int tempC)
{
  
  Serial.print("Temp C: ");
  Serial.print(tempC);
}
