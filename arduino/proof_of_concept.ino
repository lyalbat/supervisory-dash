//Setup for led
int led = 12;

//Setup for serial manipulation
const byte buffSize = 32;
char inputSeveral[buffSize];
byte maxChars = 12;

float inputFloat = 0.0;
char inputChar = 'X';
char inputCsvString[2];

//Setup for sensor usage
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress insideThermometer;
float tempC = 0.0;
float tempF = 0.0;

//Mock variables

float mockVoltage = 1.0;
float mockCurrent = 2.0;
float mockFlowRate = 3.0;
float mockHydrogen = 4.0;

void setup() {
  Serial.begin(9600);
  sensors.begin();
  sensors.setResolution(insideThermometer, 9);
  pinMode(led,OUTPUT);
}

void loop() {
  readCSV();
  sensors.requestTemperatures();
  getTemperature(insideThermometer);
  serialResponse();
  delay(800);
}

void readCSV(){
  inputSeveral[0] = 0;
  maxChars = buffSize - 1;
  byte charCount = 0;
  byte ndx = 0;

  if(Serial.available() > 0){
    while (Serial.available() > 0) { 
        if (ndx > maxChars - 1) {
          ndx = maxChars;
        } 
        inputSeveral[ndx] = Serial.read();
        ndx ++;        
        charCount ++;
      }
      if (ndx > maxChars) { 
        ndx = maxChars;
      }
      inputSeveral[ndx] = 0; 
  }
}

void getTemperature(DeviceAddress deviceAddress)
{
  tempC = sensors.getTempC(deviceAddress);
  if(tempC == DEVICE_DISCONNECTED_C) 
  {
    Serial.println("Error: Could not read temperature data");
    return;
  }
  //Serial.println(tempC);
  //tempF = DallasTemperature::toFahrenheit(tempC);
}

void serialResponse(){
  char * partOfString;
  partOfString = strtok(inputSeveral,",");      
  
  strcpy(inputCsvString, partOfString); 
  partOfString = strtok(NULL, ","); 
  inputFloat = atof(partOfString); 
  
  if(inputCsvString[0] == 'r'){
    readAllData();
  }
  /*else if(inputCsvString[0] == 'h'){
    readHydrogen();
  }
  else if(inputCsvString[0] == 'f'){
    readFlowRate();
  }
  else if(inputCsvString[0] == 't'){
    getTemperature(insideThermometer); 
  }
  else if(inputCsvString[0] == 'v'){
    readVoltage();
  }
  else if(inputCsvString[0] == 'c'){
    readCurrent();
  }*/
  else if(inputCsvString[0] == 'w'){
    write();
  }
}

void write(){
  //Serial.println("you want to write a value");
  digitalWrite(led, HIGH);
  delay(400);
  digitalWrite(led, LOW);
  Serial.println(inputFloat);
}

void readAllData(){
  Serial.print(mockVoltage);
  Serial.print(",");
  Serial.print(mockCurrent);
  Serial.print(",");
  Serial.print(tempC);
  Serial.print(",");
  Serial.print(mockFlowRate);
  Serial.print(",");
  Serial.println(mockHydrogen);
}

/*
void readCurrent(){
  Serial.println(mockCurrent);
}

void readVoltage(){
 Serial.println(mockVoltage);
}

void readHydrogen(){
  Serial.print(mockHydrogen);
}

void readFlowRate(){
  Serial.println(mockFlowRate);
}*/