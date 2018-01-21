/*
* i2c slave to run on atmega328 exposing command interface for pins
*
* http://www.digitalpolymath.co.uk/
* Tom Broughton
*/

#include <Wire.h>

#define SLAVE_ADDRESS 0x04

// comnmand constants
#define PINMODE_CMD 1
#define DIGITALREAD_CMD 2
#define DIGITALWRITE_CMD 3
#define ANALOGREAD_CMD 4
#define ANALOGWRITE_CMD 5

int cmd[4];
int index=0;
int completed_cmd=0;
byte digitalVal, analogVal[3];

void receiveData(int byteCount){
    while(Wire.available()){
      if(Wire.available()==4)  {
        completed_cmd=0;
        index=0;
      }
      cmd[index++] = Wire.read();
    }
}

void sendData(){
  if(cmd[0] == DIGITALREAD_CMD)
    Wire.write(digitalVal);
  else if(cmd[0] == ANALOGREAD_CMD)
    Wire.write(analogVal, 3);
}

void setup(){
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop(){
	if(index==4 && completed_cmd == 0 ){

		if(cmd[0]==PINMODE_CMD)
		  pinMode(cmd[1],cmd[2]);
		else if(cmd[0]==DIGITALREAD_CMD)
		  digitalVal=digitalRead(cmd[1]);
		else if(cmd[0]==DIGITALWRITE_CMD)
		  digitalWrite(cmd[1],cmd[2]);
		else if(cmd[0]==ANALOGREAD_CMD){
		  int reading=analogRead(cmd[1]);
      //# analog values may be greater than 255 and we are dealing with bytes
		  analogVal[1]=reading/256;
		  analogVal[2]=reading%256;
		}else if(cmd[0]==ANALOGWRITE_CMD)
		  analogWrite(cmd[1],cmd[2]);

    completed_cmd=1;
  }
}
