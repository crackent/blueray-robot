# Especificaciones del Programa ESP32 C3 SuperMini - Puente TCP/IP a Puerto Serie

## 1. Descripción General
Programa para ESP32 C3 SuperMini que actúa como puente entre una conexión TCP/IP y un puerto serie software, permitiendo controlar remotamente un LED en un Arduino Uno.

## 2. Hardware Requerido
- ESP32 C3 SuperMini
- Conexión WiFi a red local
- Conexión serie al Arduino Uno mediante:
  - Pin digital 5 (RX - recepción)
  - Pin digital 6 (TX - transmisión)

## 3. Configuración de Pines

| Pin | Función | Descripción |
|-----|---------|-------------|
| 5   | RX      | Recepción de datos del puerto serie software |
| 6   | TX      | Transmisión de datos del puerto serie software |
| 8   | OUTPUT  | LED integrado del ESP32 C3 SuperMini (opcional para depuración) |

## 4. Conexión TCP/IP

### 4.1 Parámetros de Red
- **Protocolo**: TCP
- **Puerto**: 1001
- **Modo**: Servidor TCP (escucha conexiones entrantes)

### 4.2 Configuración WiFi
- Modo: Station (conexión a punto de acceso existente)
- Requiere SSID y contraseña de la red WiFi
- SSID y contraseña configurables (ver config.h.example)

## 5. Comunicación Serie

### 5.1 Puerto Serie Software
- **Pines utilizados**: 5 (RX) y 6 (TX)
- **Velocidad de transmisión (baud rate)**: 115200 bps
- **Destino**: Arduino Uno (pines 2 y 3)

### 5.2 Puerto Serie Hardware
- **Velocidad**: 115200 bps (para depuración por USB)
- **Uso**: Monitor serie y mensajes de estado

## 6. Protocolo de Comunicación

### 6.1 Comandos TCP/IP → ESP32

| Comando | Letra | Acción ESP32 |
|---------|-------|--------------|
| Encender | `e` | Reenvía 'e' por puerto serie al Arduino |
| Apagar | `a` | Reenvía 'a' por puerto serie al Arduino |

### 6.2 Comandos ESP32 → Arduino Uno

| Letra Enviada | Acción en Arduino |
|---------------|-------------------|
| `e` | Enciende LED en pin 13 (HIGH) |
| `a` | Apaga LED en pin 13 (LOW) |

### 6.3 Flujo de Datos
```
Cliente TCP/IP → Puerto 1001 (ESP32) → Puerto Serie Software (ESP32) → Arduino Uno → LED
```

## 7. Estructura del Programa

### 7.1 Inicialización (`setup()`)
- Inicializar puerto serie hardware a 115200 baudios
- Inicializar puerto serie hardware 1 en pines 5 (RX) y 6 (TX) a 115200 baudios
- Conectar a red WiFi (usar credenciales predefinidas)
- Esperar conexión WiFi exitosa
- Iniciar servidor TCP en puerto 1001
- Imprimir dirección IP asignada por monitor serie

### 7.2 Bucle Principal (`loop()`)
- Verificar si hay cliente TCP conectado
- Si hay cliente:
  - Leer datos recibidos del cliente TCP
  - Si el dato es 'e' o 'a':
    - Enviar carácter por puerto serie software hacia Arduino
    - (Opcional) Confirmar envío por monitor serie
  - Si el cliente se desconecta, esperar nueva conexión
- Mantener conexión WiFi activa

## 8. Consideraciones Técnicas

### 8.1 Librerías Necesarias
```cpp
#include <WiFi.h>
#include <SoftwareSerial.h>
```

### 8.2 Velocidad de Baudios
- Puerto serie hardware 1: 115200 bps (comunicación con Arduino)
- Puerto serie hardware 0: 115200 bps (depuración por USB)

### 8.3 Puerto TCP
- Puerto: 1001 (configurable)
- Máximo de clientes simultáneos: 1

### 8.4 Timeout y Reconexión
- Timeout de cliente TCP: 5000 ms
- Reconexión automática a WiFi si se pierde conexión

### 8.5 Robustez
- Ignorar caracteres no válidos recibidos por TCP
- Manejar desconexiones de cliente gracefully
- Reiniciar servidor TCP si es necesario

## 9. Diagrama de Flujo

```
Inicio
  ↓
Configurar puerto serie hardware (115200 baudios)
  ↓
Configurar puerto serie hardware 1 pines 5/6 (115200 baudios)
  ↓
Conectar a WiFi
  ↓
¿Conexión WiFi exitosa? ──NO──→ Reintentar
         ↓ SÍ
Iniciar servidor TCP puerto 1001
  ↓
Imprimir IP asignada
  ↓
┌─────────────────────────────────────────┐
│  ¿Cliente TCP conectado?                │
│         ↓ SÍ                            │
│  ¿Hay datos del cliente?                │
│         ↓ SÍ                            │
│  Leer carácter                          │
│         ↓                               │
│  ¿Es 'e' o 'a'? ──SÍ──→ Enviar a Arduino│
│         ↓ NO                            │
│  Ignorar                                │
│         ↓                               │
│  ¿Cliente desconectado? ──SÍ──→ Esperar │
└─────────────────────────────────────────┘
         ↓
    (Repetir bucle)
```

## 10. Diagrama de Conexión ESP32 ↔ Arduino

```
┌─────────────────────┐         ┌─────────────────────┐
│   ESP32 C3          │         │   Arduino Uno       │
│   SuperMini         │         │                     │
│                     │         │                     │
│   GPIO 6 (TX) ────────────────── GPIO 2 (RX)       │
│                     │   Serie  │                     │
│   GPIO 5 (RX) ←────────────────── GPIO 3 (TX)      │
│                     │         │                     │
│   GND ──────────────────────────── GND              │
│                     │         │                     │
└─────────────────────┘         │   Pin 13 ── LED     │
                                │                     │
        ↑                       └─────────────────────┘
        │
   TCP/IP Puerto 1001
        │
┌───────┴───────────┐
│   Cliente TCP     │
│   (PC/Móvil)      │
└───────────────────┘
```

## 11. Parámetros Configurables

```cpp
// WiFi
const char* ssid = "NOMBRE_RED";
const char* password = "CONTRASEÑA";

// TCP Server
const int tcpPort = 1001;

// Serial Hardware 1
const int rxPin = 5;
const int txPin = 6;
const int baudRate = 115200;
```

## 12. Ejemplo de Uso

1. Cargar programa en ESP32 C3 SuperMini
2. Abrir monitor serie (115200 baudios)
3. Esperar conexión WiFi y ver IP asignada (ej: 192.168.1.100)
4. Desde un cliente TCP (telnet, netcat, aplicación):
   ```
   Conectar a 192.168.1.100:1001
   Enviar 'e' → LED Arduino se enciende
   Enviar 'a' → LED Arduino se apaga
   ```

## 13. Ejemplos de Conexión TCP

### 13.1 Usando Telnet
```bash
telnet 192.168.1.100 1001
```

### 13.2 Usando Netcat
```bash
nc 192.168.1.100 1001
```

### 13.3 Usando Python
```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.100", 1001))
s.send(b'e')  # Encender LED
s.send(b'a')  # Apagar LED
s.close()
```

## 14. Notas Adicionales

### 14.1 ESP32 C3 SuperMini
- Voltaje de operación: 3.3V
- Conexión GND común obligatoria entre ESP32 y Arduino
- El ESP32 C3 tiene soporte nativo para WiFi

### 14.2 Seguridad
- Este programa no implementa autenticación
- Se recomienda usar solo en redes locales confiables
- Para producción, considerar añadir autenticación básica

### 14.3 Compatibilidad
- Puerto serie hardware (HardwareSerial 1) compatible con Arduino Uno
- El ESP32 C3 usa HardwareSerial(1) en pines GPIO 5/6

## 15. Mensajes de Estado por Monitor Serie

| Mensaje | Descripción |
|---------|-------------|
| `Conectando a WiFi...` | Intentando conectar a la red |
| `WiFi conectado` | Conexión exitosa |
| `IP: x.x.x.x` | Dirección IP asignada |
| `Servidor TCP iniciado en puerto 1001` | Servidor listo |
| `Cliente conectado` | Nuevo cliente TCP |
| `Enviado: e` | Letra 'e' enviada al Arduino |
| `Enviado: a` | Letra 'a' enviada al Arduino |
| `Cliente desconectado` | Cliente TCP cerró conexión |
