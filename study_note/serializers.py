from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import (
    StudyNote,
    StudyNoteContent,
    CoWriterForStudyNote,
    StudyNoteBriefingBoard,
    ClassRoomForStudyNote,
    AnswerForQaBoard,
    ErrorReportForStudyNote,
    QnABoard,
    FAQBoard,
    CommentForErrorReport,
    Suggestion,
    CommentForSuggestion,
    CommentForFaqBoard,
    RoadMap,
    RoadMapContent
)
from django.utils import timezone  # timezone 모듈 임포트

# 1122


class CoWriterForStudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CoWriterForStudyNote
        fields = ('id', 'writer', 'study_note', 'is_approved', 'created_at')


class StudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    note_cowriters = CoWriterForStudyNoteSerializer(many=True, required=False)
    count_for_note_contents = serializers.SerializerMethodField()
    total_count_for_subtitle = serializers.SerializerMethodField()
    total_count_for_comments = serializers.SerializerMethodField()
    total_count_for_qna_board = serializers.SerializerMethodField()
    total_count_for_faq_list = serializers.SerializerMethodField()
    total_count_for_suggestion_list = serializers.SerializerMethodField()
    total_count_for_class_list = serializers.SerializerMethodField()
    total_count_for_error_report_list = serializers.SerializerMethodField()

    class Meta:
        model = StudyNote
        fields = [
            'pk',
            'title',
            'description',
            'writer',
            'note_cowriters',
            'first_category',
            'second_category',
            'count_for_note_contents',
            'total_count_for_subtitle',
            'total_count_for_comments',
            'total_count_for_qna_board',
            'total_count_for_faq_list',
            'total_count_for_suggestion_list',
            'total_count_for_class_list',
            'total_count_for_error_report_list'
        ]

    def get_count_for_note_contents(self, obj):
        return obj.note_contents.count()

    def get_total_count_for_subtitle(self, obj):
        return obj.note_contents.filter(content_option="subtitle_for_page").count()

    def get_total_count_for_comments(self, obj):
        return obj.note_comments.count()

    def get_total_count_for_qna_board(self, obj):
        return obj.question_list.count()

    def get_total_count_for_faq_list(self, obj):
        return obj.faq_list.count()

    def get_total_count_for_class_list(self, obj):
        return obj.class_list.count()
    
    def get_total_count_for_suggestion_list(self, obj):
        return obj.suggestion_list.count()
    
    def get_total_count_for_suggestion_list(self, obj):
        return obj.suggestion_list.count()  
      
    def get_total_count_for_error_report_list(self, obj):
        return obj.error_report_list.count()    


class SerializerForRoadMap(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = RoadMap
        fields = ['id', 'writer', 'title', 'sub_title']


class SerializerForStudyNoteForRoadMapContent(serializers.ModelSerializer):
    class Meta:
        model = StudyNote
        fields = ('id', 'title', 'description', 'writer',
                  'created_at', 'first_category', 'second_category')


class SerializerForRoamdMapContent(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    study_note = SerializerForStudyNoteForRoadMapContent()
    # road_map = SerializerForRoadMap()

    class Meta:
        model = RoadMapContent
        fields = ['id', 'writer', 'study_note']


class SerializerForCreateCommentForFaqBoard(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForFaqBoard
        fields = ['id', 'faq_board', 'writer', 'content', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at_formatted'] = instance.created_at_formatted()
        return data


class CommentForFaqBoardSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForFaqBoard
        fields = ['id', 'writer', 'content', 'created_at']


class SerializerForCreateCommentForSuggestion(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForSuggestion
        fields = ['id', 'suggestion', 'writer', 'content', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at_formatted'] = instance.created_at_formatted()
        return data


class CommentForSuggestionSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForSuggestion
        fields = ['id', 'writer', 'content', 'created_at']


class SuggestionSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['study_note', 'title', 'content', 'writer']


class SuggestionSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer(read_only=True)
    comments = serializers.SerializerMethodField()  # 댓글 데이터를 가져올 필드

    class Meta:
        model = FAQBoard
        fields = [
            'pk',
            'study_note',
            'title',
            'content',
            'writer',
            'created_at_formatted',
            'updated_at',
            'comments'
        ]

    def get_created_at_formatted(self, obj):
        local_created_at = timezone.localtime(obj.created_at)
        return local_created_at.strftime('%m월 %d일 %H시 %M분')

    def get_comments(self, suggestion):
        comments = CommentForSuggestion.objects.filter(suggestion=suggestion)
        return CommentForSuggestionSerializer(comments, many=True).data


class FAQBoardSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = FAQBoard
        fields = ['pk', 'study_note', 'title', 'content',
                  'writer', 'created_at_formatted', 'updated_at']

    def get_created_at_formatted(self, obj):
        local_created_at = timezone.localtime(obj.created_at)
        return local_created_at.strftime('%m월 %d일 %H시 %M분')


class AnswerForQaBoardSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = AnswerForQaBoard
        fields = ['pk', 'question', 'content',
                  'writer', 'created_at_formatted']

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()


class QnABoardSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    answers_for_qa_board = AnswerForQaBoardSerializer(
        many=True, read_only=True)

    class Meta:
        model = QnABoard
        fields = ['pk', 'study_note', 'title', 'content', 'page',
                  'writer', 'created_at_formatted', 'updated_at', 'answers_for_qa_board']

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
    # is_logged_in = serializers.SerializerMethodField()  # 새로운 필드 추가

    class Meta:
        model = ClassRoomForStudyNote
        fields = ['id',
                  'current_note',
                  'current_page',
                  'writer',
                  #   'is_logged_in',
                  'is_approved',
                  'created_at_formatted']

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()

    # def get_is_logged_in(self, obj):
    #     writer = obj.writer
    #     if writer and writer.is_authenticated:
    #         # 작성자(writer)의 ID와 현재 요청된 사용자의 ID를 비교하여 로그인 여부 확인
    #         return writer.id == self.context['request'].user.id
    #     return False


class StudyNoteBriefingBoardSerializer(serializers.ModelSerializer):
    # created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNoteBriefingBoard
        fields = ('id', 'note', 'writer', 'comment', 'like_count',
                  'created_at', 'updated_at', 'is_edit_mode', 'created_at_formatted')
        read_only_fields = ('id', 'created_at', 'updated_at')


# class StudyNoteSerializer(serializers.ModelSerializer):
#     writer = UserProfileImageSerializer(read_only=True)
#     note_cowriters = CoWriterForStudyNoteSerializer(many=True, required=False)
#     count_for_note_contents = serializers.SerializerMethodField()
#     total_count_for_subtitle = serializers.SerializerMethodField()
#     total_count_for_comments = serializers.SerializerMethodField()
#     total_count_for_qna_board = serializers.SerializerMethodField()
#     count_for_class_list = serializers.SerializerMethodField()

#     class Meta:
#         model = StudyNote
#         fields = [
#             'pk',
#             'title',
#             'description',
#             'writer',
#             'note_cowriters',
#             'first_category',
#             'second_category',
#             'count_for_note_contents',
#             'total_count_for_subtitle',
#             'total_count_for_comments',
#             'total_count_for_qna_board',
#             'count_for_class_list'
#         ]

#     def get_count_for_note_contents(self, obj):
#         return obj.note_contents.count()

#     def get_total_count_for_subtitle(self, obj):
#         return obj.note_contents.filter(content_option="subtitle_for_page").count()

#     def get_total_count_for_comments(self, obj):
#         return obj.note_comments.count()

#     def get_total_count_for_qna_board(self, obj):
#         return obj.question_list.count()

#     def get_count_for_class_list(self, obj):
#         return obj.class_list.count()

class CommentForErrorReportSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForErrorReport
        fields = ['pk', 'error_report', 'writer', 'content', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at_formatted'] = instance.created_at_formatted()
        return data


class ErrorReportForStudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    comments = CommentForErrorReportSerializer(many=True)  # 댓글 정보를 시리얼라이즈

    class Meta:
        model = ErrorReportForStudyNote
        fields = ['pk', 'study_note', 'writer', 'page', 'content',
                  'is_resolved', 'created_at_formatted', 'updated_at', 'comments']

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()


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


class SerializerForCreateErrorReportForNote(serializers.ModelSerializer):
    class Meta:
        model = ErrorReportForStudyNote
        fields = (
            "study_note",
            "page",
            "content",
        )
