from django.test import TestCase
from .models import Localizacao, Documento
from django.core.exceptions import ValidationError
from datetime import date

class LocalizacaoModelTest(TestCase):
    def test_limites_rua_angelica(self):
        # Fora do limite
        loc = Localizacao(rua='ANGELICA', estante=27, andar=1, posicao=1)
        with self.assertRaises(ValidationError):
            loc.full_clean()
        # Dentro do limite
        loc = Localizacao(rua='ANGELICA', estante=5, andar=2, posicao=3)
        try:
            loc.full_clean()
        except ValidationError:
            self.fail("Localizacao válida levantou ValidationError")

    def test_limites_rua_camelia(self):
        loc = Localizacao(rua='CAMELIA', estante=22, andar=1, posicao=1)
        with self.assertRaises(ValidationError):
            loc.full_clean()

class DocumentoModelTest(TestCase):
    def setUp(self):
        self.loc = Localizacao.objects.create(rua='ANGELICA', estante=1, andar=1, posicao=1)

    def test_data_descarte(self):
        doc = Documento(
            responsavel='João',
            setor='RH',
            ano=2020,
            tipo='CORRENTE',
            anos_para_descarte=5,
            data_entrada=date(2020, 1, 1),
            arquivo_pdf='dummy.pdf',
            localizacao=self.loc
        )
        self.assertEqual(doc.data_descarte, date(2025, 1, 1))

    def test_status_validade(self):
        doc = Documento(
            responsavel='Maria',
            setor='TI',
            ano=2018,
            tipo='INTERMEDIARIO',
            anos_para_descarte=2,
            data_entrada=date(2018, 1, 1),
            arquivo_pdf='dummy.pdf',
            localizacao=self.loc
        )
        self.assertEqual(doc.status_validade, 'vencido')

from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Localizacao, Documento

class DocumentoAPITest(APITestCase):
    def setUp(self):
        self.loc = Localizacao.objects.create(rua='ANGELICA', estante=1, andar=1, posicao=1)
        self.doc = Documento.objects.create(
            responsavel='João',
            setor='RH',
            ano=2020,
            tipo='CORRENTE',
            anos_para_descarte=5,
            localizacao=self.loc,
            arquivo_pdf='dummy.pdf'
        )

    def test_list_documentos(self):
        url = reverse('documento-list')  # O nome padrão do router é <basename>-list
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_dashboard_status(self):
        url = reverse('dashboard-status')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('valido', response.data)