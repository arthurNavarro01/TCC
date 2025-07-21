from rest_framework import serializers
from .models import Localizacao, Documento

class LocalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacao
        fields = ['id', 'rua', 'estante', 'andar', 'posicao']

    def validate(self, data):
        # Garante que os limites de localização sejam respeitados
        rua = data.get('rua')
        estante = data.get('estante')
        andar = data.get('andar')
        posicao = data.get('posicao')
        if rua == 'ANGELICA':
            if not (1 <= estante <= 26 and 1 <= andar <= 10 and 1 <= posicao <= 6):
                raise serializers.ValidationError('Localização fora dos limites da Rua Angélica.')
        elif rua == 'CAMELIA':
            if not (1 <= estante <= 21 and 1 <= andar <= 8 and 1 <= posicao <= 6):
                raise serializers.ValidationError('Localização fora dos limites da Rua Camélia.')
        return data

class DocumentoSerializer(serializers.ModelSerializer):
    data_descarte = serializers.SerializerMethodField()
    status_validade = serializers.SerializerMethodField()
    localizacao = LocalizacaoSerializer()

    class Meta:
        model = Documento
        fields = [
            'id', 'responsavel', 'setor', 'ano', 'tipo', 'anos_para_descarte',
            'data_entrada', 'data_descarte', 'status_validade', 'arquivo_pdf', 'localizacao'
        ]

    def get_data_descarte(self, obj):
        return obj.data_descarte

    def get_status_validade(self, obj):
        return obj.status_validade

    def create(self, validated_data):
        # Cria ou recupera a localização
        localizacao_data = validated_data.pop('localizacao')
        localizacao, _ = Localizacao.objects.get_or_create(**localizacao_data)
        documento = Documento.objects.create(localizacao=localizacao, **validated_data)
        return documento

    def update(self, instance, validated_data):
        # Atualiza a localização
        localizacao_data = validated_data.pop('localizacao', None)
        if localizacao_data:
            for attr, value in localizacao_data.items():
                setattr(instance.localizacao, attr, value)
            instance.localizacao.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance 