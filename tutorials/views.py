from django.shortcuts import render
from rest_framework.views import APIView
from .models import Tutorial
from rest_framework.response import Response
from tutorials.serializers import TutorialListSerializer


class Tutorials(APIView):
    def get(self, request):
        all_tutorials = Tutorial.objects.all()
        print("count : ", all_tutorials.count())
        serializer = TutorialListSerializer(all_tutorials, many=True)
        print("serializer length: ", serializer)
        return Response(serializer.data)
    
    def post(self, request):
        print("tutorial posting check")
        serializer = TutorialListSerializer(data=request.data)
        if serializer.is_valid():
            tutorial = serializer.save()
            return Response(TutorialListSerializer(tutorial).data)
        else:
            print("serializer is not valid : ", serializer.errors)
            return Response(serializer.errors)  