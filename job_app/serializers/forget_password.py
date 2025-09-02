from rest_framework import serializers

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)
