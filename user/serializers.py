from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    badges = serializers.SerializerMethodField('_badges')

    def _badges(self, obj):
        return list(obj.award_set.all().values_list('badge__code', flat=True))

    class Meta:
        model = User
        fields = ['username', 'email', 'badges']