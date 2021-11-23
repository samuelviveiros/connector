from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Creator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CreatorSerializer(serializers.ModelSerializer):
    #created_by = UserSerializer(required=False)

    class Meta:
        model = Creator
        # fields = ('id', 'name', 'phone', 'created_at', 'updated_at', 'created_by')
        # read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')
        fields = ('id', 'name', 'phone', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):

        request = self.context.get('request', None)
        if request:
            validated_data['created_by'] = request.user

        instance = Creator(**validated_data)
        instance.save()

        return instance
