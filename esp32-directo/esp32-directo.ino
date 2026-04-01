#include <WiFi.h>
#include "config.h"

#define TCP_PORT 1001
#define TCP_TIMEOUT 5000
#define VELOCIDAD_DEFAULT 200
#define PWM_FREQ 1000
#define PWM_RES 8

// Puente H 1 - Motores Delanteros
#define H1_IN1 19
#define H1_IN2 18
#define H1_ENA 5
#define H1_IN3 4
#define H1_IN4 2
#define H1_ENB 15

// Puente H 2 - Motores Traseros
#define H2_IN1 33
#define H2_IN2 25
#define H2_ENA 32
#define H2_IN3 26
#define H2_IN4 27
#define H2_ENB 14

WiFiServer server(TCP_PORT);
WiFiClient client;

void setup() {
    Serial.begin(115200);
    
    pinMode(H1_IN1, OUTPUT);
    pinMode(H1_IN2, OUTPUT);
    pinMode(H1_IN3, OUTPUT);
    pinMode(H1_IN4, OUTPUT);
    
    pinMode(H2_IN1, OUTPUT);
    pinMode(H2_IN2, OUTPUT);
    pinMode(H2_IN3, OUTPUT);
    pinMode(H2_IN4, OUTPUT);
    
    ledcAttach(H1_ENA, PWM_FREQ, PWM_RES);
    ledcAttach(H1_ENB, PWM_FREQ, PWM_RES);
    ledcAttach(H2_ENA, PWM_FREQ, PWM_RES);
    ledcAttach(H2_ENB, PWM_FREQ, PWM_RES);
    
    detener();
    
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
            
            switch (comando) {
                case 'w':
                    moverAdelante(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Adelante");
                    break;
                case 's':
                    moverAtras(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Atras");
                    break;
                case 'a':
                    girarIzquierda(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Girar izquierda");
                    break;
                case 'd':
                    girarDerecha(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Girar derecha");
                    break;
                case 'q':
                    lateralIzquierda(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Lateral izquierda");
                    break;
                case 'e':
                    lateralDerecha(VELOCIDAD_DEFAULT);
                    Serial.println("Movimiento: Lateral derecha");
                    break;
                case 'x':
                    detener();
                    Serial.println("Movimiento: Detener");
                    break;
            }
        }
        
        if (!client.connected()) {
            Serial.println("Cliente desconectado");
            client.stop();
        }
    }
}

void setMotor(int in1, int in2, int enPin, int velocidad) {
    if (velocidad > 0) {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        ledcWrite(enPin, velocidad);
    } else if (velocidad < 0) {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        ledcWrite(enPin, -velocidad);
    } else {
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        ledcWrite(enPin, 0);
    }
}

void moverAdelante(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, velocidad);
}

void moverAtras(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, -velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, -velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, -velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, -velocidad);
}

void girarDerecha(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, -velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, -velocidad);
}

void girarIzquierda(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, -velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, -velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, velocidad);
}

void lateralDerecha(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, -velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, -velocidad);
}

void lateralIzquierda(int velocidad) {
    setMotor(H1_IN1, H1_IN2, H1_ENA, velocidad);
    setMotor(H1_IN3, H1_IN4, H1_ENB, -velocidad);
    setMotor(H2_IN1, H2_IN2, H2_ENA, -velocidad);
    setMotor(H2_IN3, H2_IN4, H2_ENB, velocidad);
}

void detener() {
    setMotor(H1_IN1, H1_IN2, H1_ENA, 0);
    setMotor(H1_IN3, H1_IN4, H1_ENB, 0);
    setMotor(H2_IN1, H2_IN2, H2_ENA, 0);
    setMotor(H2_IN3, H2_IN4, H2_ENB, 0);
}
