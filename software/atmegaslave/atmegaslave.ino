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
byte digital_reading=0,analog_reading[4];

void receiveData(int byteCount){
    while(Wire.available()){
      if(Wire.available()==3)  {
        completed_cmd=0;
        index=0;
      }
      cmd[index++] = Wire.read();
    }
}

void sendData(){
  if(cmd[0] == DIGITALREAD_CMD){
    Wire.write(digital_reading);
  }else if(cmd[0] == ANALOGREAD_CMD){
    Wire.write(analog_reading, 3);
  }
}

void setup(){
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop(){
	if(index==3 && completed_cmd == 0 ){

		if(cmd[0]==PINMODE_CMD){
		  pinMode(cmd[1],cmd[2]);
		}else if(cmd[0]==DIGITALREAD_CMD){
		  digital_reading=digitalRead(cmd[1]);
		}else if(cmd[0]==DIGITALWRITE_CMD){
		  digitalWrite(cmd[1],cmd[2]);
		}else if(cmd[0]==ANALOGREAD_CMD){
		  short sensor_value=analogRead(cmd[1]);
      analog_reading[0] = map(sensor_value, 0, 1023, 0, 255);
      // using map to send first byte as can not send and receive block data atm but need to to get granular
      // data back to the pi see https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=203286
		  analog_reading[1]=sensor_value/256;
		  analog_reading[2]=sensor_value%256;
		}else if(cmd[0]==ANALOGWRITE_CMD){
		  analogWrite(cmd[1],cmd[2]);
    }

    completed_cmd=1;
  }
}
