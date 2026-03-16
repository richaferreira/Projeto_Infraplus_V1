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
- **Geolocalização**: Sistema de mapa interativo (Leaflet)
- **Gestão de empresas** terceirizadas para resolução
- **Painel administrativo** para monitoramento
- **Upload de imagens** para evidências

---

## 🚀 Funcionalidades Ativas

* ✅ **Reporte com Anexos:** Registro de problemas com localização e múltiplos uploads de fotos.
* ✅ **Painel Administrativo:** Gestão centralizada de chamados com filtros avançados e paginação.
* ✅ **Gestão de empresas:** Cria empresas terceirizadas para resolução.
* ✅ **Comentários Automáticos:** Logs de interação identificando automaticamente o usuário logado.
* ✅ **Geolocalização:** Sistema de mapa interativo (Leaflet).

<br>

## 📂 Estrutura do Projeto

A organização do projeto segue o padrão **MVC** (Model-View-Controller) aliado ao **Repository Pattern**:




```bash
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
### 📋 **Informações Gerais**
- **Nome**: Projeto Infraplus (InfraPlus — Águas Seguras)
- **Descrição**: Projeto InflaPlus
- **Licença**: Apache License 2.0
- **Criado em**: 4 de março de 2023
- **Visibilidade**: Público
- **Linguagens**:
  - HTML: 53.6%
  - Python: 40.3%
  - JavaScript: 4.7%
  - Other: 1.4%

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

🔧 Como Rodar o Projeto
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
source .venv/bin/activate      # Linux/macOS
.\.venv\Scripts\Activate.ps1   # Windows
```
2. Instalação e Configuração
```bash
pip install -r requirements.txt
cp .env.example .env
```
3. Execução
```bash
python run.py
```
Acesse: http://127.0.0.1:5000/ | Admin Seed: admin@infra.plus / Senha: 123

⚙️ Configuração (.env)
```bash
Variável,Descrição
SECRET_KEY,Chave de segurança para criptografia de sessões.
DATABASE_URL,String de conexão com o banco de dados.
MAIL_SERVER,Servidor SMTP para envio de notificações.
```



🗺️ Roadmap de Evolução

[ ] Alembic: Implementar migrações de banco de dados.

[ ] Testes Unitários: Adicionar cobertura com pytest.

[ ] Geocodificação: Integrar API para converter endereços em coordenadas reais.

[ ] Docker: Criar ambiente de containerização para deploy.

<br>




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
