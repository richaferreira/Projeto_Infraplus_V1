# 💧 InfraPlus - Gestão de Infraestrutura Hídrica - Projeto Acadêmico.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
</p>

<br>

## 📌 Sobre o Projeto

O **InfraPlus** é uma plataforma web desenvolvida para otimizar o reporte e a gestão de problemas relacionados à rede de água (vazamentos, falta de abastecimento, manutenção). O objetivo é conectar o cidadão aos órgãos responsáveis de forma ágil, permitindo um monitoramento eficiente da infraestrutura urbana.

> [!IMPORTANT]
> **Diferencial Técnico:** O projeto utiliza uma arquitetura baseada em **Camadas e Repositórios**, separando rigorosamente as responsabilidades (SOC) e facilitando a manutenção e a escalabilidade do software.

### 🎯 **Propósito da Aplicação**

- **Criar denúncias** sobre problemas de água/saneamento
- **Visualizar denúncias** abertas, em andamento ou resolvidas
- **Geolocalização**: Sistema de mapa interativo (Leaflet) + busca por proximidade
- **Gestão de empresas** terceirizadas para resolução
- **Painel administrativo** para monitoramento com gráficos e KPIs
- **Painel da empresa** para gestão de denúncias atribuídas
- **Upload de imagens** para evidências
- **Assistente de chat** com IA para consultas rápidas
- **Notificações em tempo real** via SSE (Server-Sent Events)

---

## 🚀 Funcionalidades Ativas

### Gerais
* ✅ **Reporte com Anexos:** Registro de problemas com localização e múltiplos uploads de fotos.
* ✅ **Comentários:** Logs de interação identificando automaticamente o usuário logado.
* ✅ **Geolocalização:** Mapa interativo (Leaflet) com busca por denúncias próximas (Haversine, raio até 50 km).
* ✅ **Notificações em Tempo Real:** Alertas via SSE (Server-Sent Events) com toasts ao vivo para novas denúncias e mudanças de status.
* ✅ **Assistente de Chat IA:** Chatbot em `/chat` para consultas de denúncias, estatísticas e buscas (baseado em regras).
* ✅ **Rate Limiting:** Proteção contra brute force no login (5 tentativas por 5 minutos por IP).
* ✅ **Testes Automatizados:** 30 testes unitários com pytest cobrindo rotas, serviços e funcionalidades.

### Painel Administrativo (`/admin`)
* ✅ **Dashboard com KPIs:** Cards coloridos com ícones mostrando total, abertas, em andamento e resolvidas.
* ✅ **Gráficos:** Denúncias por dia (7 dias) e distribuição por categoria (Chart.js).
* ✅ **Filtros avançados:** Por categoria, status, período e busca textual com paginação.
* ✅ **Detalhe da denúncia:** Informações completas (autor, empresa atribuída, localização com mapa, comentários).
* ✅ **Atribuição de empresa:** Atribuir/trocar empresa responsável por uma denúncia.
* ✅ **Gestão de empresas:** Criar, listar e excluir empresas terceirizadas com contagem de denúncias.
* ✅ **Gestão de usuários:** Listagem de todos os usuários (`/admin/usuarios`) com busca, KPIs e badges por tipo (Admin/Empresa/Cidadão).
* ✅ **Exportação CSV:** Download de todas as denúncias em formato CSV.

### Painel da Empresa (`/empresa`)
* ✅ **Dashboard com KPIs:** Cards com contagem por status (abertas, em andamento, resolvidas).
* ✅ **Gráficos com cores:** Doughnut charts com cores semânticas (vermelho/laranja/verde).
* ✅ **Filtros:** Filtro por status e busca por título.
* ✅ **Paginação:** Listagem paginada de denúncias atribuídas (12 por página).
* ✅ **Detalhe da denúncia:** Visualização com imagens, mapa, comentários e formulário de resposta.

### Painel Público
* ✅ **Home com mapa:** Mapa interativo com marcadores de denúncias + botão "Próximas a mim".
* ✅ **Listagem com filtros:** Por categoria, status, período e busca textual.
* ✅ **Minhas Denúncias:** Página `/minhas-denuncias` para cidadãos verem apenas suas denúncias com KPIs e filtros.
* ✅ **Detalhe da denúncia:** Visualização com mapa, imagens, comentários e formulário de comentário.
* ✅ **Páginas de erro:** 404 e 500 estilizadas.

<br>

## 📂 Estrutura do Projeto

A organização do projeto segue o padrão **MVC** (Model-View-Controller) aliado ao **Repository Pattern**:

```bash
├── backend/
│   └── app/
│       ├── __init__.py          # Inicialização Flask
│       ├── config.py            # Configurações
│       ├── extensions.py        # Extensões (db, login, csrf, mail)
│       ├── notifications.py     # NotificationBus (SSE pub/sub thread-safe)
│       ├── rate_limit.py        # Rate limiter in-memory por IP
│       ├── models/              # Modelos de dados (User, Report, Company, Comment, ReportImage)
│       ├── services/            # Lógica de negócios (ReportService)
│       ├── repositories/        # Padrão Repository (ReportRepository)
│       ├── blueprints/
│       │   ├── public/          # Rotas públicas (home, denúncias, minhas denúncias, API nearby)
│       │   ├── auth/            # Autenticação (login, registro, logout)
│       │   ├── admin/           # Painel administrativo (dashboard, empresas, usuários)
│       │   ├── company/         # Painel da empresa (dashboard, detalhe, resposta)
│       │   ├── chat/            # Assistente de chat IA (engine + rotas)
│       │   └── sse/             # Server-Sent Events (stream de notificações)
│       └── utils.py             # Utilitários (@admin_required, etc.)
├── frontend/
│   ├── templates/               # Templates Jinja2
│   │   ├── admin/               # Páginas do admin (dashboard, report_detail, users_list, companies)
│   │   ├── company/             # Páginas da empresa (dashboard, report_detail)
│   │   ├── public/              # Páginas públicas (home, reports, my_reports, report_detail)
│   │   ├── chat/                # Chat interface
│   │   ├── errors/              # Páginas 404 e 500
│   │   └── shared/              # Componentes reutilizáveis (_pagination, _status_badge, _flashes)
│   └── static/
│       ├── css/styles.css       # Estilos customizados
│       ├── js/                  # Scripts (map_home, map_detail, map_picker, charts, report_modal)
│       └── uploads/             # Imagens enviadas
├── tests/                       # Testes unitários (pytest)
│   ├── conftest.py              # Fixtures de teste
│   ├── test_admin.py            # Testes do painel admin
│   ├── test_auth.py             # Testes de autenticação
│   ├── test_chat.py             # Testes do chat
│   ├── test_notifications.py   # Testes do NotificationBus
│   ├── test_public.py           # Testes das rotas públicas
│   └── test_rate_limit.py       # Testes do rate limiter
├── requirements.txt             # Dependências Python
└── run.py                       # Entrada da aplicação
```

### 📋 **Informações Gerais**
- **Nome**: Projeto Infraplus (InfraPlus — Águas Seguras)
- **Descrição**: Plataforma web para reporte e gestão de problemas de infraestrutura hídrica
- **Licença**: Apache License 2.0
- **Criado em**: 4 de março de 2023
- **Visibilidade**: Público

---

### 🔧 **Stack Tecnológico**

**Backend:**
- **Flask** (framework web Python)
- **Flask-SQLAlchemy** (ORM para banco de dados)
- **Flask-Login** (autenticação de usuários)
- **Flask-WTF / CSRFProtect** (formulários e proteção CSRF)
- **Flask-Mail** (envio de e-mails)
- **SQLite** (banco de dados padrão)
- **pytest** (testes unitários)

**Frontend:**
- **HTML5** com Jinja2 templates
- **Bootstrap 5.3.2** (UI framework)
- **Bootstrap Icons** (ícones)
- **Leaflet.js** (mapas interativos)
- **Chart.js 4.4.1** (gráficos doughnut e linha)
- **JavaScript vanilla**
- **Server-Sent Events** (notificações em tempo real)

---

### 👥 **Sistema de Usuários e Permissões**

O projeto implementa **3 níveis de acesso**:

1. **Admin** (is_admin=True)
   - Painel administrativo com dashboard, gráficos e KPIs
   - Gerenciamento de denúncias (status, atribuição de empresa, remoção)
   - Gerenciamento de empresas terceirizadas
   - Gestão de usuários (listagem com busca)
   - Exportação de dados (CSV)

2. **Empresa** (company_id vinculado)
   - Dashboard com KPIs e gráficos por status/categoria
   - Filtros e busca nas denúncias atribuídas
   - Resposta a denúncias com comentários e atualização de status
   - Visualização de imagens e localização

3. **Usuário Público (Cidadão)**
   - Criar e visualizar denúncias
   - Usar geolocalização e busca por proximidade
   - Página "Minhas Denúncias" com KPIs pessoais
   - Comentar em denúncias
   - Assistente de chat para consultas

---

### 📁 **Principais Funcionalidades**

**No Backend:**

1. **ReportService** - Criação e gerenciamento de denúncias
   - Salvamento de imagens com UUID único
   - Notificação por e-mail quando status muda
   - Notificação em tempo real via SSE
   - Suporte a múltiplas imagens por denúncia

2. **ReportRepository** - Acesso a dados
   - Filtros avançados (categoria, status, período, busca textual)
   - Paginação reutilizável
   - Contagem diária (últimos 7 dias)
   - Busca por proximidade (Haversine)

3. **NotificationBus** - Notificações em tempo real
   - Pub/sub thread-safe com threading.Lock
   - SSE stream para clientes conectados
   - Toasts ao vivo no frontend

4. **ChatEngine** - Assistente de IA
   - Reconhecimento de intenção por regras
   - Consulta de denúncias e estatísticas
   - Busca textual integrada

5. **RateLimiter** - Proteção contra brute force
   - Rastreamento in-memory por IP
   - 5 tentativas por 300 segundos
   - Reset automático após período

6. **Blueprints Registrados:**
   - `public_bp` - Rotas públicas (home, denúncias, minhas denúncias, API nearby)
   - `auth_bp` - Autenticação/cadastro com rate limiting
   - `admin_bp` - Administração (dashboard, empresas, usuários, exportação)
   - `company_bp` - Gestão empresarial (dashboard, detalhe, resposta)
   - `chat_bp` - Assistente de chat IA
   - `sse_bp` - Stream de notificações SSE

**No Frontend:**

1. **Map Home** - Mapa interativo na página inicial
   - Marcadores de todas as denúncias com coordenadas
   - Botão "Próximas a mim" com geolocalização do navegador
   - Popup com detalhes da denúncia

2. **Map Detail** - Visualização de localização da denúncia
   - Exibição de marcador no mapa
   - Link para Google Maps
   - Centrado nas coordenadas lat/lon

3. **Map Picker** - Seletor de localização ao criar denúncia
   - Clique no mapa para definir coordenadas
   - Geolocalização automática do navegador
   - Integração com OpenStreetMap

4. **Charts** - Visualização de dados
   - Gráfico de linha (últimos 7 dias de denúncias)
   - Gráfico doughnut (por categoria e por status)
   - Cores semânticas: vermelho (Aberta), laranja (Em andamento), verde (Resolvida)

5. **KPI Cards** - Indicadores visuais
   - Ícones Bootstrap Icons
   - Bordas laterais coloridas por status
   - Contagem em tempo real

6. **Navigation** - Menu responsivo com busca
   - Filtro por status (Abertas, Em andamento, Resolvidas)
   - Dropdowns contextuais para admin/empresa
   - Link "Minhas Denúncias" para cidadãos logados
   - Link para assistente de chat

7. **Notificações** - Toasts em tempo real
   - Conecta via SSE ao endpoint `/api/notifications/stream`
   - Toast Bootstrap para novas denúncias e mudanças de status

---

### 🔐 **Segurança Implementada**

- **CSRF protection** via CSRFProtect (todas as rotas POST, incluindo API fetch)
- **Rate limiting** no login (5 tentativas/5 min por IP)
- **Proteção contra open redirect** no login (apenas caminhos relativos aceitos)
- Validação de arquivos por extensão
- Nomes de arquivo sanitizados com `secure_filename`
- UUIDs para nomes únicos de arquivos
- Decoradores para verificação de autenticação e autorização (`@admin_required`, `@company_required`)
- Thread safety no NotificationBus com `threading.Lock`

---

### 🧪 **Testes**

O projeto inclui **30 testes unitários** com pytest:

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Testes por módulo
python -m pytest tests/test_admin.py -v      # Painel admin (5 testes)
python -m pytest tests/test_auth.py -v       # Autenticação (6 testes)
python -m pytest tests/test_chat.py -v       # Chat IA (5 testes)
python -m pytest tests/test_notifications.py -v  # NotificationBus (3 testes)
python -m pytest tests/test_public.py -v     # Rotas públicas (6 testes)
python -m pytest tests/test_rate_limit.py -v # Rate limiter (4 testes)
```

---

### 💾 **Configurações Principais**

```python
MAX_CONTENT_LENGTH = 20 MB  # Limite de upload
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
DATABASE_URL = SQLite (infra_plus.db)
UPLOAD_FOLDER = frontend/static/uploads
SECRET_KEY = configurável via ambiente
RATE_LIMIT = 5 tentativas / 300 segundos
NOTIFICATION_QUEUE = 50 itens por conexão SSE
```

---

## 🔧 Como Rodar o Projeto

### 1. Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
source .venv/bin/activate      # Linux/macOS
.\.venv\Scripts\Activate.ps1   # Windows
```

### 2. Instalação e Configuração
```bash
pip install -r requirements.txt
cp .env.example .env
```

### 3. Execução
```bash
python run.py
```

Acesse: http://127.0.0.1:5000/

**Credenciais padrão:** `admin@infra.plus` / Senha: `123`

### 4. Testes
```bash
python -m pytest tests/ -v
```

---

### ⚙️ Configuração (.env)

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Chave de segurança para criptografia de sessões |
| `DATABASE_URL` | String de conexão com o banco de dados |
| `MAIL_SERVER` | Servidor SMTP para envio de notificações |

---

## 🗺️ Roadmap de Evolução

- [ ] **Alembic:** Implementar migrações de banco de dados
- [x] **Testes Unitários:** Cobertura com pytest (30 testes)
- [x] **Geolocalização avançada:** Busca por proximidade com Haversine
- [x] **Notificações em tempo real:** SSE com toasts ao vivo
- [x] **Assistente de chat:** Chatbot para consultas rápidas
- [x] **Rate limiting:** Proteção contra brute force
- [x] **Gestão de usuários:** Painel admin com listagem e busca
- [ ] **Migração para PostgreSQL:** Banco de dados para produção
- [ ] **Docker:** Ambiente de containerização para deploy
- [ ] **Alembic:** Migrações de banco de dados

<br>

<p align="center">
Projeto Acadêmico - <b>Universidade de Vassouras.</b> 👋 

<br>
<br>


<a href="https://www.linkedin.com/in/richardson-ferreira-464571264" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
&nbsp;
<a href="https://github.com/richaferreira" target="_blank">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>
&nbsp;
  <a href="https://www.instagram.com/richardsonferreira__" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
  </a>
<a><p align="center">
  <img src="https://komarev.com/ghpvc/?username=richaferreira-InfraPlus&color=dc143c&style=for-the-badge&label=Visualizações" alt="Contador de Visitas" />
</p></a>
  
</p>
