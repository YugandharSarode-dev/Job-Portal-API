from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    new_otp = serializers.IntegerField()
    email = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)
    confirm_password = serializers.CharField(max_length=256)
