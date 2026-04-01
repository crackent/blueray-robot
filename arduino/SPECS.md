# Especificaciones del Programa Arduino - Control de LED por Puerto Serie Software

## 1. Descripción General
Programa para Arduino Uno que permite controlar un LED mediante comandos enviados por un puerto serie simulado en los pines digitales 2 y 3.

## 2. Hardware Requerido
- Arduino Uno
- LED conectado al pin digital 13
- Dispositivo externo capaz de enviar datos serie conectado a:
  - Pin digital 2 (RX - recepción)
  - Pin digital 3 (TX - transmisión)

## 3. Configuración de Pines

| Pin | Función | Descripción |
|-----|---------|-------------|
| 2   | RX      | Recepción de datos del puerto serie software |
| 3   | TX      | Transmisión de datos del puerto serie software |
| 13  | OUTPUT  | LED integrado de Arduino |

## 4. Comunicación Serie

### 4.1 Puerto Serie Software
- **Pines utilizados**: 2 (RX) y 3 (TX)
- **Velocidad de transmisión (baud rate)**: 9600 bps
- **Biblioteca requerida**: `SoftwareSerial`

### 4.2 Puerto Serie Hardware (opcional)
- **Velocidad**: 9600 bps
- **Uso**: Depuración y monitoreo

## 5. Protocolo de Comandos

### 5.1 Comandos Disponibles

| Comando | Letra | Acción |
|---------|-------|--------|
| Encender | `e` | Enciende el LED en el pin 13 (HIGH) |
| Apagar | `a` | Apaga el LED en el pin 13 (LOW) |

### 5.2 Comportamiento
1. El programa espera continuamente datos del puerto serie software
2. Cuando recibe un carácter:
   - Si es `'e'` → `digitalWrite(13, HIGH)`
   - Si es `'a'` → `digitalWrite(13, LOW)`
   - Cualquier otro carácter → se ignora (sin acción)

## 6. Estructura del Programa

### 6.1 Inicialización (`setup()`)
- Configurar pin 13 como OUTPUT
- Inicializar LED en estado LOW (apagado)
- Inicializar puerto serie software a 9600 baudios
- (Opcional) Inicializar puerto serie hardware para depuración

### 6.2 Bucle Principal (`loop()`)
- Verificar si hay datos disponibles en el puerto serie software
- Si hay datos:
  - Leer el carácter recibido
  - Comparar con comandos válidos
  - Ejecutar acción correspondiente

## 7. Consideraciones Técnicas

### 7.1 Librerías Necesarias
```cpp
#include <SoftwareSerial.h>
```

### 7.2 Velocidad de Baudios
- 9600 bps (estándar, compatible con la mayoría de dispositivos)

### 7.3 Tiempo de Respuesta
- El LED debe responder inmediatamente al recibir el comando
- No se requieren delays ni tiempos de espera

### 7.4 Robustez
- El programa debe ignorar caracteres no válidos sin causar errores
- El programa debe funcionar de forma continua sin reinicios

## 8. Diagrama de Flujo

```
Inicio
  ↓
Configurar pin 13 como OUTPUT
  ↓
Inicializar puerto serie software (9600 baudios)
  ↓
LED apagado (LOW)
  ↓
┌─────────────────────────────────┐
│  ¿Hay datos disponibles?        │
│         ↓ SÍ                    │
│  Leer carácter                  │
│         ↓                       │
│  ¿Es 'e'? ──SÍ──→ Encender LED  │
│         ↓ NO                    │
│  ¿Es 'a'? ──SÍ──→ Apagar LED    │
│         ↓ NO                    │
│  Ignorar carácter               │
└─────────────────────────────────┘
         ↓
    (Repetir bucle)
```

## 9. Ejemplo de Uso

1. Conectar dispositivo serie externo a pines 2 (RX) y 3 (TX)
2. Cargar el programa en Arduino Uno
3. Enviar letra `e` → LED se enciende
4. Enviar letra `a` → LED se apaga

## 10. Notas Adicionales

- El pin 13 tiene un LED integrado en la placa Arduino Uno, no requiere componentes externos adicionales
- Asegurar conexión a tierra (GND) común entre Arduino y el dispositivo externo
- Los pines 0 y 1 se dejan libres para el puerto serie hardware (USB)
