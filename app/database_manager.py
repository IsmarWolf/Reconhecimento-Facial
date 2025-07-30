# /reconhecimento_facial_app/app/database_manager.py

import pickle
import os
from cryptography.fernet import Fernet
from typing import Dict, Any, Optional

# Gera uma chave de criptografia e a salva em um arquivo.
# Só executa se a chave não existir.
def generate_and_save_key(key_path: str):
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)

# Carrega a chave de criptografia do arquivo.
def load_key(key_path: str) -> bytes:
    with open(key_path, "rb") as key_file:
        return key_file.read()

class DatabaseManager:
    def __init__(self, encodings_path: str, key_path: str):
        self.encodings_path = encodings_path
        self.key_path = key_path
        
        # Garante que a pasta de dados exista
        os.makedirs(os.path.dirname(encodings_path), exist_ok=True)
        
        # Gera a chave de criptografia se ela não existir
        generate_and_save_key(self.key_path)
        self.key = load_key(self.key_path)
        self.cipher = Fernet(self.key)

    def load_encodings(self) -> Optional[Dict[str, Any]]:
        """
        Carrega e descriptografa os encodings do arquivo .pkl.
        Retorna os dados ou None se o arquivo não existir ou estiver vazio.
        """
        if not os.path.exists(self.encodings_path) or os.path.getsize(self.encodings_path) == 0:
            print("[INFO] Arquivo de encodings não encontrado ou vazio. Criando um novo.")
            return {"known_encodings": [], "known_names": []}
        
        try:
            with open(self.encodings_path, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            data = pickle.loads(decrypted_data)
            print(f"[INFO] Encodings de {len(data['known_names'])} pessoas carregados com sucesso.")
            return data
        except Exception as e:
            print(f"[ERRO] Falha ao carregar ou descriptografar encodings: {e}")
            print("[AVISO] Criando um novo arquivo de encodings.")
            # Se houver um erro (ex: chave errada, arquivo corrompido), cria um novo.
            return {"known_encodings": [], "known_names": []}

    def save_encodings(self, data: Dict[str, Any]):
        """
        Criptografa e salva os encodings no arquivo .pkl.
        """
        try:
            serialized_data = pickle.dumps(data)
            encrypted_data = self.cipher.encrypt(serialized_data)
            
            with open(self.encodings_path, "wb") as f:
                f.write(encrypted_data)
            print(f"[INFO] Encodings salvos e criptografados com sucesso em {self.encodings_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar e criptografar encodings: {e}")