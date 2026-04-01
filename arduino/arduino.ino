#include <SoftwareSerial.h>

#define LED_PIN 13
#define RX_PIN 2
#define TX_PIN 3
#define BAUD_RATE 9600

SoftwareSerial mySerial(RX_PIN, TX_PIN);

void setup() {
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);
    
    mySerial.begin(BAUD_RATE);
}

void loop() {
    if (mySerial.available()) {
        char comando = mySerial.read();
        
        if (comando == 'e') {
            digitalWrite(LED_PIN, HIGH);
        } else if (comando == 'a') {
            digitalWrite(LED_PIN, LOW);
        }
    }
}
