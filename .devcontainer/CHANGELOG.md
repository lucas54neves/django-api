# Dev Container - Changelog

## [2024-11-27] - Correções Críticas

### Corrigido
- ✅ Contexto de build do Docker (`.devcontainer/docker-compose.yml`)
  - Alterado de `context: .` para `context: ..`
  - Dockerfile agora referenciado corretamente como `.devcontainer/Dockerfile`
  
- ✅ Dockerfile - Instalação de dependências
  - Removida cópia de `requirements*.txt` durante build
  - Dependências agora instaladas via `postCreateCommand` para garantir atualização
  
- ✅ Scripts de post-create unificados
  - Removido `post-create.sh` duplicado
  - `postCreateCommand.sh` agora contém o melhor de ambos os scripts
  - Adicionado `postStartCommand` para usar `post-start.sh`
  
- ✅ Ordem dos parâmetros no mount SSH
  - Corrigido de `readonly,type=bind,consistency=cached`
  - Para `type=bind,consistency=cached,readonly`
  
- ✅ Makefile comando `run`
  - Alterado de `python manage.py runserver`
  - Para `python manage.py runserver 0.0.0.0:8000`
  - Agora acessível de fora do container
  
- ✅ Versão obsoleta no docker-compose.yml
  - Removido `version: '3.8'` (obsoleto no Docker Compose v2)

### Adicionado
- 📄 `.devcontainer/FIXES.md` - Documentação detalhada das correções
- 📄 `.devcontainer/TEST_GUIDE.md` - Guia completo de testes
- 📄 `.devcontainer/CHANGELOG.md` - Este arquivo

### Mantido
- ✅ Python 3.12-slim como imagem base
- ✅ Usuário não-root (vscode)
- ✅ SSH mount read-only para segurança
- ✅ Extensões VS Code para Python
- ✅ Port forwarding na porta 8000
- ✅ Variáveis de ambiente Django
- ✅ Git e GitHub CLI features
- ✅ Documentação SSH detalhada

### Arquivos Modificados
- `.devcontainer/devcontainer.json`
- `.devcontainer/docker-compose.yml`
- `.devcontainer/Dockerfile`
- `.devcontainer/postCreateCommand.sh`
- `Makefile`

### Arquivos Removidos
- `.devcontainer/post-create.sh` (duplicado)

### Arquivos Criados
- `.devcontainer/FIXES.md`
- `.devcontainer/TEST_GUIDE.md`
- `.devcontainer/CHANGELOG.md`
- `.devcontainer/.gitignore`

## Antes destas Correções

### Problemas
- ❌ Container não iniciava corretamente
- ❌ Erros durante o build do Docker
- ❌ Dependências não eram instaladas
- ❌ Servidor Django não era acessível do host
- ❌ Scripts de setup não executavam

## Depois destas Correções

### Status
- ✅ Container builda sem erros
- ✅ PostCreate executa completamente
- ✅ Dependências instaladas automaticamente
- ✅ Servidor acessível em localhost:8000
- ✅ Superuser criado automaticamente (admin/admin)
- ✅ SSH configurado (se disponível no host)
- ✅ Git hooks configurados
- ✅ Pronto para desenvolvimento

## Como Testar

Veja `.devcontainer/TEST_GUIDE.md` para instruções completas de teste.

## Suporte

Para mais informações:
- Correções detalhadas: `.devcontainer/FIXES.md`
- Documentação: `.devcontainer/README.md`
- SSH setup: `.devcontainer/SSH_SETUP.md`
