#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(10, 9); // RX, TX
int Data; // the data received
 
void setup() {
  Bluetooth.begin(9600);
  Serial.begin(9600);
  Serial.println("Waiting for command...");
  Bluetooth.println("Send 1 to turn on the LED. Send 0 to turn Off");
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
}
 
void loop() {
  if (Bluetooth.available()){ //wait for data received
    Data=Bluetooth.read();
    if(Data=='1'){  
      Serial.println("GOING FORWARD");
      Bluetooth.println("GOING FORWARD");
       digitalWrite(2,HIGH);
       digitalWrite(3,LOW);
       digitalWrite(5,HIGH);
       digitalWrite(4,LOW); 
    }
    else if(Data=='0'){
       Serial.println("STOPPING");
       Bluetooth.println("STOPPING");
       digitalWrite(2,LOW);
       digitalWrite(3,LOW);
       digitalWrite(5,LOW);
       digitalWrite(4,LOW);
       
    }
    else if(Data=='2'){  
      Serial.println("GOING BACK");
      Bluetooth.println("GOING BACK");
      digitalWrite(3,HIGH);
      digitalWrite(2,LOW);
      digitalWrite(4,HIGH);
      digitalWrite(5,LOW); 
    }
    else if(Data=='3'){
       Serial.println("TURNING RIGHT");
       Bluetooth.println("TURNING RIGHT");
       digitalWrite(2,HIGH);
       digitalWrite(3,LOW);
      digitalWrite(4,LOW);
      digitalWrite(5,LOW);
    }
    else if(Data=='4'){
       Serial.println("TURNING LEFT");
       Bluetooth.println("TURNING LEFT");
       digitalWrite(3,LOW);
       digitalWrite(2,LOW);
       digitalWrite(5,HIGH);
       digitalWrite(4,LOW);
    }
     else if(Data=='5'){
       Serial.println("TURNING 360");
       Bluetooth.println("TURNING 360");
       digitalWrite(3,HIGH);
       digitalWrite(2,LOW);
       digitalWrite(5,HIGH);
       digitalWrite(4,LOW); 
    }
    else{;}
  }
delay(100);
}