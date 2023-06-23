from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import (
    StudyNote,
    StudyNoteContent,
    CoWriterForStudyNote,
    StudyNoteBriefingBoard,
    ClassRoomForStudyNote,
    QnABoard
)

# 1122


class QnABoardSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = QnABoard
        fields = ['pk', 'study_note', 'title', 'content', 'page',
                  'writer', 'created_at_formatted', 'updated_at']

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()


class CreateCommentSerializerForNote(serializers.ModelSerializer):
    class Meta:
        model = StudyNoteBriefingBoard
        fields = (
            "note",
            "comment",
        )


class ClassRoomForStudyNoteSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = ClassRoomForStudyNote
        fields = ['id', 'current_note', 'current_page',
                  'writer', 'is_approved', 'created_at_formatted']

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()


class StudyNoteBriefingBoardSerializer(serializers.ModelSerializer):
    # created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNoteBriefingBoard
        fields = ('id', 'note', 'writer', 'comment', 'like_count',
                  'created_at', 'updated_at', 'is_edit_mode', 'created_at_formatted')
        read_only_fields = ('id', 'created_at', 'updated_at')


class CoWriterForStudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CoWriterForStudyNote
        fields = ('id', 'writer', 'study_note', 'is_approved', 'created_at')


# class StudyNoteSerializer(serializers.ModelSerializer):
#     writer = UserProfileImageSerializer(read_only=True)
#     note_cowriters = CoWriterForStudyNoteSerializer(many=True)
#     count_for_note_contents = serializers.SerializerMethodField()

#     class Meta:
#         model = StudyNote
#         fields = ['pk', 'title', 'description',
#                   'writer', 'count_for_note_contents', 'note_cowriters']

#     def get_count_for_note_contents(self, obj):
#         return obj.note_contents.count()
class StudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    note_cowriters = CoWriterForStudyNoteSerializer(many=True, required=False)
    count_for_note_contents = serializers.SerializerMethodField()
    count_for_note_comments = serializers.SerializerMethodField()

    class Meta:
        model = StudyNote
        fields = [
            'pk',
            'title',
            'description',
            'writer',
            'count_for_note_contents',
            'note_cowriters',
            'count_for_note_comments',
            'first_category',
            'second_category'
        ]

    def get_count_for_note_contents(self, obj):
        return obj.note_contents.count()

    def get_count_for_note_comments(self, obj):
        return obj.note_comments.count()


class StudyNoteContentSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNoteContent
        fields = [
            'pk',
            'page',
            'title',
            'file_name',
            'content',
            'content_option',
            'ref_url1',
            'ref_url2',
            'youtube_url',
            'writer',
            'created_at',
            'order'
        ]
        read_only_fields = ['id', 'created_at']


class SerializerForCreateQuestionForNote(serializers.ModelSerializer):
    class Meta:
        model = QnABoard
        fields = (
            "study_note",
            "title",
            "content",
            "page"
        )
