//https://console.firebase.google.com/u/0/project/led-blink-wifi/database/led-blink-wifi-default-rtdb/data

#include <ESP8266WiFi.h>
#include "FirebaseESP8266.h"
//#include <Servo.h>
 
int sensor = 14;              // the pin that the sensor is atteched to
int state = LOW;             // by default, no motion detected
int val;  

//#define WIFI_SSID "Galaxy M116379"
//#define WIFI_PASSWORD "kvow3925"

#define WIFI_SSID "Vicky"
#define WIFI_PASSWORD "oyevicks"

#define FIREBASE_HOST "led-blink-wifi-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "VvFhb5Ij53hPmECwjzf3lxmtXXUA7a0SqW34CNSa"

FirebaseData firebaseData;

void setup() {
//  Servo1.attach(servoPin); 
  
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  //Set database read timeout to 1 minute (max 15 minutes)
  Firebase.setReadTimeout(firebaseData, 1000 * 60);

  pinMode(sensor, INPUT);
}

void loop() {

 val = digitalRead(sensor);   // read sensor value
  if (val == HIGH) {           // check if the sensor is HIGH

    if (Firebase.pushInt(firebaseData,"/led1",1))
    {
      Serial.println("1");
    }
  } 
  
  else {
 if (Firebase.pushInt(firebaseData,"/led1",0))
    {  
      Serial.println("0");
    }
  
  }
     
    delay(200);
}
