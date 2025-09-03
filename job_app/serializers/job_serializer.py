from rest_framework import serializers
from job_app.model.job import Job
from job_app.model.skill import Skill
from job_app.model.users import User

class JobSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    posted_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=2))

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value
    
    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty")
        return value


    class Meta:
        model = Job
        fields = '__all__'
        