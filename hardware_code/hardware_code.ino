//int LABEL = 1;

//-----------------------------------------------------Declarações sensor hidrogênio-------------------------------------------------------

/************************Hardware Related Macros************************************/
#define         MQ_PIN                       (0)     //define which analog input channel you are going to use
#define         RL_VALUE                     (10)    //define the load resistance on the board, in kilo ohms
#define         RO_CLEAN_AIR_FACTOR          (9.21)  //RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                                     //which is derived from the chart in datasheet
 
/***********************Software Related Macros************************************/
#define         CALIBARAION_SAMPLE_TIMES     (50)    //define how many samples you are going to take in the calibration phase
#define         CALIBRATION_SAMPLE_INTERVAL  (500)   //define the time interal(in milisecond) between each samples in the
                                                     //cablibration phase
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interal(in milisecond) between each samples in 
                                                     //normal operation
 
/**********************Application Related Macros**********************************/
#define         GAS_H2                      (0)
 
/*****************************Globals***********************************************/
float           H2Curve[3]  =  {2.3, 0.93,-1.44};    //two points are taken from the curve in datasheet. 
                                                     //with these two points, a line is formed which is "approximately equivalent" 
                                                     //to the original curve. 
                                                     //data format:{ x, y, slope}; point1: (lg200, lg8.5), point2: (lg10000, lg0.03) 
 
float           Ro           =  10;                  //Ro is initialized to 10 kilo ohms

//Setup for serial manipulation
const byte buffSize = 32;
char inputSeveral[buffSize];
byte maxChars = 12;

float inputFloat = 0.0;
char inputChar = 'X';
char inputCsvString[2];

//-----------------------------------------------------Declarações sensores corrente e tensão-------------------------------------------------------


#define sensorACS712 A3      //Pino sensor de corrente
#define sensorTensaoDC A1    //Pino sensor de tensão
float R1 = 30000;
float R2 = 7500;
float sensibilidade = 0.066; //
unsigned int tempo = 0;
float temperatureByIndex;
float hydrogen;


//-----------------------------------------------------Declarações sensor de vazão-------------------------------------------------------

int contaPulso; 
float calculoVazao;
unsigned long tempo_inicio_abertura;
unsigned long tempo_total_abertura;
boolean torneira_aberta = false;
float tensao;
float corrente;

//-----------------------------------------------------Declarações sensor de temperatura-------------------------------------------------------

#include <OneWire.h>
#include <DallasTemperature.h>

// O fio de dados é conectado no pino digital 2 no Arduino
#define ONE_WIRE_BUS 7

// Prepara uma instância oneWire para comunicar com qualquer outro dispositivo oneWire
OneWire oneWire(ONE_WIRE_BUS);  

// Passa uma referência oneWire para a biblioteca DallasTemperature
DallasTemperature sensors(&oneWire);

//-------------------------------------------------------------------------------------------------------------------------------------------------------
 
void setup() {

  Serial.begin(9600);                                //UART setup, baudrate = 9600bps
  sensors.begin();  // Inicia a biblioteca

  //-----------SENSOR DE HIDROGÊNIO--------------

 // Serial.print("Calibrating...\n");                
  Ro = MQCalibration(MQ_PIN);                        //Calibrating the sensor. Please make sure the sensor is in clean air 
                                                     //when you perform the calibration                    

  //-----------SENSOR DE CORRENTE E TENSÃO--------------

  analogReference(DEFAULT); //Valor referencial
  Serial.begin(9600);
  pinMode(sensorTensaoDC, INPUT); //Declara pino sensor de tensao
  pinMode(sensorACS712, INPUT); //Declara pino sensor de corrente
  //tempo = millis();

  //-----------SENSOR DE VAZÃO-----------------

  pinMode(2, INPUT);
  attachInterrupt(0, incpulso, RISING);

  //------------------------------------------------------------------------

}
 
void loop() {   

  //-----------SENSOR DE TENSÃO E CORRENTE--------------

    unsigned int tensao_ADC = analogRead(sensorTensaoDC);
    unsigned int corrente_ADC = analogRead(sensorACS712);

    tensao = tensao_ADC*(5.0/1023.0);
    tensao /= (R2/(R1+R2));
    float corrente = (corrente_ADC*(5.0/1023.0))-2.5;
    corrente /= sensibilidade;

  //-----------SENSOR DE TEMPERATURA--------------

    // Manda comando para ler temperaturas
    sensors.requestTemperatures(); 

  //-----------SENSOR DE VAZÃO--------------

    contaPulso = 0;

    interrupts();                                   //Habilita interr.

    delay(1000);                  //Espera 1 segundo      

    noInterrupts();                                 //Desabilita a interru.
  

  //==========================================USER INPUT===============================================================

  temperatureByIndex = sensors.getTempCByIndex(0);

  //Serial.print("H2 Concentration: "); 
  hydrogen = MQGetGasPercentage(MQRead(MQ_PIN)/Ro,GAS_H2);


  if (contaPulso > 0){
      calculoVazao = contaPulso*(1.11/8); 
  }
  else{
    calculoVazao = -1;
  }

  readCSV();
  serialResponse();
  delay(1000);

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

void serialResponse(){
  char * partOfString;
  partOfString = strtok(inputSeveral,",");      
  
  strcpy(inputCsvString, partOfString); 
  partOfString = strtok(NULL, ","); 
  inputFloat = atof(partOfString); 
  
  if(inputCsvString[0] == 'r'){
    readAllData();
  }

  else if(inputCsvString[0] == 'w'){
    write();
  }
}

void write(){
  // Serial.println("you want to write a value");
  // if(inputFloat == 9){
    // digitalWrite(led, HIGH);
  // }
  // delay(400);
  // digitalWrite(led, LOW);
  // mockCurrent = inputFloat;
  Serial.println(inputFloat);
}

void readAllData(){
  Serial.print(tensao);
  Serial.print(",");
  Serial.print(corrente);
  Serial.print(",");
  Serial.print(temperatureByIndex);
  Serial.print(",");
  Serial.print(calculoVazao);
  Serial.print(",");
  Serial.print(hydrogen);
  Serial.print(",");
  Serial.println(contaPulso);
}



//-------------------------------Funções sensor de hidrogênio-----------------------------------------------------
 
/****************** MQResistanceCalculation ****************************************
Input:   raw_adc - raw value read from adc, which represents the voltage
Output:  the calculated sensor resistance
Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
         across the load resistor and its resistance, the resistance of the sensor
         could be derived.
************************************************************************************/ 
float MQResistanceCalculation(int raw_adc) {
  return ( ((float)RL_VALUE*(1023-raw_adc)/raw_adc));
}
 
/***************************** MQCalibration ****************************************
Input:   mq_pin - analog channel
Output:  Ro of the sensor
Remarks: This function assumes that the sensor is in clean air. It use  
         MQResistanceCalculation to calculates the sensor resistance in clean air 
         and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
         10, which differs slightly between different sensors.
************************************************************************************/ 
float MQCalibration(int mq_pin) {
  int i;
  float val=0;
 
  for (i=0;i<CALIBARAION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBARAION_SAMPLE_TIMES;                   //calculate the average value
 
  val = val/RO_CLEAN_AIR_FACTOR;                        //divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                        //according to the chart in the datasheet 
 
  return val; 
}
/*****************************  MQRead *********************************************
Input:   mq_pin - analog channel
Output:  Rs of the sensor
Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
         The Rs changes as the sensor is in the different consentration of the target
         gas. The sample times and the time interval between samples could be configured
         by changing the definition of the macros.
************************************************************************************/ 
float MQRead(int mq_pin) {
  int i;
  float rs=0;
 
  for (i=0;i<READ_SAMPLE_TIMES;i++) {
    rs += MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }
 
  rs = rs/READ_SAMPLE_TIMES;
 
  return rs;  
}
 
/*****************************  MQGetGasPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         gas_id      - target gas type
Output:  ppm of the target gas
Remarks: This function passes different curves to the MQGetPercentage function which 
         calculates the ppm (parts per million) of the target gas.
************************************************************************************/ 
int MQGetGasPercentage(float rs_ro_ratio, int gas_id) {
  if ( gas_id == GAS_H2) {
     return MQGetPercentage(rs_ro_ratio,H2Curve);
  }  
  return 0;
}
 
/*****************************  MQGetPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         pcurve      - pointer to the curve of the target gas
Output:  ppm of the target gas
Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
         of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
         logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
         value.
************************************************************************************/ 
int  MQGetPercentage(float rs_ro_ratio, float *pcurve) {
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}

//-------------------------------Funções sensor de vazao-----------------------------------------------------

void incpulso(){
  contaPulso++;
}
