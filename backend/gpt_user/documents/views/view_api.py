from django.http import StreamingHttpResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# base
from gpt_base.auth.permission_class import IsUserAuthenticated
from gpt_base.documents.models.documents import Templates ,WorkBooks,Documents

# gpt_user
from gpt_user.documents.services.documents import DocumentService

from gpt_user.documents.serializers.documents import (
    TemplateDetailListSerializer,
    TemplateDetailSerializer,
    WorkBookDetailListSerializer,
    DocumentsCreateSerializer,
    DocumentsDetailListSerializer,
    DocumentsUpdateSerializer,
    DocumentsDetailSerializer,
    WorkBooksCreateSerializer,
    WorkBooksUpdateSerializer
)

@extend_schema(
    methods=['POST'],
    tags=['document-template'],
    request=[],
    description="""
    Chat-GPT Process Caller
    
    *Format request sample:
    {
        "prompt": <str>,
        "system_message": <str>,
        "temperature": <float>,
        "top_p": <int>,
        "question_asked" : <str>
    }
    """,
    responses={200: None}
)
@api_view(["POST"])
@permission_classes([IsUserAuthenticated])
def process_generate_document(request):
    documents_service = DocumentService()
    data = request.data
    completion = documents_service.generate_result_completion_member(
        prompt=data.get('prompt'),
        system_message=data.get('system_message'),
        temperature=data.get('temperature'),
        top_p=data.get('top_p'),
        stream=True,
        request_user=request.user,
        question_asked = data.get('question_asked'),
        document_id = ''
    )
    # return Response(data=completion, status=status.HTTP_200_OK) #set stream=False
    return StreamingHttpResponse(completion, content_type='text/event-stream')


@extend_schema(
    methods=['GET'],
    tags=['document-workbook'],
    request=[],
    description="""
    Chat-GPT Process Caller
    
    *Format request sample:
    {
        "workbook_id": <int>,
    }
    """,
    responses={200: None}
)
@api_view(["GET"])
@permission_classes([IsUserAuthenticated])
def get_document_workbook(request):
    workbook_id = request.GET['workbook_id']
    response = Response()
    queryset = Documents.objects.filter(workbook_id = workbook_id) 
    serializer = DocumentsDetailListSerializer(queryset , many = True)
    response.data = {
        'data' : serializer.data , 'status' : status.HTTP_200_OK
    }
    response.status_code = status.HTTP_200_OK
    return response

