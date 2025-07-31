# Reconhecimento Facial Otimizado

Este projeto é uma aplicação de reconhecimento facial em tempo real, desenvolvida em Python, utilizando OpenCV, dlib e face_recognition. O objetivo é fornecer uma solução de Prova de Conceito (PoC) para identificação de pessoas a partir de imagens de vídeo, com foco em privacidade e segurança dos dados biométricos.

## Funcionalidades

- **Detecção de faces** em tempo real usando modelos DNN do OpenCV.
- **Reconhecimento facial** com embeddings de 128 dimensões (dlib/face_recognition).
- **Cadastro de novos rostos** diretamente pela interface, com criptografia dos dados biométricos.
- **Gerenciamento de banco de dados** de encodings e nomes, criptografado com Fernet (cryptography).
- **Seleção de câmera** pelo usuário.
- **Overlay na interface**: exibe caixas, nomes, FPS e instruções.
- **Log de inferências** para auditoria e análise.
- **Aviso de conformidade** com leis de privacidade.
- **Otimizações**: processamento de frames alternados, redimensionamento de imagem e limitação de FPS.

## Estrutura do Projeto

```
├── app/
│   ├── __init__.py
│   ├── database_manager.py
│   ├── face_detector.py
│   ├── face_recognizer.py
│   ├── ui_manager.py
│   └── video_capture.py
├── data/
│   ├── encodings.pkl
│   ├── inference_log.txt
│   ├── secret.key
│   └── known_faces/
├── models/
│   ├── deploy.prototxt.txt
│   ├── dlib_face_recognition_resnet_model_v1.dat
│   ├── res10_300x300_ssd_iter_140000.caffemodel
│   └── shape_predictor_68_face_landmarks.dat
├── config.py
├── main.py
├── requirements.txt
```

## Como Executar

1. **Clone o repositório:**
   ```
   git clone https://github.com/IsmarWolf/Reconhecimento-Facial
   cd FacialRecognition
   ```
2. **Crie e ative o ambiente virtual:**
   ```
   python -m venv .venv
   .venv\Scripts\Activate
   ```
3. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```
4. **Execute a aplicação:**
   ```
   python main.py
   ```

## Observações Importantes
- Os dados biométricos são armazenados localmente e criptografados.
- O usuário é responsável pelo uso e conformidade com leis de privacidade.
- Modelos pré-treinados devem estar na pasta `models/`.
- O sistema permite cadastrar novos rostos pressionando 'c' quando um rosto desconhecido é detectado.
- Pressione 'q' para sair da aplicação.

## Possíveis Incrementos Futuros
- Integração com banco de dados remoto (cloud ou on-premises).
- Interface gráfica (GUI) mais avançada (ex: PyQt, Tkinter).
- Suporte a múltiplas câmeras simultâneas.
- Notificações em tempo real (e-mail, Telegram, etc.).
- Dashboard web para gerenciamento dos dados e logs.
- Treinamento incremental e atualização automática dos modelos.
- Implementação de autenticação multi-fator.
- Suporte a reconhecimento de emoções ou atributos adicionais.
- Deploy em dispositivos embarcados (Raspberry Pi, Jetson Nano).

## Licença
Este projeto é fornecido como PoC e não deve ser usado em produção sem revisão de segurança e conformidade.
=======
# Reconhecimento-Facial
Projeto Proof of Concept de reconhecimento facial
>>>>>>> a3196a589192b14beb0f2206581e224325fc6d0e
