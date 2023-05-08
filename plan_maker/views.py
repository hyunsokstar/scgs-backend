from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LongTermPlanSerializer
from .models import LongTermPlan


class LongTermPlanListAPIView(APIView):
    def get(self, request):
        plans = LongTermPlan.objects.all()
        serializer = LongTermPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        writer = request.user
        print("writer : ", writer)

        data = request.data
        serializer = LongTermPlanSerializer(data=data, context={'writer': writer})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)