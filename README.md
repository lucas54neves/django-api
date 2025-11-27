# Django REST API - Sistema de Gerenciamento de Tarefas

Uma API RESTful robusta construída com Django e Django REST Framework, seguindo boas práticas de arquitetura em camadas com separação entre selectors (leitura) e services (escrita).

## 📋 Índice

- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como o Projeto Funciona](#como-o-projeto-funciona)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Deploy](#deploy)

## ✨ Características

- **API RESTful** completa com Django REST Framework
- **Autenticação** via Session e Token Authentication
- **Usuário customizado** extendendo AbstractUser
- **Paginação** configurável nas listagens
- **Arquitetura em camadas** (Views → Services/Selectors → Models)
- **Múltiplos ambientes** (dev, prod) com configurações separadas
- **Timestamps automáticos** em todos os models via TimeStampedModel
- **Testes automatizados** para garantir qualidade do código
- **Admin Django** para gerenciamento interno

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Django 5.2**
- **Django REST Framework** - Para criação da API REST
- **SQLite** - Banco de dados em desenvolvimento
- **Django Debug Toolbar** - Ferramentas de debug em desenvolvimento

## 🏗️ Arquitetura do Projeto

Este projeto segue uma arquitetura em camadas inspirada em DDD (Domain-Driven Design):

### Camadas da Aplicação

```
┌─────────────────────────────────────┐
│         API Layer (Views)           │
│     - Recebe requisições HTTP       │
│     - Valida dados (Serializers)    │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      Business Logic Layer           │
├─────────────────┬───────────────────┤
│   Services      │    Selectors      │
│   (Write)       │    (Read)         │
│ - create_task   │ - list_tasks      │
│ - update_task   │ - get_task        │
│ - delete_task   │                   │
└─────────────────┴───────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Data Layer (Models)         │
│     - Define estrutura de dados     │
│     - Interage com banco de dados   │
└─────────────────────────────────────┘
```

### Padrão de Separação: Selectors vs Services

- **Selectors** (`selectors.py`): Funções de leitura (queries). Retornam QuerySets ou objetos do banco.
- **Services** (`services.py`): Funções de escrita (commands). Encapsulam a lógica de negócio para criar/atualizar/deletar.

**Vantagens:**
- Código mais testável e organizado
- Lógica de negócio isolada das views
- Fácil reutilização de código
- Facilita refatoração futura

## 📁 Estrutura de Diretórios

```
django-api/
├── config/                      # Configurações do projeto Django
│   ├── settings/
│   │   ├── base.py             # Configurações base compartilhadas
│   │   ├── dev.py              # Configurações de desenvolvimento
│   │   └── prod.py             # Configurações de produção
│   ├── urls.py                 # URLs principais do projeto
│   ├── wsgi.py                 # Configuração WSGI
│   └── asgi.py                 # Configuração ASGI
│
├── core/                        # App central com código compartilhado
│   ├── models.py               # TimeStampedModel (modelo base abstrato)
│   └── pagination.py           # Classe de paginação customizada
│
├── users/                       # App de usuários
│   ├── models.py               # User model customizado
│   └── api/
│       ├── views.py            # UserViewSet (ReadOnly para admins)
│       ├── serializers.py      # UserSerializer
│       └── urls.py             # Rotas de usuários
│
├── tasks/                       # App de tarefas
│   ├── models.py               # Task model
│   ├── selectors.py            # Funções de consulta (read)
│   ├── services.py             # Funções de negócio (write)
│   ├── api/
│   │   ├── views.py            # TaskViewSet
│   │   ├── serializers.py      # TaskSerializer
│   │   └── urls.py             # Rotas de tarefas
│   └── tests/
│       └── test_tasks_api.py   # Testes da API de tarefas
│
├── manage.py                    # CLI do Django
├── db.sqlite3                   # Banco de dados SQLite
└── README.md                    # Este arquivo
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- virtualenv (recomendado)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/lucas54neves/django-api.git
cd django-api
```

### Passo 2: Crie e Ative o Ambiente Virtual

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instale as Dependências

```bash
pip install django djangorestframework django-debug-toolbar
```

**Ou crie um `requirements.txt`:**
```bash
# Salve as dependências instaladas
pip freeze > requirements.txt

# Para instalar em outro ambiente
pip install -r requirements.txt
```

### Passo 4: Configure as Variáveis de Ambiente (Opcional)

Para produção, defina a variável `DJANGO_SECRET_KEY`:

```bash
export DJANGO_SECRET_KEY='sua-chave-secreta-aqui'
```

### Passo 5: Execute as Migrações

```bash
python manage.py migrate
```

### Passo 6: Crie um Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções para criar username, email e senha.

### Passo 7: Inicie o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

A API estará disponível em: `http://127.0.0.1:8000/`

## 🔍 Como o Projeto Funciona

### 1. Configurações por Ambiente

O projeto usa múltiplos arquivos de configuração:

- **`base.py`**: Configurações comuns (apps instalados, middleware, banco de dados base)
- **`dev.py`**: Herda de `base.py` e adiciona DEBUG=True, debug_toolbar
- **`prod.py`**: Herda de `base.py` com DEBUG=False e configurações de produção

O arquivo `manage.py` está configurado para usar `config.settings.dev` por padrão.

### 2. Modelo de Usuário Customizado

O projeto usa um modelo de usuário customizado (`users.User`) que herda de `AbstractUser`:

```python
# users/models.py
class User(AbstractUser, TimeStampedModel):
    pass  # Adicione campos extras conforme necessário
```

Definido em `base.py`:
```python
AUTH_USER_MODEL = 'users.User'
```

**⚠️ Importante:** O usuário customizado deve ser definido antes de executar a primeira migração.

### 3. TimeStampedModel - Modelo Base Abstrato

Todos os models herdam de `TimeStampedModel` para ter campos de timestamp automáticos:

```python
# core/models.py
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

### 4. Modelo Task

```python
# tasks/models.py
class Task(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
```

Cada tarefa pertence a um usuário (owner) e possui título e status de conclusão.

### 5. Arquitetura de Services e Selectors

**Selectors** (consultas):
```python
# tasks/selectors.py
def list_tasks_for_user(user):
    return Task.objects.filter(owner=user).order_by('-created_at')

def get_task_for_user(*, user, task_id: int):
    return Task.objects.filter(owner=user, id=task_id).first()
```

**Services** (operações de escrita):
```python
# tasks/services.py
def create_task(*, owner, title: str, done: bool = False) -> Task:
    return Task.objects.create(owner=owner, title=title, done=done)

def update_task(*, task: Task, **data) -> Task:
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return task

def delete_task(*, task: Task):
    task.delete()
```

**ViewSet utilizando services e selectors:**
```python
# tasks/api/views.py
class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return selectors.list_tasks_for_user(self.request.user)
    
    def perform_create(self, serializer):
        task = services.create_task(
            owner=self.request.user,
            title=serializer.validated_data['title'],
            done=serializer.validated_data.get('done', False),
        )
        serializer.instance = task
```

### 6. Autenticação e Permissões

Configurado no `base.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

- Todas as rotas exigem autenticação por padrão
- Suporta autenticação via Session (para navegador) e Token (para apps)

### 7. Roteamento de URLs

URLs principais (`config/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('users.api.urls')),
        path('', include('tasks.api.urls')),
    ])),
]
```

Rotas de tasks (`tasks/api/urls.py`):
```python
router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
urlpatterns = router.urls
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
```

### Autenticação

Para acessar a API, você precisa estar autenticado. Use o Django Admin para fazer login:

1. Acesse `http://localhost:8000/admin/`
2. Faça login com o superusuário criado
3. Use a Session Authentication ou configure Token Authentication

### Endpoints de Tarefas

#### Listar todas as tarefas do usuário autenticado
```http
GET /api/v1/tasks/
```

**Resposta:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Minha primeira tarefa",
      "done": false,
      "created_at": "2025-11-27T10:30:00Z",
      "updated_at": "2025-11-27T10:30:00Z"
    }
  ]
}
```

#### Criar nova tarefa
```http
POST /api/v1/tasks/
Content-Type: application/json

{
  "title": "Nova tarefa",
  "done": false
}
```

#### Obter detalhes de uma tarefa
```http
GET /api/v1/tasks/{id}/
```

#### Atualizar tarefa
```http
PUT /api/v1/tasks/{id}/
Content-Type: application/json

{
  "title": "Tarefa atualizada",
  "done": true
}
```

#### Atualização parcial
```http
PATCH /api/v1/tasks/{id}/
Content-Type: application/json

{
  "done": true
}
```

#### Deletar tarefa
```http
DELETE /api/v1/tasks/{id}/
```

### Endpoints de Usuários (Apenas Admin)

#### Listar usuários
```http
GET /api/v1/users/
```

#### Detalhes de um usuário
```http
GET /api/v1/users/{id}/
```

**Nota:** Apenas usuários admin podem acessar os endpoints de usuários.

### Paginação

A API usa paginação por padrão:

- **Tamanho padrão da página:** 20 itens
- **Tamanho máximo:** 100 itens
- **Parâmetro personalizado:** `?page_size=50`

Exemplo:
```http
GET /api/v1/tasks/?page=2&page_size=10
```

## 🧪 Testes

O projeto inclui testes automatizados para a API de tarefas.

### Executar todos os testes

```bash
python manage.py test
```

### Executar testes de um app específico

```bash
python manage.py test tasks
```

### Executar com verbosidade

```bash
python manage.py test --verbosity=2
```

### Estrutura dos Testes

Os testes estão em `tasks/tests/test_tasks_api.py` e cobrem:

- Criação de tarefas
- Listagem de tarefas
- Atualização de tarefas
- Deleção de tarefas
- Permissões e isolamento entre usuários

## 🚀 Deploy

### Preparação para Produção

1. **Altere o ambiente para produção:**

   Edite o `wsgi.py` ou defina a variável de ambiente:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
   ```

2. **Configure a SECRET_KEY:**

   ```bash
   export DJANGO_SECRET_KEY='chave-secreta-super-segura'
   ```

3. **Configure o banco de dados (PostgreSQL recomendado):**

   Em `config/settings/prod.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'seu_banco',
           'USER': 'seu_usuario',
           'PASSWORD': 'sua_senha',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Configure ALLOWED_HOSTS:**

   ```python
   ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']
   ```

5. **Colete arquivos estáticos:**

   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Execute migrações:**

   ```bash
   python manage.py migrate
   ```

### Opções de Deploy

- **Heroku**: Plataforma fácil para deploy de aplicações Django
- **AWS EC2**: Máquinas virtuais configuráveis
- **DigitalOcean**: Droplets com configuração simplificada
- **Railway**: Deploy moderno e simplificado
- **Render**: Alternativa moderna ao Heroku

### Servidor WSGI/ASGI

Para produção, use servidores como:

- **Gunicorn** (WSGI)
  ```bash
  pip install gunicorn
  gunicorn config.wsgi:application --bind 0.0.0.0:8000
  ```

- **Uvicorn** (ASGI)
  ```bash
  pip install uvicorn
  uvicorn config.asgi:application --host 0.0.0.0 --port 8000
  ```

### Nginx como Reverse Proxy

Configure o Nginx para servir a aplicação:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /caminho/para/staticfiles/;
    }
}
```

## 📝 Boas Práticas Implementadas

✅ Separação de configurações por ambiente  
✅ Modelo de usuário customizado  
✅ Arquitetura em camadas (Services/Selectors)  
✅ Uso de keyword-only arguments (`*`) nas funções  
✅ Paginação configurável  
✅ Autenticação obrigatória  
✅ Timestamps automáticos  
✅ Testes automatizados  
✅ Isolamento de dados por usuário  

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 📧 Contato

Lucas Neves - [@lucas54neves](https://github.com/lucas54neves)

---

**Desenvolvido com ❤️ usando Django e Django REST Framework**
