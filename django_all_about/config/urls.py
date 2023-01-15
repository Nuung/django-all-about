from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("", include("django_prometheus.urls")),  # for prometheus
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),  # DRF browsable API
    # 임시 및 테스트(유닛 테스트 아님) 관련 모든 API
    path("api/test/", include("apis.test.urls")),
    # user 관련 모든 API
    path("api/user/", include("apis.user.urls")),
    # products 관련 모든 API
    path("api/products/", include("apis.products.urls")),
    # orders 관련 모든 API
    path("api/orders/", include("apis.orders.urls")),
]

# ==================================================================== #
# DEBUG 일때만 swagger, URL patterns 추가해서 사용
# ==================================================================== #

schema_view = get_schema_view(
    openapi.Info(
        title="Django All About (@Nuung) rest API",
        default_version="v1.0.1",
        description="Django All About (@Nuung) rest API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="Nuung", email="qlgks1@naver.com"),
        license=openapi.License(name="Private License"),
    ),
    public=True,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        re_path(r"__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    SHOW_TOOLBAR_CALLBACK = True
