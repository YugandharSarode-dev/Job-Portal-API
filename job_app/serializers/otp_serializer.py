from rest_framework import serializers
from ..models import OTP

class OTPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OTP
        fields = ("email", )
