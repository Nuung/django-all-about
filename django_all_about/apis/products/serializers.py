
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _

# from api.v2.product.models import PipeBaseMaterialGradePrice, PipeMaterialGradePrice, PipeSizeThicknessPrice

# class PipeBaseMaterialGradePriceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PipeBaseMaterialGradePrice
#         exclude = ("id", )
#         read_only_fields = ("updated_at", )
