# 2025-1CriptoTP4nicolebertolino-
Trabalho prático 4 de cripitografia e sistemas de segurança: ASSINATURAS DIGITAIS COM ECDSA EM PYTHON.
Objetivo:
  Implementar e verificar assinaturas digitais com ECDSA em Python, entendendo sua aplicação na autenticação de transações em uma blockchain.


# 2025-1CriptoTP3nicolebertolino-
Comandos para executar local:

comando docker para criar a imagem des 
docker build -t blockchain_ecdsa-crypto .

comando para executar imagem via docker:
docker run -it --rm -v "${pwd}/app:/app" blockchain_ecdsa-crypto
 

Comandos para enviar imagens para o docker hub
1. Renomear sua imagem local para o padrão Docker Hub
docker tag blockchain_ecdsa-crypto nicolebertolino/2025-1criptotp4nicolebertolino:blockchain-ecdsa

2. Fazer login no Docker Hub via terminal
docker login

3. Enviar a imagem para o Docker Hub
docker push nicolebertolino/2025-1criptotp4nicolebertolino:blockchain-ecdsa
							
							
							
Como outros usarão a minha imagem do docker hub:
docker pull nicolebertolino/2025-1criptotp4nicolebertolino:blockchain-ecdsa

E executar com:
docker run -it --rm nicolebertolino/2025-1criptotp4nicolebertolino:blockchain-ecdsa
