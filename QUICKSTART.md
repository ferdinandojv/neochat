# 🚀 Início Rápido - NeoChat Django

## Comandos essenciais

### 1. Ativar ambiente virtual (Windows)
```powershell
C:/Users/Samsung/Desktop/NEOCHAT/.venv/Scripts/Activate.ps1
```

### 2. Entrar no projeto Django
```powershell
cd neochat_django
```

### 3. Rodar migrações (primeira vez)
```powershell
python manage.py migrate
```

### 4. Criar superusuário (primeira vez)
```powershell
python manage.py createsuperuser
```

### 5. Iniciar servidor
```powershell
python manage.py runserver
```

### 6. Acessar aplicação
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 📋 Checklist de configuração

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Migrações executadas (`python manage.py migrate`)
- [ ] Superusuário criado
- [ ] Servidor rodando

## 🔧 Configuração WhatsApp (opcional)

1. Criar `.env` em `neochat_django/`:
```env
WHATSAPP_PHONE_NUMBER_ID=seu_id
WHATSAPP_ACCESS_TOKEN=seu_token
WHATSAPP_WEBHOOK_VERIFY_TOKEN=seu_verify_token
WHATSAPP_APP_SECRET=seu_secret
```

2. Consultar `neochat_django/WHATSAPP_DJANGO_SETUP.md` para detalhes

## 📚 Documentação completa
- [README Principal](README.md)
- [Guia Django](neochat_django/README_DJANGO.md)
- [WhatsApp Setup](neochat_django/WHATSAPP_DJANGO_SETUP.md)
- [WhatsApp Templates](neochat_django/WHATSAPP_TEMPLATES_DJANGO.md)
