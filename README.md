# BlueRay Robot

Sistema de control remoto de LED mediante TCP/IP.

## Arquitectura

```
PC (Python) --TCP/IP--> ESP32 --Serie--> Arduino Uno --> LED
```

## Componentes

### Arduino (`arduino/`)
Controla el LED mediante comandos serie recibidos por pines 2 (RX) y 3 (TX).
- **Comandos**: `e` (encender), `a` (apagar)
- **LED**: Pin 13

### ESP32 (`esp32/`)
Actúa como puente TCP/IP a puerto serie.
- **WiFi**: Se conecta a red local
- **Puerto TCP**: 1001
- **Serie**: Pines 5 (RX), 6 (TX) a 9600 baudios

### PC (`pc/`)
Cliente TCP en Python para enviar comandos.
- Sin dependencias externas (usa `socket`)
- Menú interactivo

## Conexiones

| ESP32 | Arduino |
|-------|---------|
| GPIO 6 (TX) | Pin 2 (RX) |
| GPIO 5 (RX) | Pin 3 (TX) |
| GND | GND |

## Uso

1. Cargar `arduino/control_led.ino` en Arduino Uno
2. Configurar WiFi en `esp32/puente_tcp_serie.ino` y cargar en ESP32
3. Ejecutar `python pc/control_led.py` e ingresar IP de la ESP32

## Licencia

MIT
