# /reconhecimento_facial_app/config.py

import os

# --- Caminhos Base ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BASE_DIR, "models")
DATA_PATH = os.path.join(BASE_DIR, "data")

# --- Arquivos de Modelo ---
PROTOTXT_PATH = os.path.join(MODELS_PATH, "deploy.prototxt.txt")
WEIGHTS_PATH = os.path.join(MODELS_PATH, "res10_300x300_ssd_iter_140000.caffemodel")
SHAPE_PREDICTOR_PATH = os.path.join(MODELS_PATH, "shape_predictor_68_face_landmarks.dat")
FACE_REC_MODEL_PATH = os.path.join(MODELS_PATH, "dlib_face_recognition_resnet_model_v1.dat")

# --- Arquivos de Dados e Segurança ---
ENCODINGS_PATH = os.path.join(DATA_PATH, "encodings.pkl")
ENCRYPTION_KEY_PATH = os.path.join(DATA_PATH, "secret.key")

# --- Arquivo de Log ---
LOG_FILE_PATH = os.path.join(DATA_PATH, "inference_log.txt")

# --- Parâmetros de Performance e Reconhecimento ---
RECOGNITION_TOLERANCE = 0.6
DETECTION_CONFIDENCE = 0.7
FPS_LIMIT = 30 # Aumentado, pois a lógica será mais leve

# --- NOVOS PARÂMETROS DE OTIMIZAÇÃO ---
# Fator de redimensionamento do frame para processamento. 0.5 = 50% do tamanho original.
# Valores menores (ex: 0.25) são mais rápidos, mas podem perder precisão em rostos pequenos.
RESIZE_SCALE = 0.5 

# Processar completamente apenas 1 a cada N frames. Aumentar este valor torna a aplicação mais fluida.
PROCESS_EVERY_N_FRAMES = 5

# Aviso de conformidade a ser exibido no início
COMPLIANCE_NOTICE = """
AVISO: Esta é uma aplicação de Prova de Conceito (PoC).
Os dados biométricos (imagens e encodings) são armazenados localmente.
O usuário é o único responsável pelo tratamento dos dados e pelo cumprimento
das leis de privacidade aplicáveis. Use com responsabilidade.
"""