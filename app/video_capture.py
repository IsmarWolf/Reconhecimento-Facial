# /reconhecimento_facial_app/app/video_capture.py

import cv2
from typing import List

def list_available_cameras() -> List[int]:
    """
    Verifica e lista os índices das câmeras disponíveis.
    """
    available_cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            break
        available_cameras.append(index)
        cap.release()
        index += 1
    return available_cameras

class VideoCapture:
    def __init__(self, source: int = 0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise IOError(f"Não foi possível abrir a câmera {source}")
        
        self.source = source
        print(f"[INFO] Câmera {source} iniciada.")

    def read_frame(self):
        """
        Lê um quadro da câmera.
        Retorna um booleano (sucesso) e o quadro da imagem.
        """
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """
        Libera o recurso da câmera.
        """
        self.cap.release()
        print(f"[INFO] Câmera {self.source} liberada.")