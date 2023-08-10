from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gingerit.gingerit import GingerIt

@api_view(['GET'])
def check_grammarly(request):
    response = Response()
    try:
        text = request.GET['text_check']
        data = {
            "suggestion" : GingerIt().parse(text)
        }
        response.data = data
        response.status_code = status.HTTP_200_OK
    except:
        response.data = { "error" : "Infomation wrong"}
        response.status_code = status.HTTP_404_NOT_FOUND
    return response