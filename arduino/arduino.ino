#define LED_PIN 13
#define BAUD_RATE 115200
#define SERIAL1_RX 2
#define SERIAL1_TX 3

#include <SoftwareSerial.h>
SoftwareSerial serialESP(SERIAL1_RX, SERIAL1_TX);

void procesar_comando(char comando) {
    if (comando == 'e') {
        digitalWrite(LED_PIN, HIGH);
    } else if (comando == 'a') {
        digitalWrite(LED_PIN, LOW);
    }
}

void setup() {
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);
    Serial.begin(BAUD_RATE);
    serialESP.begin(BAUD_RATE);
}

void loop() {
    if (Serial.available()) {
        procesar_comando(Serial.read());
    }
    if (serialESP.available()) {
        procesar_comando(serialESP.read());
    }
}
