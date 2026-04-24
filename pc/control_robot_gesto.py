import socket
import cv2
import mediapipe as mp
import sys
import math

PUERTO = 1001
TIMEOUT_CONEXION = 5
MODEL_PATH = "hand_landmarker.task"
UMBRAL_DISTANCIA = 0.04

COMANDOS = {
    "Adelante": "w",
    "Atras": "s",
    "Girar izquierda": "a",
    "Girar derecha": "d",
    "Lateral izquierda": "q",
    "Lateral derecha": "e",
    "Detener": "x",
}

COLORES = {
    "Adelante": (0, 255, 0),
    "Atras": (0, 0, 255),
    "Girar izquierda": (255, 200, 0),
    "Girar derecha": (255, 200, 0),
    "Lateral izquierda": (255, 0, 200),
    "Lateral derecha": (255, 0, 200),
    "Detener": (128, 128, 128),
}


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


def obtener_direccion(landmarks):
    tip = landmarks[8]
    mcp = landmarks[5]
    wrist = landmarks[0]

    dx = tip.x - mcp.x
    dy = -(tip.y - mcp.y)
    distancia = math.sqrt(dx * dx + dy * dy)

    mano_cerrada = tip.y > mcp.y and abs(tip.x - mcp.x) < 0.03 and tip.y > wrist.y

    if mano_cerrada or distancia < UMBRAL_DISTANCIA:
        return "Detener", 0, 0

    angulo = math.degrees(math.atan2(dy, dx)) % 360

    if angulo < 22.5 or angulo >= 337.5:
        return "Girar derecha", dx, dy
    elif angulo < 67.5:
        return "Lateral derecha", dx, dy
    elif angulo < 112.5:
        return "Adelante", dx, dy
    elif angulo < 157.5:
        return "Lateral izquierda", dx, dy
    elif angulo < 202.5:
        return "Girar izquierda", dx, dy
    elif angulo < 247.5:
        return "Girar izquierda", dx, dy
    elif angulo < 292.5:
        return "Atras", dx, dy
    else:
        return "Girar derecha", dx, dy


def dibujar_flecha(frame, dx, dy, centro):
    longitud = 80
    fin = (int(centro[0] + dx * longitud * 3), int(centro[1] - dy * longitud * 3))
    cv2.arrowedLine(frame, centro, fin, (0, 255, 255), 3, tipLength=0.3)


def main():
    print("===== Control de Robot Mecanum por Gesto =====")

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
    print("Apunta con el dedo indice para dirigir el robot")
    print("Dedo encogido o sin mano = detener")
    print("Presiona 'q' para salir")

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=1,
    )

    landmarker = HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    comando_anterior = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        results = landmarker.detect(mp_image)

        movimiento = "Detener"
        dx, dy = 0, 0

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                h, w, _ = frame.shape

                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

                for connection in (
                    mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
                ):
                    start = hand_landmarks[connection.start]
                    end = hand_landmarks[connection.end]
                    cv2.line(
                        frame,
                        (int(start.x * w), int(start.y * h)),
                        (int(end.x * w), int(end.y * h)),
                        (0, 255, 0),
                        2,
                    )

                tip_x = int(hand_landmarks[8].x * w)
                tip_y = int(hand_landmarks[8].y * h)
                cv2.circle(frame, (tip_x, tip_y), 10, (0, 0, 255), 3)

                movimiento, dx, dy = obtener_direccion(hand_landmarks)

                if movimiento != "Detener":
                    mcp_x = int(hand_landmarks[5].x * w)
                    mcp_y = int(hand_landmarks[5].y * h)
                    dibujar_flecha(frame, dx, dy, (mcp_x, mcp_y))

        comando = COMANDOS[movimiento]

        if comando != comando_anterior:
            if enviar_comando(sock, comando):
                print(movimiento)
            comando_anterior = comando

        color = COLORES[movimiento]
        cv2.putText(
            frame,
            movimiento,
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )

        h, w_frame, _ = frame.shape
        cx, cy = w_frame // 2, h // 2
        cv2.line(frame, (cx - 30, cy), (cx + 30, cy), (100, 100, 100), 1)
        cv2.line(frame, (cx, cy - 30), (cx, cy + 30), (100, 100, 100), 1)

        cv2.imshow("Control Robot por Gesto", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    enviar_comando(sock, "x")
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
    print("Conexion cerrada")


if __name__ == "__main__":
    main()
