## Análise do Projeto Infraplus

### 📋 **Informações Gerais**
- **Nome**: Projeto Infraplus (InfraPlus — Águas Seguras)
- **Descrição**: Projeto InflaPlus
- **Licença**: Apache License 2.0
- **Criado em**: 31 de outubro de 2025
- **Último push**: 4 de fevereiro de 2026
- **Visibilidade**: Público
- **Linguagens**:
  - HTML: 53.6%
  - Python: 40.3%
  - JavaScript: 4.7%
  - Other: 1.4%

---

### 🏗️ **Arquitetura do Projeto**

O projeto é uma aplicação **web full-stack** com estrutura:

```
├── backend/
│   └── app/
│       ├── __init__.py (inicialização Flask)
│       ├── config.py (configurações)
│       ├── models/ (modelos de dados)
│       ├── services/ (lógica de negócios)
│       ├── blueprints/
│       │   ├── public/ (rotas públicas)
│       │   ├── auth/ (autenticação)
│       │   ├── admin/ (painel administrativo)
│       │   └── company/ (gerenciamento de empresas)
│       └── utils.py (utilitários)
├── frontend/
│   ├── templates/ (HTML templates)
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/
└── run.py (entrada da aplicação)
```

---

### 🎯 **Propósito da Aplicação**

**InfraPlus — Águas Seguras** é um sistema de **denúncias sobre infraestrutura hídrica** que permite:

- **Criar denúncias** sobre problemas de água/saneamento
- **Visualizar denúncias** abertas, em andamento ou resolvidas
- **Geolocalização**: Sistema de mapa interativo (Leaflet)
- **Gestão de empresas** terceirizadas para resolução
- **Painel administrativo** para monitoramento
- **Upload de imagens** para evidências

---

### 🔧 **Stack Tecnológico**

**Backend:**
- **Flask** (framework web Python)
- **Flask-SQLAlchemy** (ORM para banco de dados)
- **Flask-Login** (autenticação de usuários)
- **Flask-Mail** (envio de e-mails)
- **WTForms** (processamento de formulários)
- **SQLite** (banco de dados padrão)

**Frontend:**
- **HTML5** com Jinja2 templates
- **Bootstrap 5.3.2** (UI framework)
- **Leaflet.js** (mapas interativos)
- **Chart.js** (gráficos)
- **JavaScript vanilla**

---

### 👥 **Sistema de Usuários e Permissões**

O projeto implementa **3 níveis de acesso**:

1. **Admin** (is_admin=True)
   - Painel administrativo
   - Gerenciamento de empresas terceirizadas
   - Exportação de dados (CSV)

2. **Empresa** (company_id vinculado)
   - Dashboard próprio
   - Gerenciamento de denúncias atribuídas

3. **Usuário Público**
   - Criar e visualizar denúncias
   - Usar geolocalização

**Credenciais padrão de admin:**
- Email: admin@infra.plus
- Senha: 123

---

### 📁 **Principais Funcionalidades**

**No Backend:**

1. **ReportService** - Criação e gerenciamento de denúncias
   - Salvamento de imagens com UUID único
   - Notificação por e-mail quando status muda
   - Suporte a múltiplas imagens por denúncia

2. **Utils** - Funções auxiliares
   - Validação de uploads (apenas .png, .jpg, .jpeg, .gif)
   - Decoradores para controle de acesso (@admin_required, @company_required)
   - Funções de segurança de arquivo

3. **Blueprints Registrados:**
   - public_bp - Rotas públicas
   - auth_bp - Autenticação/cadastro
   - admin_bp - Administração
   - company_bp - Gestão empresarial

**No Frontend:**

1. **Map Picker** - Seletor de localização interativo
   - Clique no mapa para definir coordenadas
   - Geolocalização automática do navegador
   - Integração com OpenStreetMap

2. **Map Detail** - Visualização de localização da denúncia
   - Exibição de marcador no mapa
   - Centrado nas coordenadas lat/lon

3. **Charts** - Visualização de dados
   - Gráfico de linha (últimos 7 dias de denúncias)
   - Gráfico de pizza (denúncias por categoria)

4. **Navigation** - Menu responsivo com busca
   - Filtro por status (Abertas, Em andamento, Resolvidas)
   - Dropdowns contextuais para admin/empresa

---

### 🔐 **Segurança Implementada**

- CSRF protection via CSRFProtect
- Validação de arquivos por extensão
- Nomes de arquivo sanitizados com secure_filename
- UUIDs para nomes únicos de arquivos
- Decoradores para verificação de autenticação e autorização

---

### 💾 **Configurações Principais**

```python
MAX_CONTENT_LENGTH = 20 MB  # Limite de upload
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
DATABASE_URL = SQLite (infra_plus.db)
UPLOAD_FOLDER = frontend/static/uploads
SECRET_KEY = configurável via ambiente
```

---

### 📌 **Observações**

- O projeto está em desenvolvimento ativo (último commit há 13 dias)
- Sem problemas abertos atualmente
- Fácil de expandir com novos blueprints e serviços
- Estrutura clean e organizada para manutenção