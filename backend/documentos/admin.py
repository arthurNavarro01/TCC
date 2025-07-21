from django.contrib import admin
from .models import Documento, Localizacao

@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'estante', 'andar', 'posicao')
    search_fields = ('rua', 'estante', 'andar', 'posicao')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('setor', 'responsavel', 'ano', 'tipo', 'status_validade', 'data_entrada')
    search_fields = ('setor', 'responsavel', 'ano', 'tipo')
    readonly_fields = ('data_descarte', 'status_validade')
    list_filter = ('tipo', 'setor', 'ano', 'localizacao__rua',)