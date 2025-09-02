from rest_framework import serializers

class FindPassSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=256)
    otp = serializers.CharField(max_length=256)
