from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Documento, Localizacao
from .serializers import DocumentoSerializer, LocalizacaoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'setor', 'responsavel', 'tipo', 'ano',
        'localizacao__rua', 'localizacao__estante', 'localizacao__andar', 'localizacao__posicao'
    ]
    search_fields = [
        'responsavel', 'setor', 'ano', 'tipo',
        'localizacao__rua', 'localizacao__estante', 'localizacao__andar', 'localizacao__posicao'
    ]
    ordering_fields = ['ano', 'data_entrada', 'setor', 'tipo']

class LocalizacaoViewSet(viewsets.ModelViewSet):
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['rua', 'estante', 'andar', 'posicao']

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def dashboard_status_count(request):
    total = Documento.objects.count()
    valido = sum(1 for doc in Documento.objects.all() if doc.status_validade == 'válido')
    a_vencer = sum(1 for doc in Documento.objects.all() if doc.status_validade == 'a vencer')
    vencido = sum(1 for doc in Documento.objects.all() if doc.status_validade == 'vencido')
    return Response({
        'total': total,
        'valido': valido,
        'a_vencer': a_vencer,
        'vencido': vencido,
    })