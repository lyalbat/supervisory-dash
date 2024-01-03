#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress insideThermometer;

void setup(void)
{
  Serial.begin(9600);
  sensors.begin();
  sensors.setResolution(insideThermometer, 9);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  if(tempC == DEVICE_DISCONNECTED_C) 
  {
    Serial.println("Error: Could not read temperature data");
    return;
  }
  float tempF = DallasTemperature::toFahrenheit(tempC);
  Serial.print("Temp C: ");
  Serial.print(tempC);
  Serial.print(" Temp F: ");
  Serial.println(tempF); // Converts tempC to Fahrenheit
}

void loop(void)
{ 
  sensors.requestTemperatures(); 
  printTemperature(insideThermometer);
}
