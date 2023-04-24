from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudyNote, StudyNoteContent
from .serializers import StudyNoteSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
import random


class StudyNoteAPIView(APIView):
    def get(self, request):
        study_notes = StudyNote.objects.all()
        serializer = StudyNoteSerializer(study_notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudyNoteSerializer(data=request.data)

        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudyNoteDetailView(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        api_docu = self.get_object(pk)
        api_docu.delete()

        return Response(status=HTTP_204_NO_CONTENT)

class AddDummyDataForStudyNote(APIView):
    def post(self, request):
        for i in range(10):
            title = f"Dummy Note {i+1}"
            description = f"This is a dummy note with index {i+1}"
            StudyNote.objects.create(title=title, description=description)
        return Response({"message": "Dummy data added successfully."})
    
class StudyNoteContentDummyAPI(APIView):
    def post(self, request):
        study_notes = StudyNote.objects.all()
        print("study_notes :" , study_notes)

        for i in range(5):
            study_note_obj = random.choice(study_notes)

            if study_note_obj:
                StudyNoteContent.objects.create(
                    title=f"dummy title {i}",
                    content=f"dummy content {i}",
                    writer=request.user,
                    study_note=study_note_obj,
                    # created_at=datetime.now() - timedelta(days=i),
            )
        return Response({"message": "Dummy data created successfully."})    