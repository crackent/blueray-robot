# Especificaciones del Programa Arduino - Control de LED por Dos Puertos Serie

## 1. Descripción General
Programa para Arduino Uno que controla un LED respondiendo a comandos recibidos por dos puertos serie: el hardware (pines 0/1) y un SoftwareSerial (pines 2/3) conectado a una ESP32.

## 2. Hardware Requerido
- Arduino Uno
- LED conectado al pin digital 13
- Dispositivos serie conectados a:
  - Puerto serie hardware: pines 0 (RX) y 1 (TX)
  - Puerto serie software: pines 2 (RX) y 3 (TX)

## 3. Configuración de Pines

| Pin | Función | Descripción |
|-----|---------|-------------|
| 0   | RX      | Recepción serie hardware |
| 1   | TX      | Transmisión serie hardware |
| 2   | RX      | Recepción serie software (ESP32) |
| 3   | TX      | Transmisión serie software (ESP32) |
| 13  | OUTPUT  | LED integrado de Arduino |

## 4. Comunicación Serie

### 4.1 Puerto Serie Hardware
- **Pines**: 0 (RX) y 1 (TX)
- **Velocidad**: 9600 bps
- **Uso**: Conexión por USB, depuración o dispositivo externo

### 4.2 Puerto Serie Software
- **Pines**: 2 (RX) y 3 (TX)
- **Velocidad**: 9600 bps
- **Biblioteca**: `SoftwareSerial`
- **Uso**: Comunicación con ESP32

## 5. Protocolo de Comandos

Ambos puertos serie responden al mismo protocolo:

| Comando | Letra | Acción |
|---------|-------|--------|
| Encender | `e` | Enciende el LED en el pin 13 (HIGH) |
| Apagar | `a` | Apaga el LED en el pin 13 (LOW) |

### 5.1 Comportamiento
1. El programa escucha ambos puertos serie simultáneamente
2. Al recibir un carácter válido por cualquiera de los dos puertos, ejecuta la acción correspondiente
3. Caracteres no reconocidos se ignoran

## 6. Estructura del Programa

### 6.1 Inicialización (`setup()`)
- Configurar pin 13 como OUTPUT, estado LOW (apagado)
- Iniciar puerto serie hardware a 9600 baudios
- Iniciar puerto serie software en pines 2/3 a 9600 baudios

### 6.2 Bucle Principal (`loop()`)
- Verificar datos en puerto serie hardware → procesar si hay
- Verificar datos en puerto serie software → procesar si hay
- Repetir

### 6.3 Función Auxiliar
```cpp
void procesar_comando(char comando);
```
Procesa un carácter recibido de cualquier puerto serie.

## 7. Consideraciones Técnicas

### 7.1 Librerías Necesarias
```cpp
#include <SoftwareSerial.h>
```

### 7.2 Velocidad de Baudios
- Ambos puertos a 9600 bps

### 7.3 Robustez
- Ignorar caracteres no válidos sin errores
- Funcionamiento continuo sin reinicios
- Sin delays ni bloqueos

## 8. Diagrama de Flujo

```
Inicio
  ↓
Configurar pin 13 como OUTPUT (LOW)
  ↓
Iniciar Serial (9600 baudios)
  ↓
Iniciar SoftwareSerial pines 2/3 (9600 baudios)
  ↓
┌──────────────────────────────────────┐
│  ¿Datos en Serial? ──SÍ──→ Procesar │
│  ¿Datos en SoftSerial? ──SÍ──→ Procesar │
└──────────────────────────────────────┘
  ↓
(Repetir bucle)
```

## 9. Diagrama de Conexión

```
┌─────────────────────┐         ┌─────────────────────┐
│      PC / USB       │         │      ESP32          │
│                     │         │                     │
│   TX ──────────────────── RX0 │                     │
│   RX ←────────────────── TX0 │      TX3 ──────────────── RX2
│                     │         │      RX2 ←─────────────── TX3
└─────────────────────┘         └─────────────────────┘
                                          │
                                     WiFi TCP 1001
                                          │
                                    Cliente TCP
                                         (PC)
         │                                     │
         └────────── Arduino Uno ──────────────┘
                    Pin 13 ── LED
```

## 10. Ejemplo de Uso

### 10.1 Por USB (serie hardware)
```
Enviar 'e' → LED se enciende
Enviar 'a' → LED se apaga
```

### 10.2 Por ESP32 (serie software)
```
Conectar por TCP a ESP32:1001
Enviar 'e' → LED se enciende
Enviar 'a' → LED se apaga
```

## 11. Parámetros Configurables

```cpp
#define LED_PIN 13
#define BAUD_RATE 9600
#define SERIAL1_RX 2
#define SERIAL1_TX 3
```
