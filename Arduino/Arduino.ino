#include <SPI.h>
#include <MFRC522.h>
#include "Adafruit_MCP23017.h"
#include <Arduino_JSON.h>

// Variables and declaration for RFID Reader
#define SS_PIN 10
MFRC522 mfrc522(SS_PIN);

// Mcp
Adafruit_MCP23017 mcp;

// Variables for receiving
const byte numChars = 500;
char receivedChars[numChars];
boolean newData = false;

void setup() {
  // Serial communication
  Serial.begin(115200);

  // Setting mcp to output (leds)
  mcp.begin();
  for (int i = 0; i <= 15; i++) {
    mcp.pinMode(i, OUTPUT);
  }

  // Init RFID reader
  SPI.begin();
  mfrc522.PCD_Init();

  // LDR init
  pinMode(A0, INPUT);
}

void loop() {

  // Serial communication handling
  getMessages();
  handleMessage();


  rfid();
  LDR();
}

void getMessages() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0';
      ndx = 0;
      newData = true;
    }
  }
}

void handleMessage() {
  if (newData == true) {
    JSONVar myObject = JSON.parse(receivedChars);
    
    if (JSON.typeof(myObject) == "undefined") {
      newData = false;
      return;
    }

    // Example for further use
    if (myObject.hasOwnProperty("led") && myObject.hasOwnProperty("value")) {
      mcp.digitalWrite(int(myObject["led"]), int(myObject["value"]));
    }
    
    newData = false;
  }
}

void rfid() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.print("UID tag :");
  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(content);
}

void LDR() {
  int sensorValue = analogRead(A0); // read the value from the sensor
  Serial.println(sensorValue); //prints the values coming from the sensor on the screen

  delay(1000);
}
