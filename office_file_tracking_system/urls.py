from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls.static import static
from office_file_tracking_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(('accounts.urls', 'accounts'), namespace='accounts')),
    re_path(r'content/', include(('content.urls', 'content'), namespace='content')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
