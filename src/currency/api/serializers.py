from rest_framework import serializers


from django.conf import settings


from currency.models import Rate
from account.models import Contact
from account.tasks import send_email_async


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'created',
            'get_currency_display',
            'currency',
            'buy',
            'sale',
            'get_source_display',
            'source',
        )
        extra_kwargs = {
            'currency': {'write_only': True},
            'source': {'write_only': True},
        }


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'created',
            'email',
            'title',
            'text',
        )

    def create(self, validated_data):
        send_email_async.delay(
            validated_data['title'],
            validated_data['text'],
            settings.EMAIL_HOST_USER,
            [validated_data['email'], ]
        )
        return super().create(validated_data)
