# /reconhecimento_facial_app/main.py

import cv2
import time
import face_recognition
import numpy as np
import logging
from datetime import datetime

# Importa as configurações e os módulos da aplicação
import config
from app.database_manager import DatabaseManager
from app.video_capture import VideoCapture, list_available_cameras
from app.face_detector import FaceDetector
from app.face_recognizer import FaceRecognizer
from app.ui_manager import draw_results, draw_performance_metrics, display_instructions

# --- Configuração do Logging Técnico ---
logging.basicConfig(
    filename=config.LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def select_camera() -> int:
    """
    Permite ao usuário selecionar uma câmera a partir da lista de câmeras disponíveis.
    """
    cameras = list_available_cameras()
    if not cameras:
        print("[ERRO] Nenhuma câmera encontrada. Encerrando.")
        exit()
    
    print("Câmeras disponíveis:")
    for cam_index in cameras:
        print(f"  [{cam_index}] Câmera {cam_index}")
        
    while True:
        try:
            choice = int(input("Digite o número da câmera que deseja usar: "))
            if choice in cameras:
                return choice
            else:
                print("Seleção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def main():
    """
    Função principal que executa a aplicação de reconhecimento facial otimizada.
    """
    print(config.COMPLIANCE_NOTICE)
    
    # --- Inicialização dos Módulos ---
    db_manager = DatabaseManager(config.ENCODINGS_PATH, config.ENCRYPTION_KEY_PATH)
    data = db_manager.load_encodings()
    
    camera_index = select_camera()
    video_capture = VideoCapture(source=camera_index)
    
    face_detector = FaceDetector(config.PROTOTXT_PATH, config.WEIGHTS_PATH, config.DETECTION_CONFIDENCE)
    face_recognizer = FaceRecognizer()
    
    # --- Variáveis para a Lógica de Otimização ---
    last_frame_time = 0
    frame_count = 0
    # Armazenam os últimos resultados conhecidos para serem exibidos nos frames não processados
    last_known_boxes = []
    last_known_names = []
    last_known_encodings = []
    
    print("\n[INFO] Aplicação otimizada iniciada. Pressione 'q' na janela de vídeo para sair.")
    
    # --- Loop Principal ---
    while True:
        # Limitação de FPS (opcional, mas bom para estabilidade)
        if config.FPS_LIMIT > 0:
            time.sleep(1.0 / config.FPS_LIMIT)
        
        current_time = time.time()
        fps = 1 / (current_time - last_frame_time) if (current_time - last_frame_time) > 0 else 0
        last_frame_time = current_time
        
        ret, frame = video_capture.read_frame()
        if not ret:
            print("[ERRO] Não foi possível capturar o quadro. Encerrando.")
            break
        
        frame_count += 1
        
        # --- LÓGICA DE OTIMIZAÇÃO ---
        # Processa completamente apenas a cada N frames
        if frame_count % config.PROCESS_EVERY_N_FRAMES == 0:
            # 1. Reduz o tamanho do frame para acelerar a detecção
            small_frame = cv2.resize(frame, (0, 0), fx=config.RESIZE_SCALE, fy=config.RESIZE_SCALE)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # 2. Executa o pipeline de detecção e reconhecimento no frame PEQUENO
            boxes = face_detector.detect_faces(small_frame)
            encodings = face_recognizer.get_face_encodings(rgb_small_frame, boxes)
            
            names = []
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["known_encodings"], encoding, tolerance=config.RECOGNITION_TOLERANCE)
                name = "Desconhecido"
                face_distances = face_recognition.face_distance(data["known_encodings"], encoding)
                
                log_distance = "N/A"
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    log_distance = f"{face_distances[best_match_index]:.4f}"
                    if matches[best_match_index]:
                        name = data["known_names"][best_match_index]
                
                names.append(name)
                logging.info(f"camera_id={video_capture.source}, faces_detected={len(boxes)}, face_index={len(names)}, distance={log_distance}, decision='{name}'")
            
            # 3. Armazena os resultados para os próximos frames
            last_known_boxes = boxes
            last_known_names = names
            last_known_encodings = encodings
        
        # --- Renderização do Overlay (em TODOS os frames) ---
        # Redimensiona as caixas delimitadoras de volta para o tamanho original do frame
        display_boxes = []
        if last_known_boxes:
            scale = config.RESIZE_SCALE
            for (startX, startY, endX, endY) in last_known_boxes:
                display_boxes.append((int(startX / scale), int(startY / scale), int(endX / scale), int(endY / scale)))

        draw_results(frame, display_boxes, last_known_names)
        draw_performance_metrics(frame, fps)
        display_instructions(frame)
        
        cv2.imshow("Reconhecimento Facial Otimizado - Pressione 'q' para sair", frame)
        key = cv2.waitKey(1) & 0xFF

        # --- Interação do Usuário ---
        if key == ord("q"):
            break
        
        if key == ord("c"):
            if last_known_names.count("Desconhecido") == 1:
                idx = last_known_names.index("Desconhecido")
                new_encoding = last_known_encodings[idx]
                
                cv2.destroyAllWindows()
                new_name = input("Detectado um rosto desconhecido. Digite o nome para cadastro e pressione Enter: ")
                
                if new_name:
                    data["known_encodings"].append(new_encoding)
                    data["known_names"].append(new_name)
                    db_manager.save_encodings(data)
                    print(f"[INFO] Usuário '{new_name}' cadastrado com sucesso.")
                else:
                    print("[AVISO] Cadastro cancelado.")
            else:
                print("[AVISO] Para cadastrar, posicione apenas UM rosto 'Desconhecido' na câmera.")

    # --- Finalização ---
    video_capture.release()
    cv2.destroyAllWindows()
    print("[INFO] Aplicação encerrada.")

if __name__ == "__main__":
    main()