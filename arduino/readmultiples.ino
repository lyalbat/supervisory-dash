const byte buffSize = 32;
char inputSeveral[buffSize];
byte maxChars = 12;
float inputFloat = 0.0;
char inputChar = 'X';
char inputCsvString[2];

int mockVar1 = 1;
int mockVar2 = 2;
int mockVar3 = 3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  readCSV();
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
  char * partOfString; 
    
  partOfString = strtok(inputSeveral,",");      
  strcpy(inputCsvString, partOfString); 
  partOfString = strtok(NULL, ","); 
  inputFloat = atof(partOfString); 
  if(inputCsvString[0] == 'r'){
    read();
  }
  else if(inputCsvString[0] == 'w'){
    write();
  }
 
}

void write(){
  Serial.println("you want to write a value");
  Serial.println(inputFloat);
}

void read(){
  //Serial.print("String -- ");
  //Serial.print(inputCsvString);
  //Serial.print("  Float -- ");
  Serial.println(inputFloat);
  Serial.println(mockVar1);
  Serial.println(mockVar2);
  Serial.println(mockVar3);
}