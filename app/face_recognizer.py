# /reconhecimento_facial_app/app/face_recognizer.py

import face_recognition
import numpy as np
from typing import List, Tuple

class FaceRecognizer:
    def __init__(self):
        """
        Esta classe usa a biblioteca face_recognition para extrair embeddings.
        A biblioteca gerencia o carregamento dos modelos Dlib internamente.
        """
        print("[INFO] Reconhecedor de faces (Dlib) pronto.")

    def get_face_encodings(self, frame_rgb: np.ndarray, boxes: List[Tuple[int, int, int, int]]) -> List[np.ndarray]:
        """
        Calcula os embeddings de 128 dimensões para cada face detectada.
        
        Args:
            frame_rgb: O quadro de vídeo em formato RGB.
            boxes: Uma lista de caixas delimitadoras no formato (top, right, bottom, left).
        
        Returns:
            Uma lista de vetores de embedding.
        """
        # A biblioteca face_recognition espera caixas no formato (top, right, bottom, left)
        # O detector do OpenCV fornece (startX, startY, endX, endY)
        # Convertendo: top=startY, right=endX, bottom=endY, left=startX
        dlib_boxes = [(y1, x2, y2, x1) for (x1, y1, x2, y2) in boxes]
        
        encodings = face_recognition.face_encodings(frame_rgb, dlib_boxes)
        return encodings