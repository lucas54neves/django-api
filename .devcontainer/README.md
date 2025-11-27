# Dev Container - Django API

Este projeto está configurado para usar Dev Containers, permitindo um ambiente de desenvolvimento consistente e isolado.

## 📋 Pré-requisitos

- **Docker Desktop** instalado e rodando
- **Visual Studio Code** ou **Cursor** com a extensão "Dev Containers" instalada
  - Extensão: `ms-vscode-remote.remote-containers`

## 🚀 Como usar

### Opção 1: Abrir no Dev Container (Recomendado)

1. Abra o projeto no VS Code/Cursor
2. Pressione `F1` ou `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Digite: `Dev Containers: Reopen in Container`
4. Aguarde o container ser construído e inicializado

### Opção 2: Usar Command Palette

1. Com o projeto aberto, clique no ícone verde no canto inferior esquerdo
2. Selecione `Reopen in Container`

### Opção 3: Prompt Automático

- Se você tiver a pasta `.devcontainer` no projeto, o VS Code/Cursor pode sugerir automaticamente abrir no container

## 🔧 O que acontece automaticamente

Quando o container é criado pela primeira vez:

1. ✅ Instala todas as dependências do `requirements.txt`
2. ✅ Executa as migrações do Django (`python manage.py migrate`)
3. ✅ Inicia o servidor de desenvolvimento na porta 8000

## 🌐 Acessando a aplicação

Após o container iniciar, acesse:
- **URL**: http://localhost:8000
- **Admin**: http://localhost:8000/admin (se configurado)

## 🛠️ Extensões incluídas

O Dev Container vem com extensões pré-instaladas:

- **Python** - Suporte completo para Python
- **Pylance** - IntelliSense avançado
- **Black Formatter** - Formatação automática de código
- **Pylint** - Linting de código Python
- **Django** - Suporte para templates e sintaxe Django
- **Jinja** - Suporte para templates Jinja2
- **Docker** - Gerenciamento de containers
- **GitLens** - Recursos avançados de Git

## ⚙️ Configurações personalizadas

### Formatação automática

O código será formatado automaticamente ao salvar usando Black.

### Linting

O Pylint está ativado para análise de código em tempo real.

## 🔄 Reconstruir o container

Se você fizer alterações no Dockerfile ou devcontainer.json:

1. Pressione `F1` ou `Ctrl+Shift+P`
2. Digite: `Dev Containers: Rebuild Container`

## 📝 Comandos úteis

Dentro do container, você pode executar:

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test

# Abrir shell do Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 🐛 Troubleshooting

### O container não inicia

1. Certifique-se de que o Docker Desktop está rodando
2. Tente reconstruir o container: `Dev Containers: Rebuild Container`
3. Verifique os logs do Docker para erros

### Porta 8000 já está em uso

1. Pare qualquer servidor Django rodando fora do container
2. Ou altere a porta em `.devcontainer/devcontainer.json` e `docker-compose.yml`

### Dependências não instalam

1. Verifique se o `requirements.txt` está correto
2. Reconstrua o container do zero
3. Execute manualmente: `pip install -r requirements.txt`

## 🔒 Segurança

O container roda com um usuário não-root (`vscode`) para maior segurança.

## 📚 Recursos adicionais

- [Documentação oficial dos Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Documentação do Django](https://docs.djangoproject.com/)

