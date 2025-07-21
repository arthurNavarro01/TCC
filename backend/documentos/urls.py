from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, LocalizacaoViewSet, dashboard_status_count

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet)
router.register(r'localizacoes', LocalizacaoViewSet)

urlpatterns = [
    path('dashboard/status/', dashboard_status_count, name='dashboard-status'),
]

urlpatterns += router.urls