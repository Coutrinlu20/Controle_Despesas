from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics, filters # type: ignore
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from transactions.models import Transacao
from transactions.serializers import TransacaoSerializer


class TransacaoListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar transações.
    """
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['tipo', 'categoria', 'usuario', 'data']
    ordering_fields = ['valor', 'data']
    search_fields = ['descricao', 'categoria']

    def perform_create(self, serializer):
        """
        Regras ao criar uma transação:
        - O valor deve ser positivo.
        - A data deve ser informada corretamente.
        """
        if serializer.validated_data['valor'] <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        serializer.save(usuario=self.request.user)


class TransacaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para recuperar, atualizar e deletar uma transação específica.
    """
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer

    def perform_update(self, serializer):
        """
        Regras ao atualizar uma transação:
        - Verificar se o valor permanece positivo.
        """
        if serializer.validated_data.get('valor', 0) <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        serializer.save()


class RelatorioTransacoesView(APIView):
    """
    View para gerar um relatório com o resumo das transações do usuário.
    """
    def get(self, request):
        """
        Retorna um resumo das transações, incluindo total de receitas, despesas e saldo final.
        """
        usuario = request.user
        transacoes = Transacao.objects.filter(usuario=usuario)

        total_receitas = transacoes.filter(tipo='receita').aggregate(models.Sum('valor'))['valor__sum'] or 0
        total_despesas = transacoes.filter(tipo='despesa').aggregate(models.Sum('valor'))['valor__sum'] or 0
        saldo_final = total_receitas - total_despesas

        resumo = {
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo_final': saldo_final,
        }
        return JsonResponse(resumo, status=status.HTTP_200_OK)


class FiltrarTransacoesView(generics.ListAPIView):
    """
    View para filtrar transações com base em parâmetros avançados.
    """
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'valor': ['gte', 'lte'],  # Faixa de valores
        'data': ['gte', 'lte'],  # Faixa de datas
        'tipo': ['exact'],
        'categoria': ['exact'],
    }


class ExcluirTransacoesAntigasView(APIView):
    """
    View para excluir transações antigas (por exemplo, mais de 5 anos).
    """
    def delete(self, request):
        """
        Remove transações com data superior a 5 anos a partir da data atual.
        """
        limite_data = timezone.now() - timezone.timedelta(days=5 * 365)
        transacoes_antigas = Transacao.objects.filter(data__lt=limite_data, usuario=request.user)
        total_excluidas = transacoes_antigas.count()
        transacoes_antigas.delete()

        return JsonResponse({
            "mensagem": f"{total_excluidas} transações antigas foram excluídas com sucesso."
        }, status=status.HTTP_200_OK)


class ImportarTransacoesCSVView(APIView):
    """
    View para importar transações a partir de um arquivo CSV.
    """
    def post(self, request):
        """
        Processa o upload de um arquivo CSV e importa as transações para o banco de dados.
        """
        arquivo = request.FILES.get('arquivo')
        if not arquivo:
            return JsonResponse({"erro": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)

        # Implementar lógica de importação aqui.
        # Exemplo simplificado:
        try:
            import csv

            with arquivo.open('r') as f:
                reader = csv.DictReader(f)
                for linha in reader:
                    Transacao.objects.create(
                        usuario=request.user,
                        tipo=linha['tipo'],
                        valor=float(linha['valor']),
                        descricao=linha['descricao'],
                        categoria=linha['categoria'],
                        data=linha['data'],
                    )

            return JsonResponse({"mensagem": "Transações importadas com sucesso."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

