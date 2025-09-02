from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from utility.response import ApiResponse
from utility.utils import CreateRetrieveUpdateViewSet, get_serielizer_error
from job_app.model.skill import Skill
from job_app.serializers.skill_serializer import SkillSerializer

class SkillView(CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = SkillSerializer
    singular_name = 'Skill'
    model_class = Skill.objects
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """Create a new skill"""
        sp1 = transaction.savepoint()
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(
                    self,
                    data=serializer.data,
                    message=self.singular_name + ' created successfully.'
                )
            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)
        except Exception as e:
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_internal_server_error(self, message=[str(e)])

    def list(self, request, *args, **kwargs):
        """List all skills"""
        try:
            queryset = self.model_class.all().order_by('name')
            data = [ {'id': s.id, 'name': s.name} for s in queryset ]
            return ApiResponse.response_ok(self, data=data)
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e)])
