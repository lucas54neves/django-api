# 🧪 Guia de Teste - Dev Container Corrigido

## 📋 Resumo das Correções

Foram identificados e corrigidos **6 problemas críticos** que impediam o dev container de funcionar:

1. ✅ Contexto de build do Docker incorreto
2. ✅ Dockerfile tentando copiar arquivos com caminho inválido
3. ✅ Scripts de post-create duplicados
4. ✅ Ordem incorreta dos parâmetros do mount SSH
5. ✅ Makefile com IP incorreto para containers
6. ✅ Versão obsoleta no docker-compose.yml

---

## 🚀 Como Testar Agora

### Pré-requisitos

Antes de começar, certifique-se:

- [ ] Docker Desktop está **instalado** e **rodando**
- [ ] VS Code ou Cursor está instalado
- [ ] Extensão **"Dev Containers"** está instalada
- [ ] Você está na branch correta do projeto

### Passo 1: Limpar Containers Antigos (Se Aplicável)

Se você já tinha tentado abrir o container antes:

```bash
# Parar e remover containers antigos
docker compose -f .devcontainer/docker-compose.yml down --volumes

# Remover imagens antigas (opcional, mas recomendado)
docker rmi $(docker images -q --filter "dangling=true") 2>/dev/null || true

# Limpar cache do Docker (opcional)
docker builder prune -f
```

### Passo 2: Abrir o Projeto no Dev Container

#### No VS Code/Cursor:

1. **Abra o projeto** (pasta raiz `django-api/`)
2. Pressione `F1` ou `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
3. Digite e selecione: **"Dev Containers: Reopen in Container"**
4. Aguarde o build completar

**Tempo estimado:**
- Primeira vez: ~5-10 minutos
- Rebuilds subsequentes: ~1-2 minutos

#### O que deve acontecer:

```
[1/6] Building Docker image...
  → Using Python 3.12-slim
  → Installing system dependencies
  → Creating vscode user
  
[2/6] Starting container...
  
[3/6] Running postCreateCommand.sh...
  📦 Installing Python dependencies...
  🔑 Fixing SSH permissions...
  🗄️  Running database migrations...
  👤 Setting up default superuser...
  ✅ Superuser created: username=admin, password=admin
  🪝 Setting up Git hooks...
  
✅ Dev container setup complete!
```

### Passo 3: Validar o Ambiente

Uma vez dentro do container, execute estes comandos no terminal:

#### 3.1. Verificar Python e Dependências

```bash
# Verificar versão do Python
python --version
# Esperado: Python 3.12.x

# Verificar pip
pip --version

# Verificar Django instalado
python -c "import django; print(f'Django {django.get_version()}')"
# Esperado: Django 5.2.x

# Listar dependências principais
pip list | grep -E "django|rest"
```

#### 3.2. Verificar Banco de Dados

```bash
# Ver status das migrações
python manage.py showmigrations

# Deve mostrar algo como:
# admin
#  [X] 0001_initial
#  [X] 0002_...
# auth
#  [X] 0001_initial
#  ...
# users
#  [X] 0001_initial

# Verificar se o superuser existe
python manage.py shell -c "from django.contrib.auth import get_user_model; print(f'Superuser exists: {get_user_model().objects.filter(username=\"admin\").exists()}')"
# Esperado: Superuser exists: True
```

#### 3.3. Verificar Git e SSH (Opcional)

```bash
# Verificar Git
git --version

# Verificar GitHub CLI (opcional)
gh --version

# Testar SSH (se você configurou)
ssh -T git@github.com
# Esperado: "Hi username! You've successfully authenticated..."
# Se falhar: isso é normal se você não configurou SSH keys
```

#### 3.4. Verificar Estrutura de Arquivos

```bash
# Ver estrutura do projeto
ls -la

# Verificar que você está em /workspace
pwd
# Esperado: /workspace

# Verificar permissões
whoami
# Esperado: vscode
```

### Passo 4: Iniciar o Servidor Django

```bash
# Opção 1: Usando Makefile (recomendado)
make run

# Opção 2: Comando direto
python manage.py runserver 0.0.0.0:8000
```

**O que deve aparecer:**

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 27, 2025 - 22:50:00
Django version 5.2, using settings 'config.settings.dev'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### Passo 5: Testar os Endpoints

#### No navegador do seu host (não do container):

1. **Homepage/API Root**
   ```
   http://localhost:8000/api/v1/
   ```
   Deve mostrar a interface da API (Django REST Framework)

2. **Django Admin**
   ```
   http://localhost:8000/admin
   ```
   Login:
   - Username: `admin`
   - Password: `admin`
   
   Deve entrar no painel administrativo

3. **Tasks API**
   ```
   http://localhost:8000/api/v1/tasks/
   ```
   Deve mostrar lista de tasks (vazia inicialmente)

#### Usando curl (dentro do container ou no host):

```bash
# Verificar se o servidor responde
curl http://localhost:8000/api/v1/

# Login no admin (pegar cookie de sessão)
curl -c cookies.txt -X POST http://localhost:8000/admin/login/ \
  -d "username=admin&password=admin&csrfmiddlewaretoken=..." \
  -H "Referer: http://localhost:8000/admin/login/"

# Ou use a API diretamente após fazer login via navegador
```

### Passo 6: Rodar os Testes

```bash
# Todos os testes
make test

# Esperado:
# Creating test database...
# System check identified no issues (0 silenced).
# ...
# ----------------------------------------------------------------------
# Ran X tests in X.XXs
#
# OK

# Testes com coverage
make test-coverage

# Verificar linting
make lint

# Formatar código
make format

# Rodar tudo (como na CI)
make check
```

---

## ✅ Checklist de Sucesso

Marque cada item à medida que validar:

### Build e Inicialização
- [ ] Container buildou sem erros
- [ ] `postCreateCommand.sh` executou completamente
- [ ] Nenhum erro apareceu durante o setup

### Ambiente Python
- [ ] Python 3.12.x está instalado
- [ ] Django 5.2.x está instalado
- [ ] Todas as dependências do `requirements.txt` instaladas
- [ ] Todas as dependências do `requirements-dev.txt` instaladas

### Banco de Dados
- [ ] Migrações foram aplicadas
- [ ] Superuser `admin` foi criado
- [ ] `db.sqlite3` existe em `/workspace`

### Servidor Django
- [ ] Servidor inicia em `0.0.0.0:8000`
- [ ] Acessível via `http://localhost:8000` no host
- [ ] Django admin funciona (login com admin/admin)
- [ ] API endpoints respondem

### Testes e Qualidade
- [ ] `make test` passa todos os testes
- [ ] `make lint` não reporta erros críticos
- [ ] `make format` funciona

### Git e SSH (Opcional)
- [ ] Git está configurado
- [ ] SSH keys montadas (se aplicável)
- [ ] Push/pull funcionam (se aplicável)

---

## 🐛 Troubleshooting

### ❌ Container não builda

**Erro comum:**
```
ERROR: failed to solve: failed to compute cache key: 
failed to calculate checksum of ref ...
```

**Solução:**
```bash
# Rebuild sem cache
F1 → "Dev Containers: Rebuild Container Without Cache"

# Ou via terminal:
docker compose -f .devcontainer/docker-compose.yml build --no-cache
```

---

### ❌ postCreateCommand falha

**Erro comum:**
```
bash: .devcontainer/postCreateCommand.sh: Permission denied
```

**Solução:**
```bash
# No host (fora do container)
chmod +x .devcontainer/postCreateCommand.sh
chmod +x .devcontainer/post-start.sh

# Rebuild o container
```

---

### ❌ Porta 8000 já está em uso

**Erro:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:8000: 
bind: address already in use
```

**Solução:**
```bash
# Encontrar processo usando a porta
lsof -i :8000

# Matar o processo
kill -9 <PID>

# Ou mudar a porta em docker-compose.yml:
ports:
  - "8001:8000"  # Use 8001 no host
```

---

### ❌ Dependências não instaladas

**Sintoma:**
```python
ModuleNotFoundError: No module named 'django'
```

**Solução:**
```bash
# Dentro do container
pip install --user -r requirements.txt
pip install --user -r requirements-dev.txt

# Ou rebuild o container
```

---

### ❌ Migrações não foram aplicadas

**Sintoma:**
```
django.db.utils.OperationalError: no such table: ...
```

**Solução:**
```bash
# Aplicar migrações manualmente
python manage.py migrate

# Verificar
python manage.py showmigrations
```

---

### ❌ Superuser não existe

**Sintoma:**
Login falha com admin/admin

**Solução:**
```bash
# Criar manualmente
python manage.py createsuperuser

# Ou recriar o admin padrão
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.filter(username='admin').delete()
>>> User.objects.create_superuser('admin', 'admin@example.com', 'admin')
>>> exit()
```

---

### ❌ Servidor não é acessível do host

**Sintoma:**
Servidor roda, mas `localhost:8000` não abre no navegador

**Checklist:**
1. Servidor está rodando em `0.0.0.0:8000` (não `127.0.0.1`)?
2. Port forwarding está configurado no devcontainer.json?
3. Porta 8000 está livre no host?
4. Firewall bloqueando?

**Solução:**
```bash
# Verificar que está usando 0.0.0.0
python manage.py runserver 0.0.0.0:8000

# Ou use o Makefile (já corrigido)
make run
```

---

### ❌ SSH não funciona

Consulte o guia detalhado: `.devcontainer/SSH_SETUP.md`

---

## 📊 Resultados Esperados

### ✅ Build Bem-Sucedido

```
[+] Building 123.4s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 1.23kB
 => [internal] load .dockerignore
 => ...
 => exporting to image
 => => exporting layers
 => => writing image sha256:...
 => => naming to docker.io/library/devcontainer-app
```

### ✅ PostCreate Bem-Sucedido

```
🚀 Starting post-create setup...
📦 Installing Python dependencies...
  ✅ Requirements installed
🔑 Fixing SSH permissions...
  ✅ SSH keys available
🗄️  Running database migrations...
  ✅ Migrations applied
👤 Setting up default superuser...
  ✅ Superuser created: username=admin, password=admin
🪝 Setting up Git hooks...
  ✅ Git hooks configured
✅ Dev container setup complete!
```

### ✅ Servidor Rodando

```
System check identified no issues (0 silenced).
November 27, 2025 - 22:50:00
Django version 5.2, using settings 'config.settings.dev'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### ✅ Testes Passando

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....................
----------------------------------------------------------------------
Ran 20 tests in 1.234s

OK
Destroying test database for alias 'default'...
```

---

## 📝 Próximos Passos Após Validação

Se tudo estiver funcionando:

1. ✅ **Commit as alterações**
   ```bash
   git add .devcontainer/ Makefile
   git commit -m "fix: corrigir configuração do dev container"
   ```

2. ✅ **Testar desenvolvimento normal**
   - Criar uma nova task via API
   - Editar código e ver auto-reload
   - Rodar testes após mudanças

3. ✅ **Documentar mudanças** (opcional)
   - Atualizar CHANGELOG se houver
   - Notificar o time sobre as correções

4. ✅ **Validar SSH/Git** (se usar)
   - Fazer push/pull
   - Verificar SSH keys funcionando

---

## 📞 Suporte

Se após seguir todos os passos ainda houver problemas:

1. **Verifique os logs:**
   ```bash
   # Logs do Docker
   docker compose -f .devcontainer/docker-compose.yml logs
   
   # Logs do container
   docker logs <container-name>
   ```

2. **Capture informações do sistema:**
   ```bash
   # Versão do Docker
   docker --version
   docker compose version
   
   # Sistema operacional
   uname -a  # Linux/Mac
   ver       # Windows
   ```

3. **Documentos de referência:**
   - `.devcontainer/FIXES.md` - Detalhes das correções
   - `.devcontainer/README.md` - Documentação completa
   - `.devcontainer/SSH_SETUP.md` - Configuração SSH
   - Projeto README.md - Documentação geral

---

**Teste realizado em:** 27/11/2024  
**Status esperado:** ✅ Todas as validações devem passar

Boa sorte! 🚀

