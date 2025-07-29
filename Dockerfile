# Usa a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY app/ /app/

# Instala dependências (se houver)
# RUN pip install --no-cache-dir -r requirements.txt

# Define o comando padrão para executar o script
ENTRYPOINT ["python", "./blockchain.py"]