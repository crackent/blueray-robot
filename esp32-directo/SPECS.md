# Especificaciones del Programa ESP32 WROOM - Control Directo de Robot Mecanum

## 1. Descripción General
Programa para ESP32 WROOM que controla directamente un robot con ruedas mecanum mediante 4 motores DC y 2 puentes H. Recibe comandos por TCP/IP desde un cliente remoto.

## 2. Hardware Requerido
- ESP32 WROOM
- 4 motores DC
- 2 puentes H (cada uno maneja 2 motores)
- 4 ruedas mecanum
- Conexión WiFi a red local

## 3. Configuración de Pines

### 3.1 Puente H 1 (Motores Delanteros)
| Pin ESP32 | Define | Función | Descripción |
|-----------|--------|---------|-------------|
| D19  | H1_IN1 | IN1 | Motor delantero izquierdo - dirección A |
| D18  | H1_IN2 | IN2 | Motor delantero izquierdo - dirección B |
| D5   | H1_ENA | ENA | Motor delantero izquierdo - PWM (velocidad) |
| D4   | H1_IN3 | IN3 | Motor delantero derecho - dirección A |
| D2   | H1_IN4 | IN4 | Motor delantero derecho - dirección B |
| D15  | H1_ENB | ENB | Motor delantero derecho - PWM (velocidad) |

### 3.2 Puente H 2 (Motores Traseros)
| Pin ESP32 | Define | Función | Descripción |
|-----------|--------|---------|-------------|
| D33  | H2_IN1 | IN1 | Motor trasero izquierdo - dirección A |
| D25  | H2_IN2 | IN2 | Motor trasero izquierdo - dirección B |
| D32  | H2_ENA | ENA | Motor trasero izquierdo - PWM (velocidad) |
| D26  | H2_IN3 | IN3 | Motor trasero derecho - dirección A |
| D27  | H2_IN4 | IN4 | Motor trasero derecho - dirección B |
| D14  | H2_ENB | ENB | Motor trasero derecho - PWM (velocidad) |

## 4. Conexión TCP/IP

### 4.1 Parámetros de Red
- **Protocolo**: TCP
- **Puerto**: 1001
- **Modo**: Servidor TCP (escucha conexiones entrantes)

### 4.2 Configuración WiFi
- Modo: Station (conexión a punto de acceso existente)
- Requiere SSID y contraseña de la red WiFi (configurar en config.h)

## 5. Movimientos del Robot Mecanum

### 5.1 Configuración de Motores
```
       ┌─────────── PUENTE H 1 ───────────┐
       │                                  │
    DELANTERO                         DELANTERO
    IZQUIERDO                         DERECHO
       [1]                              [2]
         \                            /
          \__________________________/
          |                          |
          |         ESP32            |
          |__________________________|
          /                          \
         /                            \
        [3]                            [4]
     TRASERO                          TRASERO
     IZQUIERDO                        DERECHO
       │                               │
       └─────────── PUENTE H 2 ────────┘
```

### 5.2 Tabla de Movimientos

| Movimiento | Motor DI | Motor DD | Motor TI | Motor TD |
|------------|----------|----------|----------|----------|
| Adelante | + | + | + | + |
| Atrás | - | - | - | - |
| Girar derecha | + | - | + | - |
| Girar izquierda | - | + | - | + |
| Lateral derecho | - | + | + | - |
| Lateral izquierdo | + | - | - | + |
| Detener | 0 | 0 | 0 | 0 |

Leyenda:
- `DI` = Delantero Izquierdo (Puente H 1)
- `DD` = Delantero Derecho (Puente H 1)
- `TI` = Trasero Izquierdo (Puente H 2)
- `TD` = Trasero Derecho (Puente H 2)
- `+` = Girar hacia adelante
- `-` = Girar hacia atrás
- `0` = Detenido

## 6. Protocolo de Comandos TCP/IP

| Comando | Letra | Acción |
|---------|-------|--------|
| Adelante | `w` | Mover hacia adelante |
| Atrás | `s` | Mover hacia atrás |
| Girar derecha | `d` | Rotar hacia la derecha |
| Girar izquierda | `a` | Rotar hacia la izquierda |
| Lateral derecho | `e` | Desplazarse lateralmente a la derecha |
| Lateral izquierdo | `q` | Desplazarse lateralmente a la izquierda |
| Detener | `x` | Detener todos los motores |

## 7. Estructura del Programa

### 7.1 Inicialización (`setup()`)
- Inicializar puerto serie hardware a 115200 baudios
- Configurar pines de los puentes H como OUTPUT
- Conectar a red WiFi
- Iniciar servidor TCP en puerto 1001
- Imprimir dirección IP asignada

### 7.2 Bucle Principal (`loop()`)
- Verificar conexión WiFi
- Esperar cliente TCP
- Leer comandos del cliente
- Ejecutar movimiento correspondiente
- Mantener conexión activa

## 8. Funciones de Control de Motores

### 8.1 Funciones Principales
```cpp
void moverAdelante(int velocidad);
void moverAtras(int velocidad);
void girarDerecha(int velocidad);
void girarIzquierda(int velocidad);
void lateralDerecha(int velocidad);
void lateralIzquierda(int velocidad);
void detener();
```

### 8.2 Funciones Auxiliares
```cpp
void setMotor(int in1, int in2, int en, int velocidad);
// velocidad > 0: adelante, velocidad < 0: atrás, velocidad = 0: detener
```

## 9. Consideraciones Técnicas

### 9.1 Librerías Nececesarias
```cpp
#include <WiFi.h>
```

### 9.2 PWM
- Frecuencia PWM: 1000 Hz (configurable)
- Resolución: 8 bits (0-255)
- Canales PWM: TODO (asignar uno por cada pin EN)

### 9.3 Timeout y Reconexión
- Timeout de cliente TCP: 5000 ms
- Reconexión automática a WiFi si se pierde conexión

## 10. Parámetros Configurables

```cpp
// WiFi (en config.h)
const char* ssid = "NOMBRE_RED";
const char* password = "CONTRASEÑA";

// TCP Server
const int tcpPort = 1001;

// Velocidad por defecto
const int velocidadDefault = 200; // 0-255
```

## 11. Diagrama de Conexión

```
                    ┌─────────────────────────────────┐
                    │           ESP32 WROOM           │
                    │                                 │
   Puente H 1 ◄─────┤ Pines GPIO (TODO)               ├─────► Puente H 2
   (Motores Del.)   │                                 │      (Motores Tras.)
                    │         WiFi                    │
                    │            │                    │
                    └────────────┼────────────────────┘
                                 │
                           TCP/IP Puerto 1001
                                 │
                    ┌────────────┴────────────┐
                    │      Cliente TCP        │
                    │      (PC/Móvil)         │
                    └─────────────────────────┘
```

## 12. Ejemplo de Uso

1. Cargar programa en ESP32 WROOM
2. Abrir monitor serie (115200 baudios)
3. Esperar conexión WiFi y ver IP asignada
4. Desde un cliente TCP:
   ```
   Conectar a 192.168.1.100:1001
   Enviar 'w' → Robot avanza
   Enviar 'a' → Robot gira izquierda
   Enviar 'x' → Robot se detiene
   ```

## 13. Pendientes de Completar

- [ ] Asignar pines GPIO para Puente H 1 (Motores Delanteros):
  - H1_IN1, H1_IN2, H1_ENA (Delantero Izquierdo)
  - H1_IN3, H1_IN4, H1_ENB (Delantero Derecho)
- [ ] Asignar pines GPIO para Puente H 2 (Motores Traseros):
  - H2_IN1, H2_IN2, H2_ENA (Trasero Izquierdo)
  - H2_IN3, H2_IN4, H2_ENB (Trasero Derecho)
- [ ] Asignar canales PWM
- [ ] Ajustar velocidad por defecto según motores
- [ ] Verificar lógica de dirección de motores según instalación física
