"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Blog')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path('docs/', include_docs_urls(title='BlogAPI')),
    path('api/v1/accounts/', include(('accounts.urls',  'accounts'), namespace="accounts-api")),
    path('api/v1/forum/', include(('forum.urls', 'forum'), namespace='forum-api')),
    path('api/v1/chat/', include(('chat.urls', 'chat'), namespace='chat-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

