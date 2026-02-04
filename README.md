# 💧 InfraPlus - Gestão de Infraestrutura Hídrica - Projeto Acadêmico.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  
</p>

<br>

## 📌 Sobre o Projeto

O **InfraPlus** é uma plataforma web desenvolvida para otimizar o reporte e a gestão de problemas relacionados à rede de água (vazamentos, falta de abastecimento, manutenção). O objetivo é conectar o cidadão aos órgãos responsáveis de forma ágil, permitindo um monitoramento eficiente da infraestrutura urbana.

> [!IMPORTANT]
> **Diferencial Técnico:** O projeto utiliza uma arquitetura baseada em **Camadas e Repositórios**, separando rigorosamente as responsabilidades (SOC) e facilitando a manutenção e a escalabilidade do software.


## 🚀 Funcionalidades Principais

* ✅ **Reporte com Anexos:** Registro de problemas com localização e múltiplos uploads de fotos.
* ✅ **Painel Administrativo:** Gestão centralizada de chamados com filtros avançados e paginação.
* ✅ **Comentários Automáticos:** Logs de interação identificando automaticamente o usuário logado.
* ✅ **Notificações:** Sistema de e-mail integrado para atualizações de status em tempo real.

<br>

## 📂 Estrutura do Projeto

A organização do projeto segue o padrão **MVC** (Model-View-Controller) aliado ao **Repository Pattern**:




```bash
InfraPlus_AguasSeguras/
├─ backend/app/
│  ├─ blueprints/     # Rotas divididas por contexto (Admin, Auth, Public)
│  ├─ models/         # Definição das tabelas (SQLAlchemy)
│  ├─ services/       # Lógica de negócio e notificações
│  ├─ repositories/   # Consultas ao banco, filtros e paginação
│  └─ forms/          # Validações de formulários (WTForms)
├─ frontend/
│  ├─ templates/      # Páginas HTML (Jinja2)
│  └─ static/         # CSS, JS e diretório de Uploads
└─ run.py             # Ponto de entrada da aplicação
```
🛠️ Tecnologias Utilizadas

Linguagem: Python 3.x

Framework Web: Flask

Banco de Dados: SQLite (Desenvolvimento) / Suporte a PostgreSQL e MySQL

Segurança: Variáveis de ambiente (.env) e validação rigorosa de e-mails.

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



🤝 Contribuição e Comunidade
Quer ajudar o projeto a crescer e ainda ganhar Achievements no seu perfil?

Issues: Confira nossas Good First Issues para começar a contribuir.

Guia: Antes de enviar um Pull Request, leia o nosso arquivo CONTRIBUTING.md.

<br>

<p align="center">
Desenvolvido por <b>Richardson Ferreira</b> 👋 




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
