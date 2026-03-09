# Templates WhatsApp - Django

## Como enviar templates aprovados

Endpoint: `POST /api/whatsapp/send-template/`

### Exemplo simples (sem variáveis)

```json
{
  "conversation_id": 1,
  "template_name": "hello_world",
  "language_code": "pt_BR"
}
```

### Exemplo com variáveis (body)

```json
{
  "conversation_id": 1,
  "template_name": "appointment_reminder",
  "language_code": "pt_BR",
  "components": [
    {
      "type": "body",
      "parameters": [
        {"type": "text", "text": "Dr. Silva"},
        {"type": "text", "text": "10/03/2026"},
        {"type": "text", "text": "14:30"}
      ]
    }
  ]
}
```

### Exemplo com botões

```json
{
  "conversation_id": 1,
  "template_name": "confirm_appointment",
  "language_code": "pt_BR",
  "components": [
    {
      "type": "body",
      "parameters": [
        {"type": "text", "text": "Rex"},
        {"type": "text", "text": "10/03/2026 às 14:30"}
      ]
    },
    {
      "type": "button",
      "sub_type": "quick_reply",
      "index": "0",
      "parameters": [
        {"type": "payload", "payload": "confirm_yes"}
      ]
    }
  ]
}
```

## Templates úteis para clínica veterinária

### 1. Lembrete de consulta
**Nome**: `appointment_reminder`
**Variáveis**: `{{1}}` nome do veterinário, `{{2}}` data, `{{3}}` hora

### 2. Confirmação de agendamento
**Nome**: `appointment_confirmation`
**Variáveis**: `{{1}}` nome do pet, `{{2}}` tipo de consulta, `{{3}}` data/hora

### 3. Resultado de exame disponível
**Nome**: `exam_ready`
**Variáveis**: `{{1}}` nome do tutor, `{{2}}` nome do pet

### 4. Lembrete de vacina
**Nome**: `vaccine_reminder`
**Variáveis**: `{{1}}` nome do pet, `{{2}}` tipo de vacina, `{{3}}` data limite

### 5. Aniversário do pet
**Nome**: `pet_birthday`
**Variáveis**: `{{1}}` nome do pet, `{{2}}` idade

## Resposta de sucesso

```json
{
  "success": true,
  "message_id": 123,
  "external_id": "wamid.HBgNNTU...",
  "whatsapp_response": {
    "messaging_product": "whatsapp",
    "contacts": [...],
    "messages": [...]
  }
}
```

## Notas importantes

- Templates devem estar aprovados pela Meta antes do uso
- Language code padrão: `pt_BR`
- Índices de botão começam em `0`
- Parâmetros de corpo seguem ordem `{{1}}`, `{{2}}`, etc.
