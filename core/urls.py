
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashbord/', include('dashbord.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
]+ static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
