# WhatsApp no Django (Passo 3)

## 1) Configurar variaveis no `.env`

```env
WHATSAPP_API_VERSION=v22.0
WHATSAPP_PHONE_NUMBER_ID=SEU_PHONE_NUMBER_ID
WHATSAPP_ACCESS_TOKEN=SEU_ACCESS_TOKEN
WHATSAPP_WEBHOOK_VERIFY_TOKEN=SEU_TOKEN_DE_VERIFICACAO
WHATSAPP_APP_SECRET=SEU_APP_SECRET
```

## 2) Configurar webhook na Meta

URL do webhook:
`https://SEU_DOMINIO/api/whatsapp/webhook/`

Verify token:
`WHATSAPP_WEBHOOK_VERIFY_TOKEN`

## 3) Fluxo implementado

- Mensagem recebida no WhatsApp -> webhook cria/atualiza conversa em `Conversation` (canal `whatsapp`)
- Mensagem recebida vira `Message` com `sender_type=customer`
- Mensagem enviada pelo atendente via `/api/messages/` em conversa WhatsApp -> enviada automaticamente para Meta API
- Status de entrega/leitura atualiza `Message.external_status` e `Message.is_read`

## 4) Endpoints

- Verificacao webhook: `GET /api/whatsapp/webhook/`
- Eventos webhook: `POST /api/whatsapp/webhook/`

## 5) Teste rapido

1. Crie uma conversa com `channel=whatsapp` e `customer_phone` valido.
2. Envie uma mensagem no dashboard.
3. Verifique no banco os campos `external_id` e `external_status` da `Message`.
4. Envie mensagem de um numero de teste para o seu WhatsApp Business e confirme criacao automatica da conversa.
