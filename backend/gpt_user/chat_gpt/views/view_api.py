from django.http import StreamingHttpResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# base
from gpt_base.auth.permission_class import IsUserAuthenticated
# gpt_user
from gpt_user.chat_gpt.services.chat_gpt import ChatGPTService


@extend_schema(
    methods=['POST'],
    tags=['chat-gpt'],
    request=[],
    description="""
    Chat-GPT Process Caller
    
    *Format request sample:
    {
        "conversation_id": <str>,
        "chat_id": <str>,
        "prompt": <str>,
        "system_message": <str>,
        "temperature": <float>,
        "top_p": <int>
    }
    ____________
    *Example:
    {
        "conversation_id": 1
        "chat_id": 1
        "prompt": "hi",
        "system_message": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
        "temperature": 0.8,
        "top_p": 1
    }
    """,
    responses={200: None}
)
@api_view(["POST"])
@permission_classes([IsUserAuthenticated])
def process(request):
    gpt_service = ChatGPTService()
    data = request.data
    completion = gpt_service.chat_completion_member(
        conversation_id=data.get('conversation_id', 2),
        chat_id=data.get('chat_id'),
        prompt=data.get('prompt'),
        system_message=data.get('system_message'),
        temperature=data.get('temperature'),
        top_p=data.get('top_p'),
        stream=True,
        request_user=request.user
    )
    # return Response(data=completion, status=status.HTTP_200_OK) #set stream=False
    return StreamingHttpResponse(completion, content_type='text/event-stream')


