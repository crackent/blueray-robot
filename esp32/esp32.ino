#include <WiFi.h>
#include "config.h"

#define RX_PIN 5
#define TX_PIN 6
#define BAUD_RATE 9600
#define TCP_PORT 1001
#define TCP_TIMEOUT 5000

HardwareSerial mySerial(1);
WiFiServer server(TCP_PORT);
WiFiClient client;

void setup() {
    Serial.begin(115200);
    mySerial.begin(BAUD_RATE, SERIAL_8N1, RX_PIN, TX_PIN);
    
    Serial.println("Conectando a WiFi...");
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println();
    Serial.println("WiFi conectado");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    
    server.begin();
    Serial.println("Servidor TCP iniciado en puerto 1001");
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi desconectado, reconectando...");
        WiFi.begin(ssid, password);
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
        }
        Serial.println("WiFi reconectado");
    }
    
    if (!client || !client.connected()) {
        client = server.available();
        if (client) {
            Serial.println("Cliente conectado");
            client.setTimeout(TCP_TIMEOUT);
        }
    }
    
    if (client && client.connected()) {
        if (client.available()) {
            char comando = client.read();
            
            if (comando == 'e') {
                mySerial.print('e');
                Serial.println("Enviado: e");
            } else if (comando == 'a') {
                mySerial.print('a');
                Serial.println("Enviado: a");
            }
        }
        
        if (!client.connected()) {
            Serial.println("Cliente desconectado");
            client.stop();
        }
    }
}
