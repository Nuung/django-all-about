
# django, drf lib
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# app lib
from apis.test.tasks import check_registration_number_from_hometax

@swagger_auto_schema(
    method='GET', 
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description='검색할 사업자 등록 번호', required=True, default="", type=openapi.TYPE_STRING),
    ]
)  
@api_view(('GET',))
def check_registration_number(request: Request):
    """
    - query에서 list로 넘어온 사업자 등록 번호들을 폐업 여부를 체크하는 API
    """
    qry = request.GET.get("query")
    if not qry:
        return Response(status=status.HTTP_204_NO_CONTENT)

    qry_list = qry.split(",")
    for registration_number in qry_list:
        registration_number = registration_number.strip()
        check_registration_number_from_hometax.apply_async(args=[registration_number], kwargs={})
    
    return Response(
        dict(success=True, message="사업자 등록 번호를 조회합니다. 결과는 admin에서 확인해 주세요"),
        status=status.HTTP_200_OK
    )