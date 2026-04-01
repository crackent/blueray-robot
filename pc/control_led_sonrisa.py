import socket
import cv2
import mediapipe as mp
import sys
import math

PUERTO = 1001
TIMEOUT_CONEXION = 5
MODEL_PATH = "face_landmarker.task"

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

def detectar_sonrisa(landmarks):
    esquina_izq = landmarks[61]
    esquina_der = landmarks[291]
    labio_sup = landmarks[13]
    labio_inf = landmarks[14]
    
    ancho_boca = math.sqrt((esquina_der.x - esquina_izq.x)**2 + (esquina_der.y - esquina_izq.y)**2)
    alto_boca = abs(labio_inf.y - labio_sup.y)
    
    if alto_boca == 0:
        return False
    
    ratio = ancho_boca / alto_boca
    
    esquinas_y = (esquina_izq.y + esquina_der.y) / 2
    centro_y = (labio_sup.y + labio_inf.y) / 2
    
    sonriendo = ratio > 3 and esquinas_y < centro_y
    return sonriendo

def main():
    print("===== Control de LED por Sonrisa =====")
    
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
    print("SONRISA = encender LED, SIN SONRISA = apagar LED")
    print("Presiona 'q' para salir")
    
    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
    
    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1
    )
    
    landmarker = FaceLandmarker.create_from_options(options)
    
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
        
        if results.face_landmarks:
            for face_landmarks in results.face_landmarks:
                h, w, _ = frame.shape
                
                for i, landmark in enumerate(face_landmarks):
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                
                sonriendo = detectar_sonrisa(face_landmarks)
                estado_actual = "sonriendo" if sonriendo else "serio"
                
                if estado_actual != estado_anterior:
                    if sonriendo:
                        if enviar_comando(sock, 'e'):
                            print("LED ENCENDIDO (sonrisa detectada)")
                    else:
                        if enviar_comando(sock, 'a'):
                            print("LED APAGADO (sin sonrisa)")
                    estado_anterior = estado_actual
        
        color = (0, 255, 0) if estado_actual == "sonriendo" else (0, 0, 255)
        cv2.putText(frame, f"Estado: {estado_actual or 'No detectado'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("Control LED por Sonrisa", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
    print("Conexion cerrada")

if __name__ == "__main__":
    main()
