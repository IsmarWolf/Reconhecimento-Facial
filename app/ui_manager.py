# /reconhecimento_facial_app/app/ui_manager.py

import cv2
import numpy as np
from typing import List, Tuple

def draw_results(frame: np.ndarray, boxes: List[Tuple[int, int, int, int]], names: List[str]):
    """
    Desenha as caixas delimitadoras e os nomes no quadro.
    """
    for ((startX, startY, endX, endY), name) in zip(boxes, names):
        # Define a cor baseada no resultado
        color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
        
        # Desenha o retângulo ao redor do rosto
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        
        # Desenha um fundo para o texto
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(frame, name, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

def draw_performance_metrics(frame: np.ndarray, fps: float):
    """
    Desenha o contador de FPS na tela.
    """
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

def display_instructions(frame: np.ndarray):
    """
    Exibe as instruções de uso na tela.
    """
    instructions = [
        "Pressione 'c' para cadastrar um rosto 'Desconhecido'",
        "Pressione 'q' para sair"
    ]
    y_offset = frame.shape[0] - 50
    
    for i, line in enumerate(instructions):
        cv2.putText(frame, line, (10, y_offset + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)