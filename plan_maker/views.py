from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LongTermPlanSerializer, LongTermPlanContentsSerializer
from .models import LongTermPlan, LongTermPlanContents
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class LongTermPlanContentsUpdateView(APIView):
    def put(self, request):
        try:
            # Get the data from request body
            contents_data_for_checked = request.data.get(
                "checkedRowsForUpdate")
            print("contents_data_for_checked : ", contents_data_for_checked)

            # Loop through the data and update each row
            for row_data in contents_data_for_checked:
                row_id = row_data.get("id")
                if row_id:
                    print("실행 확인 1111111111111")
                    row = LongTermPlanContents.objects.get(id=row_id)
                else:
                    print("실행 확인 22222222222222")
                    try:
                        long_term_plan = LongTermPlan.objects.get(id=row_data["long_term_plan"])
                    except ObjectDoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)                    
                    row = LongTermPlanContents(
                        long_term_plan=long_term_plan,
                        start=row_data["start"],
                        end=row_data["end"],
                        name=row_data["name"],
                        progress=row_data["progress"],
                        displayOrder=row_data["displayOrder"],
                        dependencies=row_data["dependencies"],
                    )

                row.start = row_data["start"]
                row.end = row_data["end"]
                row.name = row_data["name"]
                row.progress = row_data["progress"]
                row.displayOrder = row_data["displayOrder"]
                row.dependencies = row_data["dependencies"]
                row.full_clean()
                row.save()

            # Return success response
            return Response(status=status.HTTP_200_OK)

        except (LongTermPlanContents.DoesNotExist, ValidationError):
            # If the row with the specified ID does not exist, return a 404 error
            return Response(status=status.HTTP_404_NOT_FOUND)


class LongTermPlanContentsView(APIView):
    def get(self, request, pk, format=None):
        try:
            long_term_plan = LongTermPlan.objects.get(pk=pk)

            print("long_term_plan : ", long_term_plan)

            contents = LongTermPlanContents.objects.filter(
                long_term_plan=long_term_plan)
            serializer = LongTermPlanContentsSerializer(contents, many=True)
            return Response(serializer.data)
        except LongTermPlan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LongTermPlanDetailView(APIView):
    def get_object(self, pk):
        try:
            return LongTermPlan.objects.get(pk=pk)
        except LongTermPlan.DoesNotExist:
            raise status.NOT_FOUND

    def delete(self, request, pk):
        plan_obj = self.get_object(pk)
        plan_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LongTermPlanListAPIView(APIView):
    def get(self, request):
        plans = LongTermPlan.objects.all()
        serializer = LongTermPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        writer = request.user
        print("writer : ", writer)

        data = request.data
        serializer = LongTermPlanSerializer(
            data=data, context={'writer': writer})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
