
from django.shortcuts import render
from rest_framework import (generics, status)
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

class PipeBaseMaterialGradePriceApiView(generics.RetrieveUpdateAPIView):
    serializer_class = PipeBaseMaterialGradePriceSerializer
    # permission_classes = IsAdmin

    def get_object(self):
        # 자동 견적은 가장 최근 시점의 Base M.G 가격 정보만 필요하기 때문에
        # 시점에 대한 데이터는 저장할 필요가 없음
        # 따라서, static한 데이터 1개를 select 함
        return get_object_or_404(PipeBaseMaterialGradePrice, id=1)
