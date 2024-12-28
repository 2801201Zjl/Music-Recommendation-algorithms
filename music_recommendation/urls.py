from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 添加管理后台路由
    path('', include('music.urls')),  # 修改为包含 music.urls
    path('accounts/', include('django.contrib.auth.urls')),  # 保留认证相关URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)