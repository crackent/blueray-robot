import socket
import sys
import tty
import termios

PUERTO = 1001
TIMEOUT_CONEXION = 5


def conectar(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_CONEXION)
        sock.connect((ip, PUERTO))
        return sock
    except socket.error:
        return None


def enviar_comando(sock, comando):
    try:
        sock.send(comando.encode())
        return True
    except socket.error:
        return False


def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def mostrar_ayuda():
    print("\n" + "=" * 40)
    print("     Control de Robot Mecanum Remoto")
    print("=" * 40)
    print("  w    - Adelante")
    print("  s    - Atras")
    print("  a    - Girar izquierda")
    print("  d    - Girar derecha")
    print("  q    - Lateral izquierda")
    print("  e    - Lateral derecha")
    print("  x    - Detener")
    print("  h    - Mostrar esta ayuda")
    print("  Esc  - Salir")
    print("=" * 40)


def main():
    print("===== Control de Robot Mecanum Remoto =====")

    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = input("Ingrese la IP de la ESP32: ").strip()

    if not ip:
        print("Error: La IP no puede estar vacia")
        return

    print(f"Conectando a {ip}:{PUERTO}...")
    sock = conectar(ip)

    if not sock:
        print("Error: No se pudo conectar a la ESP32")
        return

    print("Conexion exitosa!")
    mostrar_ayuda()
    print("\nPresiona las teclas para mover el robot...")

    try:
        while True:
            ch = get_char()

            if ch == "\x1b":
                print("\nSaliendo...")
                break
            elif ch == "w":
                if enviar_comando(sock, "w"):
                    print("Adelante")
            elif ch == "s":
                if enviar_comando(sock, "s"):
                    print("Atras")
            elif ch == "a":
                if enviar_comando(sock, "a"):
                    print("Girar izquierda")
            elif ch == "d":
                if enviar_comando(sock, "d"):
                    print("Girar derecha")
            elif ch == "q":
                if enviar_comando(sock, "q"):
                    print("Lateral izquierda")
            elif ch == "e":
                if enviar_comando(sock, "e"):
                    print("Lateral derecha")
            elif ch == "x":
                if enviar_comando(sock, "x"):
                    print("Detener")
            elif ch == "h":
                mostrar_ayuda()

    except KeyboardInterrupt:
        print("\nInterrumpido...")
    finally:
        enviar_comando(sock, "x")
        sock.close()
        print("Conexion cerrada")


if __name__ == "__main__":
    main()
