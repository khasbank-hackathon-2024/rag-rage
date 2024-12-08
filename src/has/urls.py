from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('reset/', views.reset_chat, name='reset_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
