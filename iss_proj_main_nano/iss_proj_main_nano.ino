#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 2
#define TEMPERATURE_PRECISION 9 // Lower resolution

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

int numberOfDevices; // Number of temperature devices found

DeviceAddress tempDeviceAddress; // We'll use this variable to store a found device address
//////////////////////////////////////////////////// SETUP ////////////////////////////////////////////////////  
void setup(void)
{
  // start serial port
  Serial.begin(9600);
  Serial.println("Dallas Temperature IC Control");

  // Start up the library
  sensors.begin();
  
  // Grab a count of devices on the wire
  numberOfDevices = sensors.getDeviceCount();
  
  // locate devices on the bus
  Serial.print("Locating devices...");
  
  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");

  // report parasite power requirements
  Serial.print("Parasite power is: "); 
  if (sensors.isParasitePowerMode()) Serial.println("ON");
  else Serial.println("OFF");
  
  // Loop through each device, print out address
  for(int i=0;i<numberOfDevices; i++)
  {
    // Search the wire for address
    if(sensors.getAddress(tempDeviceAddress, i))
  {
    Serial.print("Found device ");
    Serial.print(i, DEC);
    Serial.print(" with address: ");
    printAddress(tempDeviceAddress);
    Serial.println();
    
    Serial.print("Setting resolution to ");
    Serial.println(TEMPERATURE_PRECISION, DEC);
    
    // set the resolution to TEMPERATURE_PRECISION bit (Each Dallas/Maxim device is capable of several different resolutions)
    sensors.setResolution(tempDeviceAddress, TEMPERATURE_PRECISION);
    
    Serial.print("Resolution actually set to: ");
    Serial.print(sensors.getResolution(tempDeviceAddress), DEC); 
    Serial.println();
  }else{
    Serial.print("Found ghost device at ");
    Serial.print(i, DEC);
    Serial.print(" but could not detect address. Check power and cabling");
  }
  }

}
//////////////////////////////////////////////////// FUNCTIONS //////////////////////////////////////////////////// 

void printTemperature(DeviceAddress deviceAddress){
  float tempC = sensors.getTempC(deviceAddress);
  if(tempC == DEVICE_DISCONNECTED_C) 
  {
    Serial.println("Error: Could not read temperature data");
    return;
  }
  Serial.print("Temp C: ");
  Serial.print(tempC);
}


int getTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  if(tempC == DEVICE_DISCONNECTED_C) 
  {
    Serial.println("Error: Could not read temperature data");
    return;
  }
//  Serial.print("Temp C: ");
//  Serial.print(tempC);
  return tempC;
}
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

void handleCommand(String command) {
  command.trim();
  String module = command.substring(0, 2);
  String action = command.substring(3);

  int pin;
  int temp=50;
  if (module == "T0" && action == "?") {
      sensors.requestTemperatures(); // Send the command to get temperatures
      if(sensors.getAddress(tempDeviceAddress, 3)){
        temp=getTemperature(tempDeviceAddress);
        Serial.println("T0-" + String(temp));
      }
    return;
  } else if (module == "T1" && action == "?") {
      sensors.requestTemperatures(); // Send the command to get temperatures
      if(sensors.getAddress(tempDeviceAddress, 2)){
        temp=getTemperature(tempDeviceAddress);
        Serial.println("T1-" + String(temp));
      }
    return;
  } else if (module == "T2" && action == "?") {
      sensors.requestTemperatures(); // Send the command to get temperatures
      if(sensors.getAddress(tempDeviceAddress, 1)){
        temp=getTemperature(tempDeviceAddress);
        Serial.println("T2-" + String(temp));
      }
    return;
  } else if (module == "T3" && action == "?") {
      sensors.requestTemperatures(); // Send the command to get temperatures
      if(sensors.getAddress(tempDeviceAddress, 0)){
        temp=getTemperature(tempDeviceAddress);
        Serial.println("T3-" + String(temp));
      }
    return;
  } else {
    Serial.println("Nieznany moduł: " + module);
    return;
  }

}
// function to print a device address

//////////////////////////////////////////////////// MAIN LOOP //////////////////////////////////////////////////// 

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }
}
