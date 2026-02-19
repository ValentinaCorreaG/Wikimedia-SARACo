from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path("__reload__/", include("django_browser_reload.urls")),
]