from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LongTermPlanSerializer
from .models import LongTermPlan


class LongTermPlanListAPIView(APIView):
    def get(self, request):
        plans = LongTermPlan.objects.all()
        serializer = LongTermPlanSerializer(plans, many=True)
        return Response(serializer.data)
