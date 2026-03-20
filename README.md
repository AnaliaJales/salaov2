# Salão V2.2 - Sistema de Gerenciamento de Salão de Beleza

Sistema web completo desenvolvido em **Django 6.0.3** para gerenciamento de salão de beleza. Inclui módulos para agendamentos, clientes, profissionais, serviços, relatórios, estoque e usuários.

## 📋 Funcionalidades
- **Agendamentos**: Cadastro e visualização em calendário
- **Clientes**: CRUD completo
- **Profissionais**: Gerenciamento de equipe
- **Serviços**: Cadastro com categorias
- **Relatórios**: Geração de PDFs
- **Estoque**: Controle de produtos
- **Usuários**: Autenticação com perfis (Admin e Recepcionista)

## 🛠️ Pré-requisitos
- Python 3.8+
- Node.js (para assets Bootstrap)
- Git

## 🚀 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd salao
```

### 2. Configurar Ambiente Virtual (Recomendado)
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Criar Arquivo `.env` (obrigatório)
Crie um arquivo `.env` na raiz do projeto:
```
SECRET_KEY=sua_chave_secreta_django_aqui_gerada_com_django-admin-startproject
DEBUG=True
```
> Gere SECRET_KEY em: https://djecrety.ir/

### 4. Instalar Dependências Python
```bash
pip install -r requirements.txt
```

### 5. Instalar Dependências Frontend
```bash
npm install
```

### 6. Aplicar Migrações
```bash
python manage.py migrate
```

### 7. Criar Superusuário (Admin)
```bash
python manage.py createsuperuser
```

### 8. Criar Usuário Recepcionista (Perfil Restrito)
```bash
python manage.py criar_recepcionista nome_usuario
# Exemplo: python manage.py criar_recepcionista recepcionista1
```
> A senha será solicitada interativamente. O usuário terá acesso restrito (sem relatórios/usuários).

### 9. Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### 10. Executar Servidor de Desenvolvimento
```bash
python manage.py runserver
```

### 11. Acessar a Aplicação
- **Home**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/login/

## 🖥️ Estrutura de URLs
| URL | Descrição |
|-----|-----------|
| `/` | Página inicial |
| `/agendamentos/` | Gerenciar agendamentos |
| `/agenda/` | Visualização calendário |
| `/clientes/` | Gerenciar clientes |
| `/profissionais/` | Gerenciar profissionais |
| `/servicos/` | Gerenciar serviços |
| `/relatorios/` | Gerar relatórios |
| `/estoque/` | Gerenciar estoque |

## ⚙️ Configuração para Produção
1. **ALLOWED_HOSTS** em `settings.py`:
   ```
   ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']
   ```
2. `DEBUG = False`
3. Use servidor WSGI (Gunicorn) + Nginx/Apache
4. Configure banco de dados de produção (PostgreSQL/MySQL)
5. HTTPS obrigatório

Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn projeto.wsgi:application --bind 0.0.0.0:8000
```

## 🔧 Comandos Úteis
```bash
# Criar migrações
python manage.py makemigrations

# Verificar status migrações
python manage.py showmigrations

# Shell Django
python manage.py shell

# Testes
python manage.py test
```

## 🐛 Problemas Comuns
- **Static files não carregam**: Execute `collectstatic`
- **Erro SECRET_KEY**: Verifique arquivo `.env`
- **Migrations falham**: `python manage.py migrate --fake-initial`
- **No module named 'apps'**: Verifique `INSTALLED_APPS` em settings.py
- **Recepcionista sem acesso**: Execute `criar_recepcionista` novamente

## 📁 Estrutura do Projeto
```
salao/
├── manage.py
├── requirements.txt
├── package.json
├── db.sqlite3
├── projeto/
│   ├── settings.py
│   └── urls.py
├── apps/          # Aplicações Django
├── core/
├── estoque/
└── templates/
```

## 📄 Licença
Projeto open-source para fins educacionais.

Desenvolvido com ❤️ para gerenciamento eficiente de salões de beleza!

