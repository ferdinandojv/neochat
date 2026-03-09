import hashlib
import hmac
import os
from typing import Any

import requests


class WhatsAppService:
    def __init__(self) -> None:
        self.api_version = os.getenv("WHATSAPP_API_VERSION", "v22.0")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.verify_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "")
        self.app_secret = os.getenv("WHATSAPP_APP_SECRET", "")

    @property
    def enabled(self) -> bool:
        return bool(self.phone_number_id and self.access_token)

    @property
    def webhook_verify_token(self) -> str:
        return self.verify_token

    def normalize_phone(self, phone: str) -> str:
        digits = "".join(ch for ch in phone if ch.isdigit())
        if not digits:
            return ""
        if digits.startswith("00"):
            return digits[2:]
        return digits

    def send_text_message(self, to_phone: str, text: str) -> dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("WhatsApp nao configurado no ambiente.")

        normalized_phone = self.normalize_phone(to_phone)
        if not normalized_phone:
            raise RuntimeError("Telefone do cliente ausente ou invalido.")

        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": normalized_phone,
            "type": "text",
            "text": {"body": text},
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()

    def send_template_message(
        self,
        to_phone: str,
        template_name: str,
        language_code: str = "pt_BR",
        components: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("WhatsApp nao configurado no ambiente.")

        normalized_phone = self.normalize_phone(to_phone)
        if not normalized_phone:
            raise RuntimeError("Telefone do cliente ausente ou invalido.")

        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        
        template_payload = {
            "name": template_name,
            "language": {"code": language_code},
        }
        
        if components:
            template_payload["components"] = components

        payload = {
            "messaging_product": "whatsapp",
            "to": normalized_phone,
            "type": "template",
            "template": template_payload,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()

    def verify_signature(self, raw_body: bytes, signature_header: str | None) -> bool:
        if not self.app_secret:
            return True
        if not signature_header or not signature_header.startswith("sha256="):
            return False

        expected = hmac.new(
            self.app_secret.encode("utf-8"),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()
        provided = signature_header.replace("sha256=", "", 1)
        return hmac.compare_digest(expected, provided)
