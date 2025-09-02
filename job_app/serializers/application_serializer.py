from rest_framework import serializers
from job_app.model.application import Application
from job_app.model.job import Job
from job_app.model.users import User

class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    applicant = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=3))
    resume = serializers.FileField(required=True)

    class Meta:
        model = Application
        fields = '__all__'
