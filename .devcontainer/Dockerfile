# Use a imagem oficial do Python
FROM python:3.12-slim

# Previne que o Python crie arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que a saída do Python seja enviada diretamente para o terminal
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /workspace

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria um usuário não-root
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Instala ferramentas Python úteis
RUN pip install --upgrade pip \
    && pip install black pylint autopep8 ipython ipdb

# Muda para o usuário não-root
USER $USERNAME

# Expõe a porta do Django
EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

