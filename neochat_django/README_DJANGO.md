# NEOCHAT Django (Reinicio do zero)

Base inicial do omnichannel para clinica veterinaria usando Django + DRF + JWT.

## O que ja esta pronto
- Projeto Django configurado
- Usuario customizado com roles (admin, veterinario, atendente, recepcao)
- Modelos principais: Conversation e Message
- API REST com autenticacao JWT
- Endpoints para auth, conversas e mensagens
- Admin Django configurado
- Frontend inicial com Django Templates (login + dashboard)
- Chat em tempo real com Django Channels (WebSocket por conversa)
- Integracao WhatsApp Business API (webhook + envio + status)

## Como rodar
```powershell
cd neochat_django
C:/Users/Samsung/Desktop/NEOCHAT/.venv/Scripts/python.exe manage.py migrate
C:/Users/Samsung/Desktop/NEOCHAT/.venv/Scripts/python.exe manage.py createsuperuser
C:/Users/Samsung/Desktop/NEOCHAT/.venv/Scripts/python.exe manage.py runserver
```

Depois, acesse:
- `http://127.0.0.1:8000/login/` para entrar no frontend
- `http://127.0.0.1:8000/` para dashboard e chat

## Endpoints principais
- `GET /health/`
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`
- `GET|POST /api/conversations/`
- `GET|POST /api/messages/`
- `GET|POST /api/whatsapp/webhook/`
- `POST /api/whatsapp/send-template/` (enviar templates aprovados)
- `WS /ws/conversations/<conversation_id>/`

## Exemplo de login
```json
{
  "username": "admin",
  "password": "sua_senha"
}
```

A resposta retorna `access` e `refresh` para uso no header:
`Authorization: Bearer <token>`
