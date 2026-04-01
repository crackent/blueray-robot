import socket

PUERTO = 1001
TIMEOUT_CONEXION = 5
BUFFER_SIZE = 1024

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

def mostrar_menu(ip):
    print("\n===== Control de LED Remoto =====")
    print(f"IP conectada: {ip}:{PUERTO}")
    print("=" * 32)
    print("1. Encender LED (e)")
    print("2. Apagar LED (a)")
    print("3. Salir")

def cerrar_conexion(sock):
    try:
        sock.close()
    except:
        pass

def main():
    print("===== Control de LED Remoto =====")
    
    while True:
        ip = input("Ingrese la IP de la ESP32: ").strip()
        
        if not ip:
            print("Error: La IP no puede estar vacía")
            continue
        
        print(f"Conectando a {ip}:{PUERTO}...")
        sock = conectar(ip)
        
        if sock:
            print("¡Conexión exitosa!")
            break
        else:
            print("Error: No se pudo conectar a la ESP32")
            print("Verifique que la IP sea correcta y la ESP32 esté encendida")
            reintentar = input("¿Desea reintentar? (s/n): ").strip().lower()
            if reintentar != 's':
                print("Saliendo...")
                return
    
    try:
        while True:
            mostrar_menu(ip)
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                if enviar_comando(sock, 'e'):
                    print("Comando 'e' enviado correctamente")
                    print("LED encendido")
                else:
                    print("Error al enviar comando")
            elif opcion == "2":
                if enviar_comando(sock, 'a'):
                    print("Comando 'a' enviado correctamente")
                    print("LED apagado")
                else:
                    print("Error al enviar comando")
            elif opcion == "3":
                print("Cerrando conexión...")
                cerrar_conexion(sock)
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida")
    
    except KeyboardInterrupt:
        print("\nCerrando conexión...")
        cerrar_conexion(sock)
        print("¡Hasta luego!")
    except Exception as e:
        print(f"Error inesperado: {e}")
        cerrar_conexion(sock)

if __name__ == "__main__":
    main()
