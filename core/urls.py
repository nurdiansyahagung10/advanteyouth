
from django.contrib import admin
from django.urls import path, include
from . import views
from products.views import ProductViewSet
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('search/', views.search_products, name='search_products'),
    path('api/', include(router.urls)),
    path('order/', include('order.urls')),
    path('dashbord/', include('dashbord.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('paymentpal/', include('paypal.standard.ipn.urls')),
    
]+ static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



