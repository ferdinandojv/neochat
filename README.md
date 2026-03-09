# NeoChat - Sistema Omnichannel Django

Sistema de atendimento omnichannel para clínica veterinária desenvolvido com **Django**, **Django REST Framework** e **Django Channels** (WebSocket).

## 🚀 Tecnologias

- **Backend**: Django 6.0, Django REST Framework, Django Channels
- **Autenticação**: JWT (Simple JWT) + Session Auth
- **Tempo Real**: WebSocket via Django Channels
- **Banco de Dados**: SQLite (dev) / PostgreSQL (prod)
- **Integrações**: WhatsApp Business API (Meta Cloud API)

## 📋 Funcionalidades

✅ Autenticação de usuários com perfis (admin, veterinário, atendente, recepção)  
✅ Gestão de conversas multicanal (WhatsApp, Email, SMS, Web, Telegram, Phone)  
✅ Chat em tempo real com WebSocket  
✅ Integração completa com WhatsApp Business API:
  - Receber mensagens via webhook
  - Enviar mensagens de texto automaticamente
  - Enviar templates aprovados
  - Rastreamento de status (enviado, entregue, lido)  
✅ Interface web com Django Templates  
✅ API REST completa  
✅ Painel administrativo Django  

## 🛠️ Instalação

### Pré-requisitos
- Python 3.13+
- Ambiente virtual Python

### Passo a passo

```powershell
# 1. Entre no diretório do projeto Django
cd neochat_django

# 2. Ative o ambiente virtual (já configurado)
# No Windows PowerShell:
C:/Users/Samsung/Desktop/NEOCHAT/.venv/Scripts/Activate.ps1

# 3. Instale as dependências (se necessário)
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py migrate

# 5. Crie um superusuário
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver
```

## 🌐 Acesso

- **Dashboard**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Admin**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/
- **Health Check**: http://127.0.0.1:8000/health/

## 📱 Integração WhatsApp

Consulte a documentação completa em:
- `neochat_django/WHATSAPP_DJANGO_SETUP.md` - Configuração inicial
- `neochat_django/WHATSAPP_TEMPLATES_DJANGO.md` - Uso de templates

### Configuração rápida

Crie um arquivo `.env` em `neochat_django/` baseado em `.env.example` e adicione:

```env
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_ACCESS_TOKEN=seu_access_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=seu_verify_token
WHATSAPP_APP_SECRET=seu_app_secret
```

## 📚 Documentação

- **README Principal**: Este arquivo
- **Guia Django**: `neochat_django/README_DJANGO.md`
- **WhatsApp Setup**: `neochat_django/WHATSAPP_DJANGO_SETUP.md`
- **WhatsApp Templates**: `neochat_django/WHATSAPP_TEMPLATES_DJANGO.md`

## 🔌 API Endpoints

### Autenticação
- `POST /api/auth/register/` - Registro de usuário
- `POST /api/auth/login/` - Login (retorna JWT)
- `POST /api/auth/refresh/` - Renovar token
- `GET /api/auth/me/` - Dados do usuário autenticado
- `GET /api/auth/users/` - Listar usuários

### Conversas
- `GET /api/conversations/` - Listar conversas
- `POST /api/conversations/` - Criar conversa
- `GET /api/conversations/<id>/` - Detalhes
- `PATCH /api/conversations/<id>/` - Atualizar
- `DELETE /api/conversations/<id>/` - Deletar

### Mensagens
- `GET /api/messages/?conversation=<id>` - Listar mensagens de uma conversa
- `POST /api/messages/` - Enviar mensagem

### WhatsApp
- `GET /api/whatsapp/webhook/` - Verificação Meta
- `POST /api/whatsapp/webhook/` - Receber eventos
- `POST /api/whatsapp/send-template/` - Enviar template aprovado

### WebSocket
- `WS /ws/conversations/<conversation_id>/` - Chat em tempo real

## 🏗️ Estrutura do Projeto

```
neochat_django/
├── accounts/           # Autenticação e usuários
├── conversations/      # Gestão de conversas
├── messaging/          # Mensagens e WebSocket
├── dashboard/          # Interface web (templates)
├── whatsapp/           # Integração WhatsApp
├── neochat_django/     # Configurações principais
├── templates/          # Templates HTML
├── static/             # CSS, JS, imagens
├── manage.py
├── requirements.txt
└── README_DJANGO.md
```

## 👥 Perfis de Usuário

- **admin**: Acesso total ao sistema
- **veterinario**: Atendimento e relatórios
- **atendente**: Chat e gestão de conversas
- **recepcao**: Atendimento básico e agendamentos

## 🔐 Segurança

- Autenticação JWT para API
- Session Auth para interface web
- CSRF Protection
- Validação de webhook WhatsApp (signature)
- Permissões por role

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação interna ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com Django 6.0** 🐍
