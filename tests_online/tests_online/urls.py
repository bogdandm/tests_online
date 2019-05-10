import json

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Tests Online",
        default_version='v1',
        description=""
    ),
    url=settings.SWAGGER_SETTINGS["DEFAULT_API_URL"],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

apipatterns = [
    path('auth/', include('auth.urls')),
    path('', include('questions.urls')),
]

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^apidocs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^apidocs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
    path('api/v1/', include(apipatterns)),
]

if settings.DEBUG:
    # Some dev's views
    import debug_toolbar
    from rest_framework.decorators import api_view
    from rest_framework.response import Response


    @api_view(http_method_names=["GET"])
    def echo(request):
        return Response(request.GET)


    @api_view(http_method_names=["GET"])
    def error(request):
        raise Exception(request.GET)


    def json_default(value):
        if hasattr(value, '__dict__'):
            return value.__dict__
        else:
            return str(value)


    @api_view(http_method_names=["GET"])
    def debug_info(request):
        def dump(data):
            return json.loads(json.dumps(data, default=json_default))

        return Response({
            "auth": dump(request.auth),
            "user": dump(request.user),
            "request.user.is_authenticated": request.user.is_authenticated
        })


    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('api/v1/debug/echo/', echo),
        path('api/v1/debug/500/', error),
        path('api/v1/debug/info/', debug_info)
    ]

admin.autodiscover()
admin.site.site_header = _('Tests Online admin page')
