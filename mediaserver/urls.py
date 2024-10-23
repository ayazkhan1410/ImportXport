from django.contrib import admin
from django.urls import path, include

# only for Local Development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("automation.urls")),
    path('emails/', include('emails.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Add this line
]

# only for Local Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)