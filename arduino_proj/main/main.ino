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

#define INNERTIA_UP 6
#define INNERTIA_DOWN 3

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

int program_time = 0;

int times[7] = {0, 0, 0, 0, 0, 0, 0}; //dodawac do pierwszej cos w stylu 6, a do drugiej 3 przy High i low, ||a potem odejmowac/dodawact to *1, *2  //[2][3]
int (*p) = times;
int tempC1 = ROOM_TEMP;
int tempC2 = ROOM_TEMP;
int tempC3 = ROOM_TEMP;

int rando()
{
    srand(time(NULL));
    int myArray[5] = { -2, -1, 0, 1, 2 };
    int randomIndex = rand() % 5;
    int randomValue = myArray[randomIndex];
    return randomValue;
}

//jeśli grzalka ile zmienia się temperatura
int deltaTemp1(){
  int inertia = (-times[0]) + (times[3]*2);//*2);
  return (digitalRead(H1)* DELTA_H1) + inertia; 
}


int deltaTemp2(){
  int inertia = -times[0]-times[1] + times[3]*2+times[4]*2;
  return digitalRead(H1)* DELTA_H1 + digitalRead(H2)* DELTA_H2 + inertia; // + rando(); +off  //-times[1][1]-times[1][2]    +times[2][1]*2+times[2][2]*2
}

int deltaTemp3(){
  int inertia = -times[0]-times[1]-times[2] + times[3]*2+times[4]*2+times[5]*2;
  return digitalRead(H1)* DELTA_H1 + digitalRead(H2)* DELTA_H2 + digitalRead(H3)* DELTA_H3 + inertia; // + rando();  //-times[1][1]-times[1][2]-times[1][3]     +times[2][1]*2+times[2][2]*2+times[2][3]*2
}


void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    //zmiana nagrzania/chlodzenia sie grzalki z zachowaniem bezwladnosci
    for(int i; i<6; i++){
      if(p[i]>0)
        p[i] = p[i]-1;
    }

    //stopniowe grzanie sie/ chłodzenie wody
    int delta = deltaTemp1();
    if(tempC1 <MAX_TEMP)
    { 
      if(delta == 0 && tempC1>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta += -2;
    }else
      if(delta == 0)
        delta += -2;
      else
        delta = 0;

    tempC1 += delta;

    delta = deltaTemp2();
    if(tempC2 <MAX_TEMP)
    { 
      if(delta == 0 && tempC2>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta += -2;
    }else
      if(delta == 0)
        delta += -2;
      else
        delta = 0;
        
    tempC2 += delta;
    delta = deltaTemp3();
    if(tempC3 <MAX_TEMP)
    { 
      if(delta == 0 && tempC3>ROOM_TEMP) //jesli zadna grzalka nie grzeje
        delta += -2;
    }else
      if(delta == 0)
        delta += -2;
      else
        delta = 0;
    
    tempC3 += delta;
    
    p = handleCommand(command, tempC1, tempC2, tempC3, p);  

  }
}

int* handleCommand(String command, int tempC1, int tempC2, int tempC3, int times[]) {
  command.trim();
  String module = command.substring(0, 2);
  String action = command.substring(3);

  int pin;
  int pin_num = 0;
     
  if (module == "H1") {
    pin = H1;
    pin_num = 1;
  } else if (module == "H2") {
    pin = H2;
    pin_num = 2;
  } else if (module == "H3") {
    pin = H3;
    pin_num = 3;
  } else if (module == "P1") {
    pin = P1;
  } else if (module == "T0" && action == "?") {
    printTemperature(ROOM_TEMP, "T0");
    //Serial.println();
    return times;
  } else if (module == "T1" && action == "?") {
    printTemperature(tempC1, "T1");
    //Serial.println();
    return times;
  } else if (module == "T2" && action == "?") {
    printTemperature(tempC2, "T2");
    //Serial.println();
    return times;
   } else if (module == "T3" && action == "?") {
    printTemperature(tempC3, "T3");
    //Serial.println();
    return times;
  } else {
    //Serial.println("Nieznany moduł: " + module);
    return times;
  }

  if (action == "ON") {
    
    digitalWrite(pin, HIGH);
    times[pin_num-1] = INNERTIA_UP;  //times
    if(times[3 + pin_num-1] != 0)
      times[pin_num-1] = (6 - times[3 + pin_num-1])+1;
      times[3 + pin_num-1] = 0;
    
    //Serial.println(command + "-OK"); // potwierdzenie akcji
  } else if (action == "OFF") {
    
    digitalWrite(pin, LOW);
    
    times[3 + pin_num-1] = INNERTIA_DOWN;  //times[1]
    if(times[pin_num-1] != 0)
      times[3 + pin_num-1] = int((6 - times[ pin_num-1])/2)+1;
      times[pin_num-1] = 0;

    //Serial.println("\n" + command + "-OK" + "\n"); // potwierdzenie akcji
  } else {
    //Serial.println("Nieznana akcja: " + action);
  }
  return times;
}

// function to print the temperature for a device
void printTemperature(int tempC, String T)
{
  //Serial.println();
  //Serial.print("TEMP C: ");
  Serial.print(T + "-" + String(tempC + rando() ) ); //+ rando() T1-90C
  Serial.println();
}
