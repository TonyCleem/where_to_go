from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from where_to_go import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('places/<int:place_id>/', views.location, name='location'),
    path('places/<str:json_file>/', views.get_json, name='get_json'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
