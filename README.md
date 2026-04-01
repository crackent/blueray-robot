# BlueRay Robot

Sistema de control remoto de robot mecanum y LED mediante TCP/IP.

## Arquitectura

### Opción 1: Control Directo de Robot Mecanum
```
PC (Python) --TCP/IP--> ESP32 WROOM --> 4 Motores DC (Ruedas Mecanum)
```

### Opción 2: Control de LED vía Puente Serie
```
PC (Python) --TCP/IP--> ESP32 C3 --Serie--> Arduino Uno --> LED
```

## Componentes

### `esp32-directo/` - Control Directo Robot Mecanum (ESP32 WROOM)
Controla directamente 4 motores DC mediante 2 puentes H para robot con ruedas mecanum.

| Componente | Pines |
|------------|-------|
| Puente H 1 (Delanteros) | D19, D18, D5 (IZQ) / D4, D2, D15 (DER) |
| Puente H 2 (Traseros) | D33, D25, D32 (IZQ) / D26, D27, D14 (DER) |

**Comandos TCP**: `w`(adelante), `s`(atrás), `a`(girar izq), `d`(girar der), `q`(lateral izq), `e`(lateral der), `x`(detener)

### `esp32/` - Puente TCP/Serie (ESP32 C3 SuperMini)
Actúa como puente TCP/IP a puerto serie para controlar un Arduino.

| Parámetro | Valor |
|-----------|-------|
| Puerto TCP | 1001 |
| Serie RX/TX | GPIO 5/6 @ 9600 baud |

**Comandos TCP**: `e`(encender LED), `a`(apagar LED)

### `arduino/` - Control LED (Arduino Uno)
Controla LED mediante comandos serie recibidos por SoftwareSerial.

| Pin | Función |
|-----|---------|
| 2 | RX (Serie) |
| 3 | TX (Serie) |
| 13 | LED |

### `pc/` - Clientes TCP (Python)
| Archivo | Descripción |
|---------|-------------|
| `control_robot.py` | Control por teclado del robot mecanum |
| `control_led.py` | Control básico de LED |
| `control_led_gesto.py` | Control de LED por gestos de mano |
| `control_led_sonrisa.py` | Control de LED por detección de sonrisa |

## Conexiones

### Robot Mecanum (ESP32 WROOM)
```
ESP32 WROOM
├── Puente H 1 (Motores Delanteros)
│   ├── D19, D18, D5  → Motor Delantero Izquierdo
│   └── D4, D2, D15   → Motor Delantero Derecho
└── Puente H 2 (Motores Traseros)
    ├── D33, D25, D32 → Motor Trasero Izquierdo
    └── D26, D27, D14 → Motor Trasero Derecho
```

### LED vía Puente (ESP32 C3 + Arduino)
| ESP32 C3 | Arduino |
|----------|---------|
| GPIO 6 (TX) | Pin 2 (RX) |
| GPIO 5 (RX) | Pin 3 (TX) |
| GND | GND |

## Uso

### Robot Mecanum
```bash
# 1. Configurar WiFi en esp32-directo/config.h (copiar de config.h.example)
# 2. Subir a ESP32 WROOM
arduino-cli compile --fqbn esp32:esp32:esp32 esp32-directo/esp32-directo.ino
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 esp32-directo/esp32-directo.ino

# 3. Ejecutar cliente en PC
python pc/control_robot.py 192.168.1.100
```

### LED vía Puente
```bash
# 1. Subir programa a Arduino Uno
# 2. Subir programa a ESP32 C3 (configurar WiFi primero)
# 3. Ejecutar cliente
python pc/control_led.py 192.168.1.100
```

## Controles del Robot Mecanum

```
     q         w         e
  lateral izq  │    lateral der
     a         x         d
  girar izq  detener  girar der
              s
            atrás
```

| Tecla | Acción |
|-------|--------|
| `w` | Adelante |
| `s` | Atrás |
| `a` | Girar izquierda |
| `d` | Girar derecha |
| `q` | Lateral izquierda |
| `e` | Lateral derecha |
| `x` | Detener |
| `Esc` | Salir |

## Configuración

Cada carpeta `esp32-directo/` y `esp32/` contiene un archivo `config.h.example`. Copiarlo a `config.h` y configurar:

```cpp
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_PASSWORD";
```

## Licencia

MIT
