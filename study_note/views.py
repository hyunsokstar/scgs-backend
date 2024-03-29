from .models import FAQBoard
from django.db import transaction
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework import status
import random
from django.db.models import Count, Max, Min
from django.db.models import Q, F
from django.shortcuts import get_object_or_404


from django.db import models
from django.utils import timezone
from .models import (
    StudyNoteContent,
    ClassRoomForStudyNote,
    CommentForErrorReport,
    StudyNoteBriefingBoard,
    AnswerForQaBoard,
    ErrorReportForStudyNote,
    QnABoard,
    FAQBoard,
    Suggestion,
    CommentForSuggestion,
    CommentForFaqBoard,
    CoWriterForStudyNote,
    StudyNote,
    StudyNoteContent,
    RoadMap,
    RoadMapContent,
    BookMarkForStudyNote,
    LikeForStudyNote,
)
from .serializers import (
    SerializerForCreateQuestionForNote,
    StudyNoteContentSerializer,
    StudyNoteSerializer,
    StudyNoteBriefingBoardSerializer,
    CreateCommentSerializerForNote,
    ClassRoomForStudyNoteSerializer,
    QnABoardSerializer,
    ErrorReportForStudyNoteSerializer,
    SerializerForCreateErrorReportForNote,
    FAQBoardSerializer,
    CommentForErrorReportSerializer,
    SuggestionSerializer,
    SuggestionSerializerForCreate,
    SerializerForCreateCommentForSuggestion,
    CommentForSuggestionSerializer,
    CommentForFaqBoardSerializer,
    SerializerForCreateCommentForFaqBoard,
    SerializerForRoadMap,
    SerializerForRoamdMapContent,
    SerializerForRoamdMapContentBasicForRegister,
    SerializerForStudyNoteForBasic,
    BookMarkForStudyNoteSerializer,
    LikeForStudyNoteSerializer,
)


# 1122
class PageToPageContentReplacementView(APIView):
    def post(self, request, format=None):
        # 전송된 데이터 받기
        selected_my_note_id = request.data.get("selectedMyNoteId")
        checked_page_numbers_for_destination = request.data.get(
            "checkedPageNumbersForDestination"
        )
        copy_target_note_id = request.data.get("copyTargetNoteId")
        checked_page_numbers_to_copy = request.data.get("checkedPageNumbersToCopy")

        print("Received Data:")
        print("selectedMyNoteId:", selected_my_note_id)
        print("checkedPageNumbersForDestination:", checked_page_numbers_for_destination)
        print("copyTargetNoteId:", copy_target_note_id)
        print("checkedPageNumbersToCopy:", checked_page_numbers_to_copy)

        # Step 1: selected_my_note_id와 checked_page_numbers_to_copy에 해당하는 StudyNoteContent 데이터 모두 삭제
        StudyNoteContent.objects.filter(
            study_note_id=selected_my_note_id, page__in=checked_page_numbers_to_copy
        ).delete()

        # Step 2: 페이지 복사 작업 수행
        try:
            with transaction.atomic():
                for idx, page_number in enumerate(checked_page_numbers_to_copy):
                    # copy_target_note_id와 page_number에 해당하는 StudyNoteContent 객체 찾기
                    
                    source_contents = StudyNoteContent.objects.filter(study_note_id=copy_target_note_id, page=page_number)

                    destination_page_number = checked_page_numbers_for_destination[idx]

                    if source_contents.exists():
                        for target_note in source_contents:
                            
                            destination_content = StudyNoteContent(
                                study_note_id=selected_my_note_id,
                                title=target_note.title,
                                file_name=target_note.file_name,
                                content=target_note.content,
                                writer=target_note.writer,
                                order=target_note.order,
                                page=destination_page_number,
                                content_option=target_note.content_option,
                                ref_url1=target_note.ref_url1,
                                ref_url2=target_note.ref_url2,
                                youtube_url=target_note.youtube_url,
                                created_at=target_note.created_at,
                            )
                            destination_content.save()
                    else:
                        pass

        except Exception as e:
            # 에러 처리
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 응답 메시지 작성
        copied_note_title = StudyNote.objects.get(id=copy_target_note_id).title
        
        message = (
            f"{copied_note_title}에서 {len(checked_page_numbers_to_copy)}개의 데이터를 복사했습니다."
        )

        # 적절한 응답 및 HTTP 상태 코드 반환
        response_data = {
            "message": message,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class InfoViewForSelectedNoteInfoAndPageNumberList(APIView):
    def get(self, request, my_note_id):
        try:
            # 주어진 my_note_id에 해당하는 StudyNote 객체 가져오기
            selected_my_note_obj = StudyNote.objects.get(pk=my_note_id)

            # selected_my_note_obj의 title 가져오기
            title_for_my_selected_note = selected_my_note_obj.title

            # selected_my_note_obj를 가리키는 StudyNoteContent의 페이지 번호 리스트 가져오기
            # StudyNoteContent의 페이지 번호 가져오기
            page_numbers_for_selected_my_note = (
                selected_my_note_obj.note_contents.values_list("page", flat=True)
            )

            # 중복 제거하여 유일한 값만 반환
            unique_page_numbers = list(set(page_numbers_for_selected_my_note))

            # 응답 데이터 구성
            response_data = {
                "title_for_my_selected_note": title_for_my_selected_note,
                "page_numbers_for_selected_my_note": unique_page_numbers,
            }

            # 적절한 HTTP 응답 코드와 함께 데이터 응답
            return Response(response_data, status=status.HTTP_200_OK)

        except StudyNote.DoesNotExist:
            # 주어진 my_note_id에 해당하는 StudyNote가 없을 경우 에러 응답
            return Response(
                {"error": "StudyNote with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


# 1125
class GetMyNoteInfoAndTargetNoteInForToPartialCopy(APIView):
    my_note_list = []
    totalCount = 0
    perPage = 10

    def get(self, request, study_note_id):
        # 로그인 확인
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1

        print("pageNum : ", pageNum)

        # 내 노트 리스트
        my_notes = StudyNote.objects.filter(writer=request.user).exclude(
            pk=study_note_id
        )

        # total Count 정하기
        self.totalCount = my_notes.count()

        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        my_notes = my_notes[start:end]

        # 내 노트 리스트 가져오되 페이지 번호에 맞게 가져 오기
        serializer = SerializerForStudyNoteForBasic(my_notes, many=True)

        my_notes_data = serializer.data

        study_note = get_object_or_404(StudyNote, pk=study_note_id)

        # 2. 페이지 번호들을 그룹화하여 리스트로 반환
        note_content = StudyNoteContent.objects.filter(study_note=study_note)
        target_note_page_numbers = note_content.values_list(
            "page", flat=True
        ).distinct()

        # 3. 해당 StudyNote의 제목 반환
        target_note_title = study_note.title

        # response_data에 정보 담아 Response로 응답
        response_data = {
            # 내 노트 정보
            "my_note_list": my_notes_data,
            "totalCount": self.totalCount,
            "perPage": self.perPage,
            # target 정보
            "target_note_title": target_note_title,
            "target_note_page_numbers": list(target_note_page_numbers),
            "message": "partial copy from selected note is success!",
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UpdateViewForMoveNoteContentsToOtherPage(APIView):
    def put(self, request):
        checked_ids = request.data.get("checkedIds", [])  # 기본값으로 빈 리스트 설정
        selected_page = request.data.get("selectedPage", 1)

        print("checked_ids : ", checked_ids)
        print("selected_page : ", selected_page)

        # StudyNoteContent 데이터 중 id가 checked_ids에 포함되는 노트 내용들을 가져와서 페이지를 업데이트합니다.
        try:
            note_contents_to_update = StudyNoteContent.objects.filter(
                id__in=checked_ids
            )
            note_contents_to_update.update(page=selected_page)

            # 업데이트된 노트 내용의 수를 세어서 응답 메시지에 포함할 수도 있습니다.
            count_updated = note_contents_to_update.count()

            # Response message에 선택한 페이지 대신에 selected_page를 사용하여 응답합니다.
            return Response(
                {
                    "message": f"{count_updated}개의 노트 내용을 선택한 페이지({selected_page})로 이동했습니다.",
                    "pageToMove": selected_page,
                }
            )
        except StudyNoteContent.DoesNotExist:
            return Response({"message": "노트 내용을 찾을 수 없습니다."})


class ListViewForMyLikeNote(APIView):
    def get(self, request):
        user_likes = LikeForStudyNote.objects.filter(
            user=request.user
        )  # 현재 사용자의 북마크 필터링
        serializer = LikeForStudyNoteSerializer(user_likes, many=True)  # 북마크 시리얼라이즈
        # The above code is not doing anything. It is just a sequence of numbers and symbols.
        return Response(serializer.data)


class LikeViewForNoteForPk(APIView):
    def post(self, request, notePk):
        print("like 요청 받음 !")
        study_note = get_object_or_404(StudyNote, pk=notePk)

        # 현재 유저의 북마크 확인
        like, created = LikeForStudyNote.objects.get_or_create(
            user=request.user,
            study_note=study_note,
        )

        # 북마크가 이미 존재하는 경우 삭제하고, 아닌 경우 생성
        if not created:
            like.delete()
            message = f"like for '{study_note.title}' removed."
        else:
            message = f"like for '{study_note.title}' added."

        return Response({"message": message}, status=status.HTTP_200_OK)


# LikeViewForNoteForPk
class BookMarkViewForNoteForPk(APIView):
    def post(self, request, notePk):
        print("bookmark 요청 받음 !")
        # 해당 notePk에 해당하는 StudyNote가 있는지 확인
        study_note = get_object_or_404(StudyNote, pk=notePk)

        # 현재 유저의 북마크 확인
        bookmark, created = BookMarkForStudyNote.objects.get_or_create(
            user=request.user,
            study_note=study_note,
        )

        # 북마크가 이미 존재하는 경우 삭제하고, 아닌 경우 생성
        if not created:
            bookmark.delete()
            message = f"Bookmark for '{study_note.title}' removed."
        else:
            message = f"Bookmark for '{study_note.title}' added."

        return Response({"message": message}, status=status.HTTP_200_OK)


class ListViewForMyBookMark(APIView):
    def get(self, request):
        user_bookmarks = BookMarkForStudyNote.objects.filter(
            user=request.user
        )  # 현재 사용자의 북마크 필터링
        serializer = BookMarkForStudyNoteSerializer(
            user_bookmarks, many=True
        )  # 북마크 시리얼라이즈
        return Response(serializer.data)


class UpdateViewForRoadMapContentOrder(APIView):
    def put(self, request):
        try:
            roadMapId = request.data.get("roadMapId")
            updatedRoadMapOrderList = request.data.get("updatedRoadMapOrderList", [])
            print("roadMapId for reordering: ", roadMapId)
            print("updatedRoadMapOrderList for reordering: ", updatedRoadMapOrderList)

            for item in updatedRoadMapOrderList:
                content_id = item.get("id")
                new_order = item.get("order")

                # Fetch the RoadMapContent instance
                content = RoadMapContent.objects.get(
                    id=content_id, road_map_id=roadMapId
                )
                content.order = new_order  # Update the order
                content.save()  # Save the changes

            return Response(
                {"success": "Study note content order updated successfully."},
                status=status.HTTP_200_OK,
            )

        except StudyNoteContent.DoesNotExist:
            return Response(
                {"error": "Study note content does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


# DeleteViewForRoadMapContentForCheckedIds
class DeleteViewForRoadMapContentForCheckedIds(APIView):
    def delete(self, request):
        try:
            if request.user.is_authenticated:
                print("로그인 확인 삭제 진행")
            else:
                return Response(
                    {"status": "error", "message": "로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # todo1: roadMapId, checkedIdsForRoadMapContent 얻어 오기
            roadMapId = request.data.get("roadMapId")
            checkedIdsForRoadMapContent = request.data.get(
                "checkedIdsForRoadMapContent"
            )

            if roadMapId is None or checkedIdsForRoadMapContent is None:
                return Response(
                    {"message": "Missing data in the request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            print("여기까지만 실행 되나 ??? ")
            print("roadMapId : ", roadMapId)
            roadmap = RoadMap.objects.get(id=roadMapId)

            print("roadmap.writer.username :::;:: ", roadmap.writer.username)

            if request.user.username == roadmap.writer.username:
                # todo2: checkedIdsForRoadMapContent 에 해당하는(id로 비교) RoadMapContent 삭제
                RoadMapContent.objects.filter(
                    id__in=checkedIdsForRoadMapContent
                ).delete()
                # 성공적인 응답
                return Response(
                    {"message": "delete road map content success !!"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": f"{roadmap.writer.username}님만 삭제할 수 있습니다"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except RoadMap.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "roadmap is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateViewForRegisterRoadMapFromCheckedNoteIds(APIView):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                roadMapId = request.data.get("roadMapId")
                checkedIdsForNoteList = request.data.get("checkedIdsForNoteList")

                if roadMapId and checkedIdsForNoteList:
                    road_map = RoadMap.objects.get(id=roadMapId)
                    notes_to_link = StudyNote.objects.filter(
                        id__in=checkedIdsForNoteList
                    )

                    max_order = RoadMapContent.objects.filter(
                        road_map=road_map
                    ).aggregate(Max("order"))["order__max"]
                    next_order = max_order + 1 if max_order is not None else 1

                    for note in notes_to_link:
                        RoadMapContent.objects.create(
                            study_note=note,
                            road_map=road_map,
                            writer=request.user,
                            order=next_order,
                        )
                        next_order += 1  # Increase order for each note

                    return Response({"status": "success", "message": f"로드맵 등록 완료"})
                else:
                    return Response(
                        {"status": "error", "message": "필수 정보가 누락되었습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(
                    {"status": "error", "message": "로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except RoadMap.DoesNotExist:
            return Response(
                {"status": "error", "message": "해당하는 로드맵을 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except StudyNote.DoesNotExist:
            return Response(
                {"status": "error", "message": "하나 이상의 노트를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "로드맵 등록 중 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudyNoteAPIViewForRegisterRoadMap(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 4  # 1 페이지에 몇개씩
    all_note_list = []

    def getAllNoteList(self):
        note_obj = StudyNote.objects.all()
        return note_obj

    # todo:
    # ids_to_exclude 에 값이 있을 경우
    # StudyNote 필터링할때 id가 todo ids_to_exclude 에 포함되는것들은 제외하도록 하기
    def get_all_note_list_filtered(
        self, selected_note_writer, first_category, second_category, ids_to_exclude
    ):
        filter_conditions = Q()
        if selected_note_writer != "":
            filter_conditions &= Q(writer__username=selected_note_writer)
        if first_category != "":
            filter_conditions &= Q(first_category=first_category)
        if second_category != "":
            filter_conditions &= Q(second_category=second_category)

        if ids_to_exclude:
            filter_conditions &= ~Q(id__in=ids_to_exclude)

        return StudyNote.objects.filter(filter_conditions)  # 필터링된 데이터를 반환

    def get(self, request):
        selected_note_writer = request.query_params.get("selectedNoteWriter", "")
        first_category = request.query_params.get("first_category", "")
        second_category = request.query_params.get("second_category", "")

        # step1 page 번호 가져 오기
        try:
            roadMapId = request.query_params.get(
                "roadMapId", 1
            )  # null 일 경우는 없으므로 디폴트 1로 처리
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        print("roadMapId check: ", roadMapId)
        print("page check : ", page)

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # roadMapId을 가리키는 RoadMapContent의 study_note들의 id들을 가져와서 ids_to_exclude에 저장
        road_map_content_ids = RoadMapContent.objects.filter(
            road_map__id=roadMapId
        ).values_list("study_note__id", flat=True)
        ids_to_exclude = list(road_map_content_ids)

        print("road_map_content_ids : ", road_map_content_ids)

        filtered_note_list = self.get_all_note_list_filtered(
            selected_note_writer, first_category, second_category, ids_to_exclude
        )
        self.total_page_count = filtered_note_list.count()
        paginated_notes = filtered_note_list[start:end]

        serializer = SerializerForStudyNoteForBasic(paginated_notes, many=True)

        note_writers = list(set(note.writer.username for note in paginated_notes))

        response_data = {
            "note_writers": note_writers,  # Include the note writers in the response
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page,
        }

        return Response(response_data, status=HTTP_200_OK)


class ListViewForRoadMapContentForRegister(APIView):
    listForRoadMap = []

    def getRoadMapContentListById(self, roadMapId):
        return RoadMapContent.objects.filter(road_map=roadMapId).order_by("order")

    def get(self, request, roadMapId):
        print("roadMapId : ", roadMapId)

        road_map_contents = self.getRoadMapContentListById(roadMapId)
        serializer = SerializerForRoamdMapContentBasicForRegister(
            road_map_contents, many=True
        )

        response_data = {
            "road_map_contents": serializer.data,
            # "totalCount": self.totalCount,
            # "perPage": self.perPage,
        }

        return Response(response_data, status=HTTP_200_OK)


class ListViewForRoadMapContent(APIView):
    listForRoadMap = []

    def getRoadMapContentListById(self, roadMapId):
        return RoadMapContent.objects.filter(road_map=roadMapId)

    def get(self, request, roadMapId):
        print("roadMapId : ", roadMapId)

        road_map_contents = self.getRoadMapContentListById(roadMapId)
        serializer = SerializerForRoamdMapContent(
            road_map_contents, many=True, context={"request": request}
        )

        response_data = {
            "road_map_contents": serializer.data,
            # "totalCount": self.totalCount,
            # "perPage": self.perPage,
        }

        return Response(response_data, status=HTTP_200_OK)


# DeleteViewForRoadMap


class DeleteViewForRoadMap(APIView):
    def delete(self, request, roadMapId):
        # print("삭제 요청 확인 ", roadMapId)

        try:
            # commentPk에 해당하는 댓글 찾기
            roadmap = RoadMap.objects.get(id=roadMapId)
            if request.user.username == roadmap.writer.username:
                pass
            else:
                return Response(
                    {"message": f"{roadmap.writer.username}님만 삭제할 수 있습니다"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            # 댓글 삭제
            roadmap.delete()

            # 성공적인 응답
            return Response(
                {"message": "delete road map success !!"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except RoadMap.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "roadmap is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateViewForRoadMap(APIView):
    def post(self, request):
        try:
            if request.user.is_authenticated:  # 사용자가 인증되었는지 확인
                title = request.data.get("title")
                subTitle = request.data.get("subTitle")
                writer = request.user

                # title과 subTitle을 이용하여 RoadMap 생성
                roadmap = RoadMap.objects.create(
                    writer=writer, title=title, sub_title=subTitle
                )

                return Response(
                    {
                        "status": "success",
                        "message": f'입력한 게시글의 "{roadmap.title}"을(를) 생성하였습니다.',
                    }
                )

            else:  # 로그인하지 않은 경우
                return Response(
                    {"status": "error", "message": "로그인 유저만 입력할 수 있습니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Exception as e:
            return Response(
                {"status": "error", "message": "로드맵을 생성하는 중에 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListViewForRoadMap(APIView):
    listForRoadMap = []
    totalCount = 0
    perPage = 6

    def getAllRoadMapList(self):
        return RoadMap.objects.all()

    def get(self, request):
        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1

        # 모든 리스트 정보 가져 오기
        self.listForRoadMap = self.getAllRoadMapList()

        # 총 개수 초기화
        self.totalCount = self.listForRoadMap.count()

        # list 범위 지정
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.listForRoadMap = self.listForRoadMap[start:end]

        # list 직렬화
        serializer = SerializerForRoadMap(self.listForRoadMap, many=True)

        # 응답 데이터
        response_data = {
            "listForRoadMap": serializer.data,
            "totalCount": self.totalCount,
            "perPage": self.perPage,
        }

        return Response(response_data, status=HTTP_200_OK)


class CopyOneOfNoteToMe(APIView):
    def post(self, request):
        studyNotePk = request.data.get("studyNotePk")
        print("studyNotePk : ", studyNotePk)

        with transaction.atomic():
            try:
                user = request.user

                original_study_note = StudyNote.objects.get(pk=studyNotePk)

                # StudyNote 생성
                new_study_note = StudyNote.objects.create(
                    title=original_study_note.title,
                    description=original_study_note.description,
                    writer=user,
                )

                # StudyNoteContent 생성
                original_note_contents = original_study_note.note_contents.all()
                for original_note_content in original_note_contents:
                    StudyNoteContent.objects.create(
                        study_note=new_study_note,
                        title=original_note_content.title,
                        file_name=original_note_content.file_name,
                        content=original_note_content.content,
                        content_option=original_note_content.content_option,
                        writer=user,
                        order=original_note_content.order,
                        created_at=original_note_content.created_at,
                        page=original_note_content.page,
                    )

                response_data = {
                    "message": "Selected notes copied to my note successfully."
                }

                return Response(response_data, status=HTTP_200_OK)

            except StudyNote.DoesNotExist:
                response_data = {"message": "One or more selected notes do not exist."}

                return Response(response_data, status=HTTP_400_BAD_REQUEST)


class UpdateViewForIsTaskingForCowriter(APIView):
    authority_for_writing_note_contents = None

    def put(self, request, coWriterId):
        study_note_pk = request.data.get("studyNotePk")
        print("study_note_pk : ", study_note_pk)
        print("coWriterId : ", coWriterId)

        # 모델에서 해당하는 CoWriterForStudyNote 가져오기
        try:
            co_writer = CoWriterForStudyNote.objects.get(
                id=coWriterId, study_note_id=study_note_pk
            )
        except CoWriterForStudyNote.DoesNotExist:
            return Response(
                {"message": "해당 CoWriter를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        # 업데이트되기 전의 값을 기반으로 반전
        is_tasking_before_update = co_writer.is_tasking
        co_writer.is_tasking = not is_tasking_before_update
        self.authority_for_writing_note_contents = not is_tasking_before_update
        co_writer.save()

        if is_tasking_before_update == False:
            CoWriterForStudyNote.objects.filter(study_note_id=study_note_pk).exclude(
                id=coWriterId
            ).update(is_tasking=is_tasking_before_update)

        cowriters = CoWriterForStudyNote.objects.filter(study_note_id=study_note_pk)

        cowriters_data = []

        for cowriter in cowriters:
            if cowriter.is_approved:
                cowriter_data = {
                    "id": cowriter.id,
                    "username": cowriter.writer.username,
                    "profile_image": cowriter.writer.profile_image,
                    "is_tasking": cowriter.is_tasking,
                    "current_page": cowriter.current_page,
                    "task_description": cowriter.task_description,
                }
                cowriters_data.append(cowriter_data)

        # 성공 응답
        response_data = {
            "message": "업데이트가 성공적으로 완료되었습니다.",
            "cowriters_data": cowriters_data,
            "authority_for_writing_note_contents": self.authority_for_writing_note_contents,
        }

        return Response(response_data, status=status.HTTP_200_OK)


# UpdateViewForSuggestion
class UpdateViewForSuggestion(APIView):
    def put(self, request, suggestionPk):
        print("update 요청 받았습니다")
        try:
            # commentPk에 해당하는 댓글 찾기
            suggestion = Suggestion.objects.get(pk=suggestionPk)

            # 요청에서 수정된 내용 가져오기
            editedtitle = request.data.get("title")
            editedContent = request.data.get("content")

            # 댓글 업데이트
            suggestion.title = editedtitle
            suggestion.content = editedContent
            suggestion.save()

            # 성공적인 응답
            return Response(
                {"message": "faq suggestion update success !!"},
                status=status.HTTP_200_OK,
            )

        except Suggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "suggestion not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# DeleteViewForSuggestion
class DeleteViewForSuggestion(APIView):
    def delete(self, request, suggestionPk):
        print("삭제 요청 확인 ", suggestionPk)
        try:
            # commentPk에 해당하는 댓글 찾기
            suggestion = Suggestion.objects.get(pk=suggestionPk)

            # 댓글 삭제
            suggestion.delete()

            # 성공적인 응답
            return Response(
                {"message": "delete comment for faq success"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Suggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# DeleteViewForSuggestion
class DeleteViewForCommentForSuggestion(APIView):
    def delete(self, request, commentPk):
        try:
            # commentPk에 해당하는 댓글 찾기
            comment = CommentForSuggestion.objects.get(pk=commentPk)

            # 댓글 삭제
            comment.delete()

            # 성공적인 응답
            return Response(
                {"message": "delete comment for faq success"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except CommentForSuggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# UpdateViewForCommentForFaqForBoard
class UpdateViewForSuggestionComment(APIView):
    def put(self, request, commentPk):
        try:
            # commentPk에 해당하는 댓글 찾기
            comment = CommentForSuggestion.objects.get(pk=commentPk)

            # 요청에서 수정된 내용 가져오기
            editedContent = request.data.get("editedContent")

            # 댓글 업데이트
            comment.content = editedContent
            comment.save()

            # 성공적인 응답
            return Response(
                {"message": "faq comment update success !!"}, status=status.HTTP_200_OK
            )

        except CommentForSuggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteViewForFaqComment(APIView):
    def delete(self, request, commentPk):
        try:
            # commentPk에 해당하는 댓글 찾기
            comment = CommentForFaqBoard.objects.get(pk=commentPk)

            # 댓글 삭제
            comment.delete()

            # 성공적인 응답
            return Response(
                {"message": "delete comment for faq success"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except CommentForFaqBoard.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# UpdateViewForSuggestion


class UpdateViewForFaqComment(APIView):
    def put(self, request, commentPk):
        try:
            # commentPk에 해당하는 댓글 찾기
            comment = CommentForFaqBoard.objects.get(pk=commentPk)

            # 요청에서 수정된 내용 가져오기
            editedContent = request.data.get("editedContent")

            # 댓글 업데이트
            comment.content = editedContent
            comment.save()

            # 성공적인 응답
            return Response(
                {"message": "faq comment update success !!"}, status=status.HTTP_200_OK
            )

        except CommentForFaqBoard.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response(
                {"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # 다른 예외 처리
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateViewForCommentForFaqBoard(APIView):
    def post(self, request, faqPk):
        try:
            print("faqPk :::::::::::: ", faqPk)
            faq_board = FAQBoard.objects.get(id=faqPk)

            print("faq_board ::::::::::::: ", faq_board)

        except CommentForFaqBoard.DoesNotExist:
            return Response(
                {"message": "Error report not found"}, status=status.HTTP_404_NOT_FOUND
            )

        print("request.data : ", request.data)
        request.data["faq_board"] = faq_board.id
        serializer = SerializerForCreateCommentForFaqBoard(data=request.data)

        if serializer.is_valid():
            print("시리얼 라이저는 유효")
            print("댓글 추가 요청 확인 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            serializer.save(writer=request.user)

            return Response(
                {"message": "Comment created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return detailed error messages
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListViewForCommentForFaqBoard(APIView):
    def get(self, request, faqPk):
        print("댓글 데이터 요청 확인 for 건의 사항")
        # faqId 해당하는 CommentForSuggestion 정보 가져오기
        comments = CommentForFaqBoard.objects.filter(faq_board_id=faqPk)
        print("comments : ", comments)

        if not comments:
            raise NotFound("Comments not found")

        # Serializer를 사용하여 데이터 직렬화
        serializer = CommentForFaqBoardSerializer(comments, many=True)

        # 응답 데이터 구성
        response_data = {
            "comments": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ListViewForCommentForSuggestion(APIView):
    def get(self, request, suggestionPk):
        print("댓글 데이터 요청 확인 for 건의 사항")
        try:
            # suggestionPk 해당하는 CommentForSuggestion 정보 가져오기
            comments = CommentForSuggestion.objects.filter(suggestion_id=suggestionPk)

            # Serializer를 사용하여 데이터 직렬화
            serializer = CommentForSuggestionSerializer(comments, many=True)

            # 응답 데이터 구성
            response_data = {
                "comments": serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except CommentForSuggestion.DoesNotExist:
            return Response(
                {"detail": "Comments not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateViewForCommentForSuggestionForNote(APIView):
    def post(self, request, suggestionPk):
        print("suggest 댓글 추가 요청 check !!!!!!!!!")
        try:
            print("suggestionPk :::::::::::: ", suggestionPk)
            # Check if the error_report with the provided error_report_pk exists
            suggestion = Suggestion.objects.get(id=suggestionPk)

            print("suggestion ::::::::::::: ", suggestion)

        except Suggestion.DoesNotExist:
            return Response(
                {"message": "Error report not found"}, status=status.HTTP_404_NOT_FOUND
            )

        print("request.data : ", request.data)

        request.data["suggestion"] = suggestion.id
        serializer = SerializerForCreateCommentForSuggestion(data=request.data)

        if serializer.is_valid():
            print("시리얼 라이저는 유효")
            print("댓글 추가 요청 확인 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            serializer.save(writer=request.user)

            return Response(
                {"message": "Comment created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return detailed error messages
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SearchViewForStudyNoteSuggestionList(APIView):
    suggestionList = []

    def get(self, request, study_note_pk):
        print("search 요청 check !! ")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        search_words = request.query_params.get("searchWords", "")

        study_note_list = study_note.suggestion_list.all()
        self.suggestionList = study_note_list

        if search_words:
            print("search_words : ", search_words)
            study_note_list = study_note_list.filter(title__icontains=search_words)
            print("study_note_list : ", study_note_list)

        self.suggestionList = study_note_list

        result_count = self.suggestionList.count()  # Count the number of search results

        serializer = SuggestionSerializer(self.suggestionList, many=True)

        response_data = {
            "message": f"{result_count}개의 데이터가 검색되었습니다.",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


# CreateViewForSuggestionForBoard


class CreateViewForSuggestionForNote(APIView):
    def post(self, request, study_note_pk):
        try:
            print("건의 사항 추가 요청 check !!")
            study_note_pk = int(study_note_pk)

            # 필요한 필드 직접 추출
            title = request.data.get("title")
            content = request.data.get("content")

            # SuggestionSerializerForCreate 사용
            serializer = SuggestionSerializerForCreate(
                data={
                    "study_note": study_note_pk,
                    "title": title,
                    "content": content,
                    "writer": request.user.id,  # 또는 원하는 작성자 정보
                }
            )

            if serializer.is_valid():
                suggestion = serializer.save()  # create 메서드를 사용하여 저장

                return Response(
                    {"message": "건의 사항이 추가되었습니다.", "suggestion_id": suggestion.id},
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("에러 발생:", str(e))
            return Response(
                {"message": "건의 사항 추가 중에 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateViewForErrorReportComment(APIView):
    def post(self, request, error_report_pk):
        try:
            print("error_report_pk :::::::::::: ", error_report_pk)
            # Check if the error_report with the provided error_report_pk exists
            error_report = ErrorReportForStudyNote.objects.get(id=error_report_pk)

            print("error_report ::::::::::::: ", error_report)

        except ErrorReportForStudyNote.DoesNotExist:
            return Response(
                {"message": "Error report not found"}, status=status.HTTP_404_NOT_FOUND
            )

        print("request.data : ", request.data)

        request.data["error_report"] = error_report.id
        serializer = CommentForErrorReportSerializer(data=request.data)

        if serializer.is_valid():
            print("시리얼 라이저는 유효")
            print("댓글 추가 요청 확인 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            serializer.save(error_report=error_report, writer=request.user)

            return Response(
                {"message": "Comment created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return detailed error messages
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreteViewForFAQBoard(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        title = request.data["title"]
        content = request.data["content"]

        note_content = FAQBoard.objects.create(
            study_note_id=study_note_pk,
            title=title,
            content=content,
            writer=request.user,
        )
        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)


# class CreteViewForSuggestionForNote(APIView):
#     def post(self, request, study_note_pk):
#         study_note_pk = int(study_note_pk)
#         title = request.data["title"]
#         content = request.data["content"]

#         note_content = Suggestion.objects.create(
#             study_note_id=study_note_pk,
#             title=title,
#             content=content,
#             writer=request.user
#         )
#         print("note_content : ", note_content)
#         return Response(status=status.HTTP_201_CREATED)


class DeleteViewForWithDrawClassRoom(APIView):
    def delete(self, request, study_note_pk):
        try:
            classroom = ClassRoomForStudyNote.objects.get(
                current_note_id=study_note_pk, writer=request.user
            )
        except ClassRoomForStudyNote.DoesNotExist:
            return Response(
                {"message": "classroom not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != classroom.writer:
            return Response(
                {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        classroom.delete()

        return Response(
            {"message": "FAQ deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class SearchViewForStudyNoteCardList(APIView):
    studyNoteList = []

    def get(self, request):
        try:
            study_note_list = StudyNote.objects.all()
            print("study_note_list : ", study_note_list)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        search_words = request.query_params.get("searchWords", "")

        if search_words:
            study_note_list = study_note_list.filter(title__icontains=search_words)

        self.studyNoteList = study_note_list

        result_count = self.studyNoteList.count()

        serializer = StudyNoteSerializer(self.studyNoteList, many=True)

        response_data = {
            "message": f"{result_count}개의 데이터가 검색되었습니다.",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SearchViewForStudyNoteErrorReportList(APIView):
    errorReportList = []

    def get(self, request, study_note_pk):
        # print("search 요청 check !! ")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
            print("study_note check : ", study_note)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        search_words = request.query_params.get("searchWords", "")

        study_note_list = study_note.error_report_list.all()
        self.errorReportList = study_note_list

        if search_words:
            study_note_list = study_note_list.filter(content__icontains=search_words)

        self.errorReportList = study_note_list

        # Count the number of search results
        result_count = self.errorReportList.count()

        serializer = ErrorReportForStudyNoteSerializer(self.errorReportList, many=True)

        # Create a custom response data dictionary
        response_data = {
            # Include the result count in the message
            "message": f"{result_count}개의 데이터가 검색되었습니다.",
            "data": serializer.data,  # Include the serialized data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SearchViewForStudyNoteQnaList(APIView):
    errorReportList = []

    def get(self, request, study_note_pk):
        # print("search 요청 check !! ")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
            print("study_note check : ", study_note)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        search_words = request.query_params.get("searchWords", "")

        study_note_list = study_note.question_list.all()
        self.errorReportList = study_note_list

        if search_words:
            print("search_words : ", search_words)
            study_note_list = study_note_list.filter(title__icontains=search_words)
            print("study_note_list : ", study_note_list)

        self.errorReportList = study_note_list

        # Count the number of search results
        result_count = self.errorReportList.count()

        serializer = FAQBoardSerializer(self.errorReportList, many=True)

        # Create a custom response data dictionary
        response_data = {
            # Include the result count in the message
            "message": f"{result_count}개의 데이터가 검색되었습니다.",
            "data": serializer.data,  # Include the serialized data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class DeleteViewForNoteFaq(APIView):
    def delete(self, request, faq_pk):
        try:
            faq = FAQBoard.objects.get(pk=faq_pk)
        except FAQBoard.DoesNotExist:
            return Response(
                {"message": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != faq.writer:
            return Response(
                {"message": f"{faq.writer.username}만 삭제할 수 있습니다"},
                status=status.HTTP_403_FORBIDDEN,
            )

        faq.delete()

        return Response(
            {"message": "FAQ deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class DeleteViewForCommentForErrorReport(APIView):
    def delete(self, request, commentPk):
        try:
            comment = CommentForErrorReport.objects.get(pk=commentPk)
        except CommentForErrorReport.DoesNotExist:
            return Response(
                {"message": "comment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != comment.writer:
            return Response(
                {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()

        return Response(
            {"message": "FAQ deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class DeleteViewForClassRoomForNote(APIView):
    def delete(self, request, classRoomId):
        try:
            classroom = ClassRoomForStudyNote.objects.get(pk=classRoomId)
        except ClassRoomForStudyNote.DoesNotExist:
            return Response(
                {"message": "classroom not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != classroom.writer:
            return Response(
                {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        classroom.delete()

        return Response(
            {"message": "FAQ deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# UpdateViewForFaq


class UpdateViewForFaq(APIView):
    def put(self, request, faq_pk):
        try:
            faq = FAQBoard.objects.get(pk=faq_pk)
        except FAQBoard.DoesNotExist:
            return Response(
                {"message": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != faq.writer:
            return Response(
                {"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        title = request.data.get("title")
        content = request.data.get("content")

        if title is None or content is None:
            return Response(
                {"message": "Title and content are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        faq.title = title
        faq.content = content
        faq.save()

        return Response({"message": "FAQ update success"}, status=status.HTTP_200_OK)


# SearchViewForStudyNoteSuggestionList


class SearchViewForStudyNoteFaqList(APIView):
    faqList = []

    def get(self, request, study_note_pk):
        print("search 요청 check !! ")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        search_words = request.query_params.get("searchWords", "")

        study_note_list = study_note.faq_list.all()
        self.faqList = study_note_list

        if search_words:
            print("search_words : ", search_words)
            study_note_list = study_note_list.filter(title__icontains=search_words)
            print("study_note_list : ", study_note_list)

        self.faqList = study_note_list

        result_count = self.faqList.count()  # Count the number of search results

        serializer = FAQBoardSerializer(self.faqList, many=True)

        # Create a custom response data dictionary
        response_data = {
            # Include the result count in the message
            "message": f"{result_count}개의 데이터가 검색되었습니다.",
            "data": serializer.data,  # Include the serialized data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class UpdateViewForNoteSubtitle(APIView):
    def put(self, request, content_pk, format=None):
        study_note_content = StudyNoteContent.objects.get(pk=content_pk)

        study_note_content.title = request.data.get("title", study_note_content.title)
        study_note_content.content = request.data.get(
            "content", study_note_content.content
        )
        study_note_content.ref_url1 = request.data.get(
            "ref_url1", study_note_content.ref_url1
        )
        study_note_content.ref_url2 = request.data.get(
            "ref_url2", study_note_content.ref_url2
        )
        study_note_content.youtube_url = request.data.get(
            "youtube_url", study_note_content.youtube_url
        )

        study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class DeleteViewForStudyNote(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def delete(self, request, notePk):
        api_docu = self.get_object(notePk)
        api_docu.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class DeleteViewForErrorReport(APIView):
    def delete(self, request, error_report_pk):
        try:
            error_report = ErrorReportForStudyNote.objects.get(pk=error_report_pk)

            if request.user.is_authenticated:
                error_report.delete()
                return Response(
                    {"message": "delete ErrorReport success"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "에러 노트를 삭제 할수 없습니다 로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except ErrorReportForStudyNote.DoesNotExist:
            print("ErrorReport is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateViewForErrorReport(APIView):
    def put(self, request, error_report_pk):
        try:
            contentForUpdate = request.data.get("content")
            answer = ErrorReportForStudyNote.objects.get(pk=error_report_pk)

            if request.user.is_authenticated:
                writer = request.user
                # todo commentPk 에 해당하는 answer 의 content 를 위에서 얻은 content 로 수정
                answer.content = contentForUpdate
                answer.save()

                # todo 적당한 http 응답 message 는 comment update success
                return Response(
                    {"message": "ErrorReport content update success"},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except ErrorReportForStudyNote.DoesNotExist:
            print("ErrorReport is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateViewForErrorRecordForNote(APIView):
    def get_object(self, study_note_pk):
        try:
            return StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, study_note_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # study_note_pk에 해당하는 StudyNote 가져오기
        study_note = self.get_object(study_note_pk)

        serializer = SerializerForCreateErrorReportForNote(data=request.data)

        if serializer.is_valid():
            try:
                question = serializer.save(
                    writer=request.user, study_note=study_note
                )  # study_note 정보 추가
                serializer = SerializerForCreateErrorReportForNote(question)
                return Response(
                    {"success": True, "result": serializer.data}, status=HTTP_200_OK
                )
            except Exception as e:
                print("e: ", e)
                raise ParseError(
                    "An error occurred while serializing the create question data"
                )
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class ErrorReportForStudyNoteView(APIView):
    # pagination 관련 전역 변수 선언
    totalErrorReportCount = 0
    perPage = 3
    errorReportList = []

    def get(self, request, study_note_pk):
        # pageNum 초기화
        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
        except ValueError:
            pageNum = 1
        print("pageNum : ", pageNum)

        # self.listForFaqBoard = list_for_suggestion

        try:
            # 해당 노트 찾기
            study_note = StudyNote.objects.get(pk=study_note_pk)
            error_report_list = study_note.error_report_list.all()

            # 클래스 변수 초기화 하기
            self.errorReportList = error_report_list
            self.totalErrorReportCount = error_report_list.count()

            # faq 목록 범위 지정 하기
            start = (pageNum - 1) * self.perPage
            end = start + self.perPage
            self.errorReportList = self.errorReportList[start:end]
            # print("start, end : ", start, end)
            # print("faqList : ", self.errorReportList)

            # 시리얼라이징 하기
            serializer = ErrorReportForStudyNoteSerializer(
                self.errorReportList, many=True
            )

            # 응답할 딕셔너리 만들기
            response_data = {
                "errorReportList": serializer.data,
                "totalErrorReportCount": self.totalErrorReportCount,
                "perPage": self.perPage,
            }

            print("response_data : ", response_data)

            # 응답은 요렇게
            return Response(response_data, status=HTTP_200_OK)

        except StudyNote.DoesNotExist:
            return Response(
                {"error": "StudyNote not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ErrorReportForPageForStudyNoteView(APIView):
    def get(self, request, study_note_pk, page):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
            error_report_list = study_note.error_report_list.filter(page=page)

            print("error_report_list : ", error_report_list)

            serializer = ErrorReportForStudyNoteSerializer(error_report_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudyNote.DoesNotExist:
            return Response(
                {"error": "StudyNote not found."}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteViewForCommentForQuestionForNote(APIView):
    def delete(self, request, commentPk):
        try:
            comment = AnswerForQaBoard.objects.get(pk=commentPk)
            comment.delete()
            return Response(
                {"message": "Comment deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except AnswerForQaBoard.DoesNotExist:
            return Response(
                {"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateViewForCommentForQuestionForNote(APIView):
    def put(self, request, commentPk):
        try:
            contentForUpdate = request.data.get("content")
            answer = AnswerForQaBoard.objects.get(pk=commentPk)

            if request.user.is_authenticated:
                writer = request.user
                # todo commentPk 에 해당하는 answer 의 content 를 위에서 얻은 content 로 수정
                answer.content = contentForUpdate
                answer.save()

                # todo 적당한 http 응답 message 는 comment update success
                return Response(
                    {"message": "Comment update success"}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except AnswerForQaBoard.DoesNotExist:
            print("AnswerForQaBoard is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateViewForCommentForQuestionForNote(APIView):
    def post(self, request, question_pk):
        try:
            question = QnABoard.objects.get(pk=question_pk)
            content = request.data.get("content")

            if request.user.is_authenticated:
                writer = request.user

                if content:
                    answer = AnswerForQaBoard(
                        question=question, content=content, writer=writer
                    )
                    answer.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    print("content 가 없습니다")
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except QnABoard.DoesNotExist:
            print("qa board is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteViewForQuestionBoard(APIView):
    def delete(self, request, question_pk):
        try:
            question = QnABoard.objects.get(pk=question_pk)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QnABoard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateViewForQnABoard(APIView):
    def get_object(self, question_pk):
        try:
            return QnABoard.objects.get(pk=question_pk)
        except QnABoard.DoesNotExist:
            raise NotFound

    def put(self, request, question_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        print("question_pk !!!!!!!!!!!!! : ", question_pk)
        qna_board = self.get_object(question_pk)
        if qna_board.writer != request.user:
            raise PermissionDenied

        # 업데이트할 데이터 받기
        title = request.data.get("title")
        content = request.data.get("content")
        page = request.data.get("page")

        # 필요한 필드 업데이트
        qna_board.title = title
        qna_board.content = content
        qna_board.page = page
        qna_board.updated_at = timezone.now()

        # 저장
        qna_board.save()

        return Response(status=status.HTTP_200_OK)


class CreateViewForQnABoard(APIView):
    def get_object(self, study_note_pk):
        try:
            return StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, study_note_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # study_note_pk에 해당하는 StudyNote 가져오기
        study_note = self.get_object(study_note_pk)

        serializer = SerializerForCreateQuestionForNote(data=request.data)

        if serializer.is_valid():
            try:
                question = serializer.save(
                    writer=request.user, study_note=study_note
                )  # study_note 정보 추가
                serializer = SerializerForCreateQuestionForNote(question)
                return Response(
                    {"success": True, "result": serializer.data}, status=HTTP_200_OK
                )
            except Exception as e:
                print("e: ", e)
                raise ParseError(
                    "An error occurred while serializing the create question data"
                )
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)


# list view:
# SuggestionView


class ListViewForSuggestion(APIView):
    totalSuggestionCount = 0
    perPage = 5
    suggestionList = []

    def get(self, request, study_note_pk):
        # page 번호 받기
        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
            print(pageNum)
        except ValueError:
            pageNum = 1

        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        # 검색어 가져오기
        search_words = request.query_params.get("searchWords", "")
        # 해당 노트에 대한 faq 목록 가져오기

        suggestion_list = study_note.suggestion_list.all()

        if search_words:
            # print("search_words : ", search_words)
            suggestion_list = suggestion_list.filter(title__icontains=search_words)

        self.suggestionList = suggestion_list

        # 총 개수 초기화 하기
        self.totalSuggestionCount = suggestion_list.count()
        # print("totalSuggestionCount : ", self.totalSuggestionCount)

        # list 범위 지정 하기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.suggestionList = self.suggestionList[start:end]
        # print("start, end : ", start, end)
        # print("suggestionList : ", self.suggestionList)

        # 시리얼라이징 하기
        serializer = SuggestionSerializer(self.suggestionList, many=True)

        # 응답용 딕셔너리 선언
        response_data = {
            "suggestionList": serializer.data,
            "totalSuggestionCount": self.totalSuggestionCount,
            "perPage": self.perPage,
        }
        # print("response_data for suggestion ::::::::::::::::", response_data)

        return Response(response_data, status=HTTP_200_OK)


class FAQBoardView(APIView):
    totalFaqCount = 0
    perPage = 3
    faqList = []

    def get(self, request, study_note_pk):
        # page 번호 받기
        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
            print(pageNum)
        except ValueError:
            pageNum = 1

        try:
            # 해당 노트 찾기
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        # 검색어 가져오기
        search_words = request.query_params.get("searchWords", "")
        # 해당 노트에 대한 faq 목록 가져오기

        study_note_list = study_note.faq_list.all()

        if search_words:
            # print("search_words : ", search_words)
            study_note_list = study_note_list.filter(title__icontains=search_words)

        self.faqList = study_note_list

        # 총 개수 초기화 하기
        self.totalFaqCount = study_note_list.count()
        # print("totalFaqCount : ", self.totalFaqCount)

        # faq 목록 범위 지정 하기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.faqList = self.faqList[start:end]
        # print("start, end : ", start, end)
        # print("faqList : ", self.faqList)

        # 시리얼라이징 하기
        serializer = FAQBoardSerializer(self.faqList, many=True)

        # return Response(serializer.data, status=status.HTTP_200_OK)
        response_data = {
            "faqList": serializer.data,
            "totalFaqCount": self.totalFaqCount,
            "perPage": self.perPage,
        }

        return Response(response_data, status=HTTP_200_OK)


class QnABoardView(APIView):
    # pagination 관련 변수 선언
    totalQaCount = 0
    perPage = 3
    qaList = []

    def get(self, request, study_note_pk):
        # page 번호 받기
        try:
            pageNum = request.query_params.get("pageNum", 1)
            pageNum = int(pageNum)
            print(pageNum)
        except ValueError:
            pageNum = 1

        print("pageNum ::::::::::::::::???????", pageNum)

        try:
            # 해당 노트 가져 오기
            study_note = StudyNote.objects.get(pk=study_note_pk)

        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        # 해당 노트에 대한 qa list 가져 오기
        study_note_list = QnABoard.objects.filter(study_note=study_note)

        # 전역 변수 초기화
        self.qaList = study_note_list
        self.totalQaCount = study_note_list.count()

        # qa list 범위 설정
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.qaList = self.qaList[start:end]

        serializer = QnABoardSerializer(self.qaList, many=True)

        # 응답 딕셔너리 선언 for pagination
        response_data = {
            "qaList": serializer.data,
            "totalQaCount": self.totalQaCount,
            "perPage": self.perPage,
        }

        # response 수정
        # from return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)


class GetSavedPageForCurrentNote(APIView):
    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        # todo
        # login 안했으면 로그인 사용자가 아닐 경우 저장된 페이지를 불러 올수 없습니다라고 메세지 응답
        if not request.user.is_authenticated:
            print("비로그인 유저에 대한 체크 실행 !")
            return Response(
                "Please log in to retrieve the saved page",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        existing_class_room = ClassRoomForStudyNote.objects.filter(
            current_note=study_note, writer=request.user
        ).exists()

        if existing_class_room:
            class_room = ClassRoomForStudyNote.objects.filter(
                current_note=study_note, writer=request.user
            ).first()
            current_page = class_room.current_page  # class_room.current_page를 변수로 추출
            print("current_page : ", current_page)
            return Response({"current_page": current_page}, status=status.HTTP_200_OK)
        else:
            return Response("saved_data is not exist", status=status.HTTP_404_NOT_FOUND)


class ClasssRoomView(APIView):
    def get_object(self, taskPk):
        try:
            return StudyNote.objects.get(pk=taskPk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def get(self, request, study_note_pk):
        print("로그인 여부 확인 : ", request.user.is_authenticated)
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        class_list = study_note.class_list.all()

        # todo class_list 에 writer 가 request.user인게 하나 이상 있는 경우 is_registered true 를  response_data 에 담은뒤 Response 로 응답

        is_registered = False  # 기본적으로 False로 설정

        for class_room in class_list:
            if class_room.writer == request.user:
                is_registered = True
                break

        serializer = ClassRoomForStudyNoteSerializer(
            class_list, many=True, context={"request": request}
        )

        response_data = {
            "is_registered": is_registered,
            "class_room_list": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, study_note_pk):
        try:
            study_note = self.get_object(study_note_pk)
        except StudyNote.DoesNotExist:
            print("여기 실행 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_authenticated:
            return Response("Please log in", status=status.HTTP_401_UNAUTHORIZED)

        writer = request.user
        current_page = int(request.data.get("current_page"))

        # Check if a ClassRoomForStudyNote already exists with current_note=study_note
        existing_class_room = ClassRoomForStudyNote.objects.filter(
            current_note=study_note, writer=request.user
        ).exists()

        if existing_class_room:
            existing_class_room = ClassRoomForStudyNote.objects.filter(
                current_note=study_note, writer=request.user
            ).first()
            if existing_class_room.current_page != current_page:
                print("original : ", existing_class_room.current_page)
                print("current_page : ", current_page)
                print("original type: ", type(existing_class_room.current_page))
                print("current_page type: ", type(current_page))
                existing_class_room.current_page = current_page
                existing_class_room.save()

                response_data = {"save_page_num": current_page}

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                print("페이지 번호가 다르지 않습니다")
        # update
        if existing_class_room:
            return Response(
                {
                    "message_type": "warnning",
                    "message": "The record for the current page already exists, so it will not be updated",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("excute check !!")

        class_room = ClassRoomForStudyNote.objects.create(
            current_note=study_note, current_page=current_page, writer=writer
        )

        response_data = {"save_page_num": current_page}

        return Response(response_data, status=status.HTTP_201_CREATED)


class UpdateViewForStudyNoteComment(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def put(self, request, commentPk):
        print("put 요청 확인")
        print("request.data.get(comment) : ", request.data.get("comment"))
        comment_obj = self.get_object(commentPk)
        comment_obj.comment = request.data.get("comment")
        comment_obj.is_edit_mode = False
        comment_obj.save()

        result_data = {
            "success": True,
            "message": "comment text update success",
        }

        return Response(result_data, status=HTTP_200_OK)


class CreateViewForCommentForNote(APIView):
    def get_object(self, taskPk):
        try:
            return StudyNote.objects.get(pk=taskPk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, studyNotePk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = CreateCommentSerializerForNote(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                # original_task = self.get_object(taskPk)
                test_for_task = serializer.save(writer=request.user)
                serializer = CreateCommentSerializerForNote(test_for_task)

                return Response(
                    {"success": "true", "result": serializer.data}, status=HTTP_200_OK
                )
            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task"
                )
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)


class DeleteViewForStudyNoteComment(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def delete(self, request, commentPk):
        comment_obj = self.get_object(commentPk)
        comment_obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class UpdateViewForEditModeForStudyNoteBriefingBoard(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def put(self, request, commentPk):
        print("put 요청 확인")
        message = ""
        comment = self.get_object(commentPk)

        if comment.is_edit_mode:
            comment.is_edit_mode = False
            message = "edit mode to read mode"

        else:
            comment.is_edit_mode = True
            message = "from read mode to edit mode"

        comment.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class ListViewForStudyNoteBriefingBoard(APIView):
    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                "StudyNote does not exist", status=status.HTTP_404_NOT_FOUND
            )

        briefing_boards = study_note.note_comments.all()
        serializer = StudyNoteBriefingBoardSerializer(briefing_boards, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiViewForGetSubtitleListForNote(APIView):
    def get(self, request, study_note_pk):
        # study_note_pk(StudyNote의 id임)를 참조하는 StudyNoteContent 리스트를 가져옴
        note_contents = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, content_option="subtitle_for_page"
        ).order_by("page")

        # 시리얼라이저로 응답 데이터 직렬화
        serializer = StudyNoteContentSerializer(note_contents, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateViewForYoutubeContentForNote(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        content_option = request.data["content_option"]
        title = request.data["title"]
        youtube_url = request.data["youtube_url"]

        max_order = (
            StudyNoteContent.objects.filter(
                study_note_id=study_note_pk, page=current_page_number
            ).aggregate(Max("order"))["order__max"]
            or 0
        )

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            page=current_page_number,
            order=max_order + 1,  # 이전 order 값 중 최대값에 1을 더하여 설정
            writer=request.user,  # 작성자는 현재 요청한 유저로 설정
            content_option=content_option,
            title=title,
            youtube_url=youtube_url,
        )

        print("note_content : ", note_content)

        return Response(
            {"message": "youtube content is created successfuly"},
            status=status.HTTP_201_CREATED,
        )


class CreateViewForSubTitleForNote(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        content_option = request.data["content_option"]
        title = request.data["title"]
        ref_url1 = request.data["ref_url1"]
        ref_url2 = request.data["ref_url2"]
        content = request.data["content"]
        youtube_url = request.data["youtube_url"]

        print("content_option : ", content_option)
        # 이미 sub title for page가 존재하는지 확인
        existing_subtitle = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk,
            page=current_page_number,
            content_option="subtitle_for_page",
        ).exists()

        if existing_subtitle:
            return Response(
                {
                    "message": "If a sub title for the page already exists, The note will not be updated"
                },
                status=status.HTTP_201_CREATED,
            )

        # 이전 order 값 중 최소값 구하기
        min_order = (
            StudyNoteContent.objects.filter(
                study_note_id=study_note_pk, page=current_page_number
            ).aggregate(Min("order"))["order__min"]
            or 0
        )

        # 기존의 min_order가 1인 경우, 기존의 order를 모두 +1 증가
        if min_order == 1:
            StudyNoteContent.objects.filter(
                study_note_id=study_note_pk, page=current_page_number
            ).update(order=models.F("order") + 1)

        if min_order > 1:
            order_for_update = min_order - 1
        else:
            order_for_update = 1

        # Create StudyNoteContent model
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            page=current_page_number,
            content_option=content_option,
            writer=request.user,  # Set the current user as the writer
            order=order_for_update,  # Set the order value
            title=title,
            ref_url1=ref_url1,
            ref_url2=ref_url2,
            content=content,
        )

        # Save youtube_url only if it is not empty
        if youtube_url != "":
            note_content.youtube_url = youtube_url
            note_content.save()

        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)


class ApiViewForCoWriter(APIView):
    def delete(self, request, co_writer_pk):
        try:
            co_writer = CoWriterForStudyNote.objects.get(pk=co_writer_pk)
        except CoWriterForStudyNote.DoesNotExist:
            return Response(
                {"message": "CoWriterForStudyNote does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        co_writer.delete()

        return Response(
            {"message": "CoWriterForStudyNote has been deleted successfully."},
            status=status.HTTP_200_OK,
        )


class CreateViewForCoWriterForOhterUserNote(APIView):
    def post(self, request, notePk):
        try:
            study_note = StudyNote.objects.get(pk=notePk)
        except StudyNote.DoesNotExist:
            return Response(
                {"message": "StudyNote does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if study_note.writer == request.user:
            return Response(
                {
                    "message": "You cannot request to be a co-writer for your own StudyNote."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        co_writer, created = CoWriterForStudyNote.objects.get_or_create(
            writer=request.user, study_note=study_note
        )

        if created:
            message = f"{request.user.username}님의 StudyNote에 대한 CoWriter 요청이 성공하였습니다."
        else:
            message = f"{request.user.username}님은 이미 이 StudyNote의 CoWriter입니다."

        return Response({"message": message}, status=status.HTTP_201_CREATED)


class UpdateViewForIsApprovedForCoWorker(APIView):
    def get_cowriter_obj(self, pk):
        try:
            return CoWriterForStudyNote.objects.get(pk=pk)
        except CoWriterForStudyNote.DoesNotExist:
            print("note found !!!!!!!!!!!!!!!!!!!!!!!!")
            raise NotFound

    def post(self, request):
        print("UpdateViewForIsApprovedForCoWorker ?????")
        pass

    def put(self, request):
        print("update-is-approved-for-cowriter for check !!!!!!!!!!!!!!!!!")
        # Use the same key "cowriterPk" as sent from the frontend
        cowriter_pk = request.data.get("cowriterPk")

        cowirter = self.get_cowriter_obj(pk=cowriter_pk)

        # 업데이트할 값 설정 후 save()
        if cowirter.is_approved:
            message = "승인에서 비승인으로 update"
            cowirter.is_approved = False

        else:
            message = "비승인에서 승인으로 update"
            cowirter.is_approved = True

        cowirter.save()

        result_data = {"success": True, "message": message}

        return Response(result_data, status=HTTP_200_OK)


class CopyCopySelectedNotesToMyNoteView(APIView):
    def post(self, request):
        selectedRowPksFromOriginalTable = request.data.get(
            "selectedRowPksFromOriginalTable"
        )
        print(
            "selectedRowPksFromOriginalTable : ", selectedRowPksFromOriginalTable
        )  # [17,18] <=> StudyNote의 pk

        with transaction.atomic():
            try:
                user = request.user

                # selectedRowPksFromOriginalTable에 해당하는 StudyNote 모델 데이터 복사 및 StudyNoteContent 생성
                for original_pk in selectedRowPksFromOriginalTable:
                    original_study_note = StudyNote.objects.get(pk=original_pk)

                    # StudyNote 복사
                    new_study_note = StudyNote.objects.create(
                        title=original_study_note.title,
                        description=original_study_note.description,
                        writer=user,
                    )

                    # StudyNoteContent 생성
                    original_note_contents = original_study_note.note_contents.all()
                    for original_note_content in original_note_contents:
                        StudyNoteContent.objects.create(
                            study_note=new_study_note,
                            title=original_note_content.title,
                            file_name=original_note_content.file_name,
                            content=original_note_content.content,
                            content_option=original_note_content.content_option,
                            writer=user,
                            order=original_note_content.order,
                            created_at=original_note_content.created_at,
                            page=original_note_content.page,
                        )

                response_data = {
                    "message": "Selected notes copied to my note successfully."
                }

                return Response(response_data, status=HTTP_200_OK)

            except StudyNote.DoesNotExist:
                response_data = {"message": "One or more selected notes do not exist."}

                return Response(response_data, status=HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForCheckedRows(APIView):
    total_page_count = 0  # 노트의 총 개수

    def get(self, request):
        selected_row_pks = request.GET.get("selectedRowPksFromOriginalTable", "").split(
            ","
        )
        print("selected_row_pks :::::::::::::::::::", selected_row_pks)

        all_study_note_list = StudyNote.objects.filter(
            pk__in=selected_row_pks,
        )
        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list

        serializer = StudyNoteSerializer(study_notes, many=True)

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
        }

        return Response(response_data, status=HTTP_200_OK)


class UpdateNoteContentsPageForSelectedView(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, study_note_pk):
        direction = request.data.get("direction")
        pageNumbersToEdit = request.data.get("pageNumbersToEdit")  # 초록색
        pageNumbersToMove = request.data.get("pageNumbersToMove")  # 주황색

        try:
            with transaction.atomic():
                study_note = self.get_object(study_note_pk)  # 특정 노트
                study_note_contents = study_note.note_contents.all()  # 모든 노트

                if direction == "forward":
                    for content in study_note_contents:
                        if content.page in pageNumbersToEdit:
                            new_page = pageNumbersToMove[
                                pageNumbersToEdit.index(content.page)
                            ]
                            content.page = new_page
                            content.created_at = timezone.now()
                            content.save()

                elif direction == "backward":
                    for content in study_note_contents:
                        if content.page in pageNumbersToMove:
                            new_page = pageNumbersToEdit[
                                pageNumbersToMove.index(content.page)
                            ]
                            content.page = new_page
                            content.save()

                elif direction == "switch":
                    for edit_page, move_page in zip(
                        pageNumbersToEdit, pageNumbersToMove
                    ):
                        edit_contents = study_note_contents.filter(page=edit_page)
                        move_contents = study_note_contents.filter(page=move_page)

                        if edit_contents.count() == move_contents.count() == 1:
                            edit_content = edit_contents.first()
                            move_content = move_contents.first()

                            edit_content.page, move_content.page = move_page, edit_page
                            edit_content.save()
                            move_content.save()

                elif direction == "add_whitespace":
                    max_page = 0  # 초기값 설정

                    if pageNumbersToEdit:
                        max_page = max(max_page, max(pageNumbersToEdit))

                    # 공백 만들 페이지 이후의 번호를 a만큼 증가시킴
                    a = len(pageNumbersToEdit)
                    for content in study_note_contents:
                        if content.page > max_page:
                            content.page += a
                            content.save()

                    # pageNumbersToEdit의 페이지도 a만큼 증가시킴
                    for page_num in pageNumbersToEdit:
                        contents_to_update = study_note_contents.filter(page=page_num)
                        for content in contents_to_update:
                            content.page += a
                            content.save()

                elif direction == "insert":
                    max_page = 0  # 초기값 설정

                    if pageNumbersToEdit:
                        max_page = max(max_page, max(pageNumbersToEdit))

                    # 모든 페이지 번호를 a만큼 증가시킴
                    a = len(pageNumbersToEdit)
                    for content in study_note_contents:
                        if content.page > max_page:
                            content.page += a
                            content.save()

                    # pageNumbersToEdit의 페이지도 a만큼 증가시킴
                    for page_num in pageNumbersToEdit:
                        contents_to_update = study_note_contents.filter(page=page_num)
                        for content in contents_to_update:
                            content.page += a
                            content.save()

                    # pageNumbersToMove 의 모든 요소들을 a 만큼 더함
                    pageNumbersToMove = [x + a for x in pageNumbersToMove]

                    for content in study_note_contents:
                        if content.page in pageNumbersToMove:
                            new_page = pageNumbersToEdit[
                                pageNumbersToMove.index(content.page)
                            ]
                            content.page = new_page
                            content.save()

                if direction == "forward":
                    message = f"{pageNumbersToEdit}를 pageNumbersToMove로 이동 성공"
                elif direction == "backward":
                    message = f"pageNumbersToMove를 {pageNumbersToEdit}로 이동 성공"
                elif direction == "switch":
                    message = f"{pageNumbersToEdit} <=> {pageNumbersToMove} 교체 성공"
                elif direction == "add_whitespace":
                    message = f"{pageNumbersToEdit} 공백 만들기 성공"
                elif direction == "insert":
                    message = f"공백 만들기 + 끼워 넣기 성공"

                response_data = {
                    "message": message,
                    "direction": direction,
                }

                return Response(data=response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                data={"message": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StudyNoteContentReOrderAPIView(APIView):
    def put(self, request, pk):
        try:
            study_note_contents = StudyNoteContent.objects.filter(study_note__pk=pk)

            print("study_note_contents : ", study_note_contents)

            reordered_contents_list = request.data.get("reordered_contents_list", [])
            print("reordered_contents_list : ", reordered_contents_list)

            for item in reordered_contents_list:
                pk_for_update = item["content_pk"]
                order_for_update = item["order"]

                print(
                    "pk_for_update, order_for_update : ",
                    pk_for_update,
                    order_for_update,
                )

                study_note_content = study_note_contents.get(pk=pk_for_update)
                study_note_content.order = order_for_update
                study_note_content.save()

            # study_note_contents = StudyNoteContent.objects.filter(
            #     study_note__pk=pk, page=1)

            print("study_note_contents : ", study_note_contents)

            # serializer = StudyNoteContentSerializer(study_note_content, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"success": "Study note content order updated successfully."},
                status=status.HTTP_200_OK,
            )

        except StudyNoteContent.DoesNotExist:
            return Response(
                {"error": "Study note content does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


class SearchContentListView(APIView):
    def get(self, request):
        study_note_pk = request.query_params.get("study_note_pk")
        search_term = request.query_params.get("searchTerm")

        print("search_term : ", search_term)

        # 필요한 로직 수행
        queryset = StudyNoteContent.objects.filter(study_note=study_note_pk)

        print("queryset : ", queryset)

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(content__icontains=search_term)
            )
        print("queryset2 : ", queryset)

        serializer = StudyNoteContentSerializer(queryset, many=True)

        print("serializer.data : ", serializer.data)

        return Response(serializer.data)


class DeleteNoteContentsForChecked(APIView):
    def delete(self, request):
        username = request.data.get("username")  # 'username' 값 받기
        pageNumbersToEdit = request.data  # [1, 2, 3, 5]
        print("pageNumbersToEdit : ", pageNumbersToEdit)

        # username에 해당하는 User 객체 가져오기
        writer = User.objects.get(username=username)

        deleted_count = StudyNoteContent.objects.filter(
            writer=writer, pk__in=pageNumbersToEdit
        ).delete()[0]

        return Response(
            {"message": f"{deleted_count} StudyNoteContent instances deleted."}
        )


class order_plus_one_for_note_content(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, content_pk):
        # 해당하는 객체 찾기
        content = get_object_or_404(StudyNoteContent, pk=content_pk)

        # 먼저 +1 인거 -1 처리
        # order 값이 증가된 객체보다 큰 값을 가지는 다른 객체들의 order 값을 1씩 감소시키기
        other_content = StudyNoteContent.objects.get(
            study_note=content.study_note, order=content.order + 1
        )

        study_note = self.get_object(content.study_note.pk)
        note_contents_after_order_update = study_note.note_contents.filter(
            page=content.page
        ).order_by("order")

        # order 값을 1 증가시키고 저장
        content.order += 1
        content.save()

        other_content.order -= 1
        other_content.save()

        serializer = StudyNoteContentSerializer(
            note_contents_after_order_update, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class order_minus_one_for_note_content(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, content_pk):
        # 해당하는 객체 찾기
        content = get_object_or_404(StudyNoteContent, pk=content_pk)

        # 먼저 +1 인거 -1 처리
        # order 값이 증가된 객체보다 큰 값을 가지는 다른 객체들의 order 값을 1씩 감소시키기
        other_content = StudyNoteContent.objects.get(
            study_note=content.study_note, order=content.order - 1
        )
        other_content.order += 1
        other_content.save()

        study_note = self.get_object(content.study_note.pk)
        note_contents_after_order_update = study_note.note_contents.filter(
            page=content.page
        ).order_by("order")

        # order 값을 1 증가시키고 저장
        content.order -= 1
        content.save()

        serializer = StudyNoteContentSerializer(
            note_contents_after_order_update, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudyNoteContentView(APIView):
    def delete(self, request, content_pk):
        try:
            content = StudyNoteContent.objects.get(pk=content_pk)
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudyNoteContent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, content_pk, format=None):
        study_note_content = StudyNoteContent.objects.get(pk=content_pk)

        study_note_content.title = request.data.get("title", study_note_content.title)
        study_note_content.file_name = request.data.get(
            "file_name", study_note_content.file_name
        )
        study_note_content.content = request.data.get(
            "content", study_note_content.content
        )

        study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class StudyNoteContentsView(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        title = request.data["title"]
        file = request.data["file"]
        content = request.data["content"]
        content_option = request.data["content_option"]
        print("content_option : ", content_option)

        # 이전 order 값 중 최대값 구하기
        max_order = (
            StudyNoteContent.objects.filter(
                study_note_id=study_note_pk, page=current_page_number
            ).aggregate(Max("order"))["order__max"]
            or 0
        )

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            title=title,
            file_name=file,
            content_option=content_option,
            content=content,
            writer=request.user,  # 작성자는 현재 요청한 유저로 설정
            page=current_page_number,
            order=max_order + 1,  # 이전 order 값 중 최대값에 1을 더하여 설정
        )
        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)


class PlusOnePageForSelectedPageForStudyNoteContents(APIView):
    def put(self, request, study_note_pk):
        pageNumbersToEdit = request.data.get("pageNumbersToEdit", [])
        print("pageNumbersToEdit : ", pageNumbersToEdit)
        # pageNumbersToEdit 는 [1,2,3,5] 와 같이 리스트 형태로 넘어옵니다.

        # 선택된 StudyNote의 StudyNoteContent들의 page를 +1 해줍니다.
        study_note_contents = StudyNoteContent.objects.filter(
            study_note__pk=study_note_pk, page__in=pageNumbersToEdit
        )
        for study_note_content in study_note_contents:
            study_note_content.page += 1
            study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class MinusOnePageForSelectedPageForStudyNoteContents(APIView):
    def put(self, request, study_note_pk):
        pageNumbersToEdit = request.data.get("pageNumbersToEdit", [])
        print("pageNumbersToEdit : ", pageNumbersToEdit)
        # selected_buttons_data 는 [1,2,3,5] 와 같이 리스트 형태로 넘어옵니다.

        # 선택된 StudyNote의 StudyNoteContent들의 page를 +1 해줍니다.
        study_note_contents = StudyNoteContent.objects.filter(
            study_note__pk=study_note_pk, page__in=pageNumbersToEdit
        )
        for study_note_content in study_note_contents:
            study_note_content.page -= 1
            study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class DeleteNoteContentsForSelectedPage(APIView):
    def delete(self, request, study_note_pk):
        selected_buttons_data = request.data

        StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, page__in=selected_buttons_data
        ).delete()

        message = "노트에 대해  {} 페이지 삭제 완료".format(selected_buttons_data)

        return Response({"message": message})


class StudyNoteAPIView(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 4  # 1 페이지에 몇개씩
    all_note_list = []

    def getAllNoteList(self):
        note_obj = StudyNote.objects.all()
        return note_obj

    def get_all_note_list_filtered(
        self, selected_note_writer, first_category, second_category
    ):
        filter_conditions = Q()
        if selected_note_writer != "":
            filter_conditions &= Q(writer__username=selected_note_writer)
        if first_category != "":
            filter_conditions &= Q(first_category=first_category)
        if second_category != "":
            filter_conditions &= Q(second_category=second_category)

        return StudyNote.objects.filter(filter_conditions)  # 필터링된 데이터를 반환

    def get(self, request):
        print("노트 요청 여기 맞지?? ")

        selected_note_writer = request.query_params.get("selectedNoteWriter", "")
        first_category = request.query_params.get("first_category", "")
        second_category = request.query_params.get("second_category", "")

        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        filtered_note_list = self.get_all_note_list_filtered(
            selected_note_writer, first_category, second_category
        )
        self.total_page_count = filtered_note_list.count()
        paginated_notes = filtered_note_list[start:end]

        print("request.user.username : ", request.user)

        serializer = StudyNoteSerializer(
            paginated_notes, many=True, context={"request": request}
        )

        # all_study_note_list_for_users = paginated_notes
        note_writers = list(set(note.writer.username for note in paginated_notes))

        response_data = {
            "note_writers": note_writers,  # Include the note writers in the response
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page,
        }

        return Response(response_data, status=HTTP_200_OK)

    def post(self, request):
        print("study note post 요청")
        serializer = StudyNoteSerializer(
            data=request.data, context={"request": request}
        )

        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            errors = serializer.errors
            print("serializer errors:", errors)  # 에러 출력
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print("put 요청 check !!")
        study_note_pk = request.data.get("study_note_pk")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response(
                {"error": "Study note does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StudyNoteSerializer(
            study_note, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForCopyMode(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 6  # 1 페이지에 몇개씩

    def get(self, request):
        selected_note_writer = request.query_params.get("selectedNoteWriter")

        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # study_notes 데이터중 start, end 에 해당하는 데이터 가져 오기

        if selected_note_writer == "":
            all_study_note_list = StudyNote.objects.filter(
                ~Q(writer__username=request.user.username)
            )
        else:
            all_study_note_list = StudyNote.objects.filter(
                writer__username=selected_note_writer
            )
        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list[start:end]

        serializer = StudyNoteSerializer(
            study_notes, many=True, context={"request": request}
        )

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page,
        }

        return Response(response_data, status=HTTP_200_OK)

    def post(self, request):
        serializer = StudyNoteSerializer(data=request.data)

        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForMe(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 6  # 1 페이지에 몇개씩

    def get(self, request):
        print("all_study_note_list for me check !!!!!!!!!!!!!")
        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # study_notes 데이터중 start, end 에 해당하는 데이터 가져 오기
        all_study_note_list = StudyNote.objects.filter(
            Q(writer__username=request.user.username)
        )

        # print("all_study_note_list For Me :::::::::::::::::", all_study_note_list)

        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list[start:end]

        serializer = StudyNoteSerializer(study_notes, many=True)

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page,
        }

        return Response(response_data, status=HTTP_200_OK)

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

    def get(self, request, notePk, pageNum):
        study_note = self.get_object(notePk)

        question_count_for_current_page = study_note.question_list.filter(
            page=pageNum
        ).count()
        print("question_count_for_current_page:", question_count_for_current_page)
        print("current_page:", pageNum)
        note_contents = study_note.note_contents.filter(page=pageNum).order_by("order")

        filtered_contents = note_contents.filter(content_option="subtitle_for_page")

        if filtered_contents.exists():
            subtitle_for_page = filtered_contents[0].title
        else:
            subtitle_for_page = "no data"

        serializer = StudyNoteContentSerializer(note_contents, many=True)
        data = serializer.data

        total_note_contents = study_note.note_contents.all().order_by("order")

        page_numbers = (
            total_note_contents.values("page")
            .annotate(count=Count("id"))
            .order_by("page")
        )

        exist_page_numbers = [page["page"] for page in page_numbers]

        cowriters = study_note.note_cowriters.all()
        cowriters_data = []

        for cowriter in cowriters:
            if cowriter.is_approved:
                cowriter_data = {
                    "id": cowriter.id,
                    "username": cowriter.writer.username,
                    "profile_image": cowriter.writer.profile_image,
                    "is_tasking": cowriter.is_tasking,
                    "current_page": cowriter.current_page,
                    "task_description": cowriter.task_description,
                }
                cowriters_data.append(cowriter_data)

        # Check if the request user's username is in cowriters_data

        print("cowriters_data : ", cowriters_data)

        authority_for_writing_note_contents = False

        for cowriter in cowriters_data:
            if (
                cowriter["username"] == request.user.username
                and cowriter["is_tasking"] == True
            ):
                authority_for_writing_note_contents = True
                break

        if study_note.writer.username == request.user.username:
            authority_for_writing_note_contents = True

        response_data = {
            "note_title": study_note.title,
            "subtitle_for_page": subtitle_for_page,
            "note_user_name": study_note.writer.username,
            "note_user_profile_image": study_note.writer.profile_image,
            "exist_page_numbers": exist_page_numbers,
            "data_for_study_note_contents": data,
            "co_writers_for_approved": cowriters_data,
            "question_count_for_current_page": question_count_for_current_page,
            "authority_for_writing_note_contents": authority_for_writing_note_contents,
        }

        return Response(response_data, status=HTTP_200_OK)


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
        print("study_notes :", study_notes)

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
