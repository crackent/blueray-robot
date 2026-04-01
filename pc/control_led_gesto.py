import socket
import cv2
import mediapipe as mp
import sys

PUERTO = 1001
TIMEOUT_CONEXION = 5
MODEL_PATH = "hand_landmarker.task"

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

def dedo_indice_extendido(landmarks):
    punta_indice = landmarks[8]
    base_indice = landmarks[5]
    return punta_indice.y < base_indice.y

def main():
    print("===== Control de LED por Gesto =====")
    
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
    print("Usa tu dedo indice: EXTENDIDO = encender, ENCOGIDO = apagar")
    print("Presiona 'q' para salir")
    
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
    
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=1
    )
    
    landmarker = HandLandmarker.create_from_options(options)
    
    cap = cv2.VideoCapture(0)
    estado_anterior = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        results = landmarker.detect(mp_image)
        
        estado_actual = None
        
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                h, w, _ = frame.shape
                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                
                for connection in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:
                    start = hand_landmarks[connection.start]
                    end = hand_landmarks[connection.end]
                    cv2.line(frame, 
                             (int(start.x * w), int(start.y * h)),
                             (int(end.x * w), int(end.y * h)),
                             (0, 255, 0), 2)
                
                extendido = dedo_indice_extendido(hand_landmarks)
                estado_actual = "extendido" if extendido else "encogido"
                
                if estado_actual != estado_anterior:
                    if extendido:
                        if enviar_comando(sock, 'e'):
                            print("LED ENCENDIDO (dedo extendido)")
                    else:
                        if enviar_comando(sock, 'a'):
                            print("LED APAGADO (dedo encogido)")
                    estado_anterior = estado_actual
        
        color = (0, 255, 0) if estado_actual == "extendido" else (0, 0, 255)
        cv2.putText(frame, f"Indice: {estado_actual or 'No detectado'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("Control LED por Gesto", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
    print("Conexion cerrada")

if __name__ == "__main__":
    main()
