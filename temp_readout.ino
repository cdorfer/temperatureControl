//dorfer@phys.ethz.ch

#include <Adafruit_MAX31865.h>

Adafruit_MAX31865 ch1 = Adafruit_MAX31865(3, 4, 5, 6);
Adafruit_MAX31865 ch2 = Adafruit_MAX31865(11, 10, 9, 8);
#define RREF      4300.0
#define RNOMINAL  1000.0

int incomingByte = 0;

void setup() {
  Serial.begin(115200);
  ch1.begin(MAX31865_2WIRE);
  ch2.begin(MAX31865_2WIRE);
  while(!Serial){
    ;
  }
}



void loop() {
  char serialListener = '0';
  if (Serial.available()){    
    serialListener = Serial.read();
    double temp = 1000;
    switch(serialListener){
      case 'A':
        temp = readTemperature(1);
        Serial.println(temp);
        break;
      case 'B':
        temp = readTemperature(2);
        Serial.println(temp);
        break;
      default:
        break;      
    }
    serialListener = '0';

    //clear everything that might have come after the control char
    while(Serial.available() > 0){
      char t = Serial.read();
    }   
  } //end serial available
}



float readTemperature(int ch){

  if (ch==1){
      uint16_t rtd = ch1.readRTD();
      uint8_t fault = ch1.readFault(); 
      if (!fault){
        return ch1.temperature(RNOMINAL, RREF);
      }
      else{
        ch1.clearFault();
        return 999.0;
    } 
  }
  if (ch==2){
      uint16_t rtd = ch2.readRTD();
      uint8_t fault = ch2.readFault(); 
      if (!fault){
        return ch2.temperature(RNOMINAL, RREF);
      }
      else{
        ch2.clearFault();
        return 998.0;
    }    
  }
  else{
    return 997.0;
  }
}

