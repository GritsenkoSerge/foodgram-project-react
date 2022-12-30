from django.contrib.auth import get_user_model
from djoser import serializers
from djoser.conf import settings

User = get_user_model()


class UserSerializer(serializers.UserSerializer):
    class Meta(serializers.UserSerializer.Meta):
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "is_subscribed",
        )
