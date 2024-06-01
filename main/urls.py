# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guests/', views.guest_list, name='guest_list'),
    path('invitation/<str:name>/<int:identification>/', views.invitation, name='invitation'),
    path('response/<int:guest_id>/', views.guest_response, name='response'),
    path('statistics/', views.statistics, name='statistics'),
    path('export_guests/', views.export_guests, name='export_guests'),
    path('serve_apng/', views.cached_serve, {'path': 'images/en_animation_compressed.png', 'document_root': settings.BASE_DIR / 'main' / 'static'}, name='serve_apng'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
