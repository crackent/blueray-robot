# Especificaciones del Programa Python - Cliente TCP para Control de Robot Mecanum

## 1. Descripción General
Programa en Python que actúa como cliente TCP para conectarse a una ESP32 y enviar comandos de movimiento a un robot con ruedas mecanum.

## 2. Requisitos del Sistema

### 2.1 Software
- Python 3.6 o superior
- No se requieren librerías externas (usa socket y módulos del sistema)

### 2.2 Sistema Operativo
- Compatible con Linux, macOS (Windows requiere adaptación para teclado)

## 3. Configuración de Conexión

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| Protocolo | TCP | Protocolo de transporte |
| Puerto | 1001 | Puerto del servidor ESP32 |
| IP | Variable | IP del ESP32 (pasada por argumento o solicitada) |

## 4. Flujo del Programa

### 4.1 Inicio
1. Mostrar mensaje de bienvenida
2. Leer IP de argumento o solicitar al usuario
3. Intentar conexión TCP al puerto 1001
4. Si la conexión falla, mostrar error y salir

### 4.2 Bucle Principal
1. Leer tecla presionada
2. Enviar comando correspondiente a la ESP32
3. Mostrar acción realizada
4. Repetir hasta presionar Escape

### 4.3 Cierre
1. Enviar comando de detención ('x')
2. Cerrar conexión TCP
3. Terminar programa

## 5. Controles del Teclado

| Tecla | Comando | Acción |
|-------|---------|--------|
| `w` | Adelante | Mover hacia adelante |
| `s` | Atrás | Mover hacia atrás |
| `a` | Girar izquierda | Rotar hacia la izquierda |
| `d` | Girar derecha | Rotar hacia la derecha |
| `q` | Lateral izquierda | Desplazarse lateralmente a la izquierda |
| `e` | Lateral derecha | Desplazarse lateralmente a la derecha |
| `x` | Detener | Detener todos los motores |
| `h` | Ayuda | Mostrar ayuda en pantalla |
| `Esc` | Salir | Cerrar conexión y terminar |

## 6. Diagrama de Controles

```
         q(w)    w(↑)    e(e)
         ╱       │       ╲
    lateral izq  │    lateral der
         ╲       │       ╱
          ───────┼───────
         ╱       │       ╲
    a(←)         │        d(→)
   girar izq     x        girar der
    (detener)    │
         ╲       │       ╱
          ───────┼───────
                 │
                s(↓)
              atrás
```

## 7. Comandos TCP

| Comando | Letra | Descripción |
|---------|-------|-------------|
| Adelante | `w` | Los 4 motores giran hacia adelante |
| Atrás | `s` | Los 4 motores giran hacia atrás |
| Girar izquierda | `a` | Motores izquierdos atrás, derechos adelante |
| Girar derecha | `d` | Motores izquierdos adelante, derechos atrás |
| Lateral izquierda | `q` | Movimiento lateral mecanum izquierda |
| Lateral derecha | `e` | Movimiento lateral mecanum derecha |
| Detener | `x` | Detiene todos los motores |

## 8. Estructura del Programa

### 8.1 Módulos Requeridos
```python
import socket
import sys
import tty
import termios
```

### 8.2 Funciones Principales

| Función | Descripción |
|---------|-------------|
| `main()` | Función principal del programa |
| `conectar(ip)` | Establece conexión TCP con la ESP32 |
| `enviar_comando(socket, comando)` | Envía un carácter por el socket |
| `get_char()` | Lee un carácter del teclado sin esperar Enter |
| `mostrar_ayuda()` | Muestra los controles disponibles |

## 9. Manejo de Errores

### 9.1 Errores de Conexión
- **Error**: No se puede conectar a la IP
- **Acción**: Mostrar mensaje de error y salir

### 9.2 Errores de Red
- **Error**: Conexión perdida durante operación
- **Acción**: Mostrar mensaje y cerrar programa

### 9.3 Interrupción
- **Ctrl+C**: Enviar comando de detención y cerrar conexión

## 10. Parámetros Configurables

```python
PUERTO = 1001
TIMEOUT_CONEXION = 5
```

## 11. Ejemplo de Ejecución

### 11.1 Con IP como argumento
```bash
python control_robot.py 192.168.1.100
```

### 11.2 Sin argumento (solicita IP)
```bash
python control_robot.py
```

### 11.3 Sesión Típica
```
===== Control de Robot Mecanum Remoto =====
Conectando a 192.168.1.100:1001...
Conexion exitosa!

========================================
     Control de Robot Mecanum Remoto
========================================
  w    - Adelante
  s    - Atras
  a    - Girar izquierda
  d    - Girar derecha
  q    - Lateral izquierda
  e    - Lateral derecha
  x    - Detener
  h    - Mostrar esta ayuda
  Esc  - Salir
========================================

Presiona las teclas para mover el robot...
Adelante
Girar izquierda
Detener

Saliendo...
Conexion cerrada
```

## 12. Archivos del Programa

| Archivo | Descripción |
|---------|-------------|
| `control_robot.py` | Control por teclado del robot mecanum |
| `control_led.py` | Control básico de LED (ejemplo original) |
| `control_led_gesto.py` | Control de LED por gestos de mano |
| `control_led_sonrisa.py` | Control de LED por detección de sonrisa |

## 13. Instrucciones de Uso

### 13.1 Ejecución
```bash
python control_robot.py [IP_ESP32]
```

### 13.2 Requisitos Previos
1. ESP32 WROOM ejecutando el programa esp32-directo.ino
2. Robot mecanum conectado y alimentado
3. PC y ESP32 en la misma red WiFi

### 13.3 Verificación
- Verificar que la IP del ESP32 sea correcta
- Comprobar que el servidor TCP está activo (monitor serie)

## 14. Notas Adicionales

### 14.1 Compatibilidad
- Python 3.x
- Linux/macOS (usa tty/termios para entrada de teclado)
- Para Windows, requiere adaptación usando `msvcrt` o `keyboard`

### 14.2 Seguridad
- Enviar comando 'x' al salir para detener el robot
- Siempre detener el robot antes de desconectar

### 14.3 Adaptación Windows
Para Windows, reemplazar `get_char()` con:
```python
import msvcrt

def get_char():
    if msvcrt.kbhit():
        return msvcrt.getch().decode()
    return None
```

## 15. Tabla de Comandos del Robot Mecanum

| Comando | Motor DI | Motor DD | Motor TI | Motor TD | Movimiento |
|---------|----------|----------|----------|----------|------------|
| w | + | + | + | + | Adelante |
| s | - | - | - | - | Atrás |
| a | - | + | - | + | Girar izquierda |
| d | + | - | + | - | Girar derecha |
| q | + | - | - | + | Lateral izquierda |
| e | - | + | + | - | Lateral derecha |
| x | 0 | 0 | 0 | 0 | Detener |

Leyenda: `+` adelante, `-` atrás, `0` detenido
