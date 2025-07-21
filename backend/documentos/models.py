from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# ---------------------------
# MODELO DE LOCALIZAÇÃO
# ---------------------------
class Localizacao(models.Model):
    RUA_CHOICES = [
        ('ANGELICA', 'Angélica'),
        ('CAMELIA', 'Camélia'),
        # Adicione outras ruas se necessário
    ]
    rua = models.CharField(max_length=20, choices=RUA_CHOICES)
    estante = models.PositiveIntegerField()
    andar = models.PositiveIntegerField()
    posicao = models.PositiveIntegerField()

    class Meta:
        unique_together = ('rua', 'estante', 'andar', 'posicao')
        verbose_name = "Localização"
        verbose_name_plural = "Localizações"

    def clean(self):
        # Validação dos limites de cada rua
        if self.rua == 'ANGELICA':
            if not (1 <= self.estante <= 26 and 1 <= self.andar <= 10 and 1 <= self.posicao <= 6):
                raise ValidationError("Localização fora dos limites da Rua Angélica.")
        elif self.rua == 'CAMELIA':
            if not (1 <= self.estante <= 21 and 1 <= self.andar <= 8 and 1 <= self.posicao <= 6):
                raise ValidationError("Localização fora dos limites da Rua Camélia.")

    def __str__(self):
        return f"{self.get_rua_display()} - Estante {self.estante}, Andar {self.andar}, Posição {self.posicao}"

# ---------------------------
# MODELO DE DOCUMENTO
# ---------------------------
class Documento(models.Model):
    class TipoChoices(models.TextChoices):
        CORRENTE = 'CORRENTE', 'Corrente'
        INTERMEDIARIO = 'INTERMEDIARIO', 'Intermediário'

    responsavel = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, choices=TipoChoices.choices)
    anos_para_descarte = models.PositiveIntegerField()
    data_entrada = models.DateField(default=timezone.now)
    arquivo_pdf = models.FileField(upload_to='documentos/')
    localizacao = models.OneToOneField(Localizacao, on_delete=models.PROTECT, related_name='documento')

    class Meta:
        ordering = ['-data_entrada']

    @property
    def data_descarte(self):
        # Calcula a data de descarte automaticamente
        return self.data_entrada.replace(year=self.data_entrada.year + self.anos_para_descarte)

    @property
    def status_validade(self):
        # Calcula o status do documento dinamicamente
        hoje = timezone.now().date()
        if hoje < self.data_descarte:
            if (self.data_descarte - hoje).days <= 180:
                return "a vencer"
            return "válido"
        return "vencido"

    def clean(self):
        # Garante que não haja sobreposição de localização
        if Documento.objects.filter(localizacao=self.localizacao).exclude(pk=self.pk).exists():
            raise ValidationError("Já existe um documento nessa localização.")

    def __str__(self):
        return f"{self.setor} - {self.responsavel} ({self.ano})" 