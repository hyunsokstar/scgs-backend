from rest_framework import serializers
from .models import (
    Challenge,
    EvaluationCriteria,
    EvaluationResult,
    ChallengeResult,
    ChallengeComment,
    ChallengeRef,
    ChallengerRef
)
from users.serializers import UserProfileImageSerializer
from django.db.models import Q


class ChallengeCommentSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = ChallengeComment
        fields = (
            'id',
            'challenge',
            'writer',
            'writer_classfication',
            'comment',
        )


class SerializerForCreateChallenge(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['title', 'subtitle', 'description', 'main_image', 'writer']


class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = (
            'id',
            'item_description',
            # 다른 EvaluationCriteria 모델의 필드들을 여기에 추가하세요
        )


class ChallengeResultSerializer(serializers.ModelSerializer):
    challenger = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeResult
        fields = (
            'id',
            'challenger',
            'challenge',
            'pass_status',
            'comment',
            'created_at',
            'created_at_formatted',
            'github_url1',
            'github_url2',
            'note_url',
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%y년 %m월 %d일')


class SerializerForChallenges(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    challenge_results = ChallengeResultSerializer(many=True)
    created_at_formatted = serializers.SerializerMethodField()
    evaluation_criterials = EvaluationCriteriaSerializer(
        many=True, read_only=True)  # 추가
    count_for_challenge_results = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = (
            'id',
            'title',
            'subtitle',
            'description',
            'main_image',
            'writer',
            'created_at_formatted',
            'evaluation_criterials',  # 추가
            'created_at',
            'started_at',
            'deadline',
            'challenge_results',
            'count_for_challenge_results'  # 새로운 필드 추가
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%y년 %m월 %d일')

    def get_count_for_challenge_results(self, obj):
        return obj.challenge_results.count()


class EvaluationResultSerializer(serializers.ModelSerializer):
    challenger = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = EvaluationResult
        fields = ('id', 'challenger',
                  'evaluate_criteria_description', 'result')


class EvaluationResultSerializer(serializers.ModelSerializer):
    challenger = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = EvaluationResult
        fields = ('id', 'challenger',
                  'evaluate_criteria_description', 'result')


class SerializerForChallengerRef(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    class Meta:
        model = ChallengerRef
        fields = (
            'id',
            'writer',
            'url',
            'description'
        )

class SerializerForChallengeRef(serializers.ModelSerializer):
    class Meta:
        model = ChallengeRef
        fields = (
            'id',
            'url',
            'description'
        )


class SerializerForChallengeDetail(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    evaluation_criterials = EvaluationCriteriaSerializer(
        many=True, read_only=True)

    # EvaluationResult 정보 추가
    evaluation_results = EvaluationResultSerializer(
        source='evaluations', many=True, read_only=True)

    # 추가: is_exist_for_evaluation_result 필드
    is_exist_for_evaluation_result = serializers.SerializerMethodField()

    challenge_results = ChallengeResultSerializer(many=True)
    # challenge_comments = ChallengeCommentSerializer(many=True)
    challenge_comments = serializers.SerializerMethodField()  # 수정된 부분

    challenge_refs = SerializerForChallengeRef(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = (
            'id',
            'title',
            'subtitle',
            'description',
            'main_image',
            'writer',
            'created_at',
            'created_at_formatted',
            'evaluation_criterials',
            'evaluation_results',  # EvaluationResult 정보 추가
            'is_exist_for_evaluation_result',  # 추가: is_exist_for_evaluation_result 필드
            'challenge_results',
            'challenge_comments',
            'challenge_refs'
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%y년 %m월 %d일')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # evaluation_results 필드를 가공하여 새로운 구조로 변환
        evaluation_results = representation.get('evaluation_results', [])
        evaluation_data = {}
        for result in evaluation_results:
            challenger = result['challenger']['username']
            description = result['evaluate_criteria_description']
            result_value = result['result']

            if challenger not in evaluation_data:
                evaluation_data[challenger] = {}

            evaluation_data[challenger][description] = result_value

        representation['evaluation_results'] = evaluation_data

        return representation

    # comment writer 가 챌린지 유저이거나 로그인 유저
    def get_challenge_comments(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        # 현재 유저 (request.user) 또는 challenge.writer와 동일한 writer를 가진 challenge_comments 필터링
        # comments = obj.challenge_comments.filter(
        #     Q(challenger=user) | Q(writer=obj.writer))
        comments = obj.challenge_comments.all()

        # 필터링된 데이터를 ChallengeCommentSerializer를 사용하여 직렬화
        serializer = ChallengeCommentSerializer(comments, many=True)
        return serializer.data

    # 추가: is_exist_for_evaluation_result 필드의 값을 설정하는 메서드

    def get_is_exist_for_evaluation_result(self, obj):
        # 현재 유저 (request.user)의 평가 결과가 있는지 여부를 확인
        request = self.context.get('request')
        user = request.user if request else None

        if user:
            evaluation_results = obj.evaluations.filter(challenger=user)
            print("evaluation_results.exists() : ",
                  evaluation_results.exists())
            return evaluation_results.exists()
        else:
            print("로그인 상태 아님")

        return False
