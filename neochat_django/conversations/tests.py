from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Conversation


User = get_user_model()


class ConversationPermissionsTests(APITestCase):
	def setUp(self):
		self.admin = User.objects.create_user(username="admin", password="pass123", role="admin")
		self.agent_1 = User.objects.create_user(username="agent1", password="pass123", role="atendente")
		self.agent_2 = User.objects.create_user(username="agent2", password="pass123", role="atendente")

		self.conv_agent_1 = Conversation.objects.create(
			customer_name="Cliente A",
			channel=Conversation.CHANNEL_WHATSAPP,
			status=Conversation.STATUS_OPEN,
			assigned_to=self.agent_1,
			created_by=self.agent_1,
		)
		self.conv_agent_2 = Conversation.objects.create(
			customer_name="Cliente B",
			channel=Conversation.CHANNEL_WHATSAPP,
			status=Conversation.STATUS_OPEN,
			assigned_to=self.agent_2,
			created_by=self.agent_2,
		)

	def test_agent_only_lists_own_conversations(self):
		self.client.force_authenticate(user=self.agent_1)
		response = self.client.get("/api/conversations/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		ids = {item["id"] for item in response.data}
		self.assertIn(self.conv_agent_1.id, ids)
		self.assertNotIn(self.conv_agent_2.id, ids)

	def test_assigned_agent_can_transfer_conversation(self):
		self.client.force_authenticate(user=self.agent_1)
		url = f"/api/conversations/{self.conv_agent_1.id}/transfer/"

		response = self.client.post(
			url,
			{"assigned_to": self.agent_2.id, "reason": "Troca de turno"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.conv_agent_1.refresh_from_db()
		self.assertEqual(self.conv_agent_1.assigned_to_id, self.agent_2.id)
		history = self.conv_agent_1.metadata.get("transfer_history", [])
		self.assertTrue(history)
		self.assertEqual(history[-1]["by"], self.agent_1.username)

	def test_not_assigned_agent_cannot_transfer_conversation(self):
		self.client.force_authenticate(user=self.agent_1)
		url = f"/api/conversations/{self.conv_agent_2.id}/transfer/"

		response = self.client.post(
			url,
			{"assigned_to": self.agent_1.id, "reason": "Tentativa invalida"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.conv_agent_2.refresh_from_db()
		self.assertEqual(self.conv_agent_2.assigned_to_id, self.agent_2.id)

	def test_admin_can_transfer_any_conversation(self):
		self.client.force_authenticate(user=self.admin)
		url = f"/api/conversations/{self.conv_agent_2.id}/transfer/"

		response = self.client.post(
			url,
			{"assigned_to": self.agent_1.id, "reason": "Rebalanceamento"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.conv_agent_2.refresh_from_db()
		self.assertEqual(self.conv_agent_2.assigned_to_id, self.agent_1.id)
