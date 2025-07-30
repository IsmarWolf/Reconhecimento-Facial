# /reconhecimento_facial_app/app/face_detector.py

import cv2
import numpy as np
from typing import List, Tuple

class FaceDetector:
    def __init__(self, prototxt_path: str, weights_path: str, confidence_threshold: float = 0.7):
        """
        Inicializa o detector de faces carregando o modelo DNN do OpenCV.
        """
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, weights_path)
        self.confidence_threshold = confidence_threshold
        print("[INFO] Detector de faces (OpenCV DNN) carregado.")

    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detecta faces em um quadro de imagem.
        Retorna uma lista de caixas delimitadoras (startX, startY, endX, endY).
        """
        (h, w) = frame.shape[:2]
        # Cria um blob a partir da imagem e o passa pela rede
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        detections = self.net.forward()
        
        boxes = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.confidence_threshold:
                # Calcula as coordenadas (x, y) da caixa delimitadora
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                # Garante que a caixa delimitadora esteja dentro das dimensões do quadro
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                
                if endX > startX and endY > startY:
                    boxes.append((startX, startY, endX, endY))
                    
        return boxes