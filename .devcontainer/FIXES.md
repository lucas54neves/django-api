# Dev Container - Correções Aplicadas

## 🔧 Problemas Identificados e Corrigidos

### 1. **Contexto de Build do Docker Incorreto**

**Problema:**
```yaml
# docker-compose.yml (ANTES)
build:
  context: .
  dockerfile: Dockerfile
```

O contexto estava definido como `.` (pasta `.devcontainer`), mas o Dockerfile tentava copiar arquivos de `../requirements*.txt`, o que pode falhar ou causar confusão.

**Solução:**
```yaml
# docker-compose.yml (DEPOIS)
build:
  context: ..
  dockerfile: .devcontainer/Dockerfile
```

Agora o contexto é a raiz do projeto, e o Dockerfile está referenciado corretamente.

---

### 2. **Dockerfile Tentando Copiar Requirements Durante o Build**

**Problema:**
```dockerfile
# Dockerfile (ANTES)
COPY ../requirements*.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
```

Isso pode falhar se o contexto não estiver correto, e também torna o rebuild demorado quando as dependências mudam.

**Solução:**
```dockerfile
# Dockerfile (DEPOIS)
# Install Python dependencies (will be installed via postCreateCommand)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
```

Agora as dependências são instaladas durante o `postCreateCommand`, garantindo que estejam sempre atualizadas e evitando problemas com o contexto de build.

---

### 3. **Duplicação de Scripts de Post-Create**

**Problema:**
Existiam dois scripts fazendo trabalhos similares:
- `post-create.sh` (não referenciado no devcontainer.json)
- `postCreateCommand.sh` (novo, mas inicialmente incompleto)

**Solução:**
- ✅ Unificamos em um único `postCreateCommand.sh` com o melhor de ambos os scripts
- ✅ Removemos o `post-create.sh` duplicado
- ✅ Adicionamos `postStartCommand` para usar o `post-start.sh` existente

```json
{
  "postCreateCommand": "bash .devcontainer/postCreateCommand.sh",
  "postStartCommand": "bash .devcontainer/post-start.sh"
}
```

---

### 4. **Ordem dos Parâmetros do Mount SSH**

**Problema:**
```json
"mounts": [
  "source=...,target=...,readonly,type=bind,consistency=cached"
]
```

A ordem dos parâmetros pode causar problemas em algumas versões do Docker.

**Solução:**
```json
"mounts": [
  "source=...,target=...,type=bind,consistency=cached,readonly"
]
```

Ordem corrigida: `type` antes de `readonly`.

---

### 5. **Makefile com IP Incorreto para Container**

**Problema:**
```makefile
run: ## Start development server
	python manage.py runserver
```

Isso usa `127.0.0.1` por padrão, que não é acessível de fora do container.

**Solução:**
```makefile
run: ## Start development server
	python manage.py runserver 0.0.0.0:8000
```

Agora o servidor aceita conexões de qualquer IP, permitindo acesso via `localhost:8000` no host.

---

## ✅ O Que Foi Mantido (Estava Correto)

1. ✅ **Python 3.12** - Versão moderna e estável
2. ✅ **Usuário não-root (vscode)** - Boa prática de segurança
3. ✅ **SSH mount read-only** - Mantém as chaves seguras
4. ✅ **VS Code extensions** - Configuração completa para Python
5. ✅ **Variáveis de ambiente** - `DJANGO_SETTINGS_MODULE=config.settings.dev`
6. ✅ **Port forwarding** - Porta 8000 corretamente exposta
7. ✅ **Git features** - Git e GitHub CLI instalados
8. ✅ **SSH_SETUP.md** - Documentação detalhada mantida

---

## 🚀 Como Usar Agora

### 1. Reconstruir o Container

Se você já tinha tentado abrir o container antes:

1. Abra o VS Code/Cursor
2. Pressione `F1` ou `Ctrl+Shift+P`
3. Digite: **"Dev Containers: Rebuild Container"**
4. Aguarde o build completar (~5-10 minutos na primeira vez)

### 2. Iniciar pela Primeira Vez

Se é a primeira vez:

1. Abra o projeto no VS Code/Cursor
2. Pressione `F1` ou `Ctrl+Shift+P`
3. Digite: **"Dev Containers: Reopen in Container"**
4. Aguarde o container inicializar

### 3. Após o Container Iniciar

O script `postCreateCommand.sh` automaticamente:
- ✅ Instala todas as dependências Python
- ✅ Configura SSH (se disponível)
- ✅ Roda migrações do banco de dados
- ✅ Cria um superuser padrão: `admin` / `admin`
- ✅ Configura Git hooks

### 4. Iniciar o Servidor Django

```bash
# Opção 1: Usando Makefile (recomendado)
make run

# Opção 2: Comando direto
python manage.py runserver 0.0.0.0:8000
```

### 5. Acessar a Aplicação

- **API**: http://localhost:8000/api/v1/
- **Admin**: http://localhost:8000/admin
  - Usuário: `admin`
  - Senha: `admin`

---

## 🔍 Verificando Se Está Funcionando

### Checklist de Validação

Execute estes comandos dentro do container para validar:

```bash
# 1. Verificar Python
python --version
# Esperado: Python 3.12.x

# 2. Verificar dependências
pip list | grep -i django
# Esperado: Django 5.2.x

# 3. Verificar banco de dados
python manage.py showmigrations
# Esperado: Lista de migrações com [X] aplicadas

# 4. Verificar SSH (se configurado)
ssh -T git@github.com
# Esperado: Mensagem de autenticação bem-sucedida

# 5. Testar o servidor
python manage.py check
# Esperado: System check identified no issues (0 silenced).

# 6. Rodar testes
make test
# Esperado: Todos os testes passando
```

---

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs do Docker
docker logs <container-id>

# Rebuild sem cache
F1 → "Dev Containers: Rebuild Container Without Cache"
```

### Dependências não instaladas

```bash
# Dentro do container
pip install --user -r requirements.txt
pip install --user -r requirements-dev.txt
```

### Porta 8000 em uso

```bash
# No host, encontrar processo usando a porta
lsof -i :8000

# Matar processo
kill -9 <PID>

# Ou usar outra porta no docker-compose.yml
ports:
  - "8001:8000"
```

### SSH não funciona

Consulte: `.devcontainer/SSH_SETUP.md` para troubleshooting detalhado

---

## 📚 Arquivos Modificados

- ✏️ `.devcontainer/devcontainer.json` - Corrigido mounts e adicionado postStartCommand
- ✏️ `.devcontainer/Dockerfile` - Removida cópia de requirements durante build
- ✏️ `.devcontainer/docker-compose.yml` - Corrigido contexto de build
- ✏️ `.devcontainer/postCreateCommand.sh` - Unificado e melhorado
- 🗑️ `.devcontainer/post-create.sh` - Removido (duplicado)
- ✏️ `Makefile` - Corrigido comando `make run` para usar 0.0.0.0

---

## 📝 Próximos Passos Recomendados

1. ✅ Testar o container com estas correções
2. ✅ Validar que o servidor Django inicia corretamente
3. ✅ Testar SSH/Git operations (se aplicável)
4. ✅ Rodar `make check` para validar qualidade do código
5. ✅ Atualizar documentação se necessário

---

**Correções aplicadas em:** 27/11/2024

Se ainda encontrar problemas, verifique:
- Docker Desktop está rodando
- Extensão "Dev Containers" está instalada
- Você tem permissões de sudo (se no Linux)

