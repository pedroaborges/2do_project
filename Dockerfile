# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copia o requirements
COPY requirements.txt .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando padrão (substituído pelo compose quando necessário)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
