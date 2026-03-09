from rest_framework import serializers


class SendTemplateSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField(required=True)
    template_name = serializers.CharField(required=True, max_length=200)
    language_code = serializers.CharField(required=False, default="pt_BR", max_length=10)
    components = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True,
    )
