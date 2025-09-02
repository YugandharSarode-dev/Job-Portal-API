from rest_framework import serializers

class LoginOtpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    otp = serializers.CharField(max_length=256)
