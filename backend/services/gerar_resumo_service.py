from repositories.boi_repository import BoiRepository


class GerarResumoService:
    """Service responsável por gerar o resumo das avaliações de bois.

    Fornece estatísticas gerais como total de avaliações,
    pesos médios, valores médios e totais por categoria/raça.
    """

    def executar(self):
        """Gera o resumo completo das avaliações.

        Returns:
            Dicionário com estatísticas gerais, resumo por categoria
            e resumo por raça.
        """
        resumo = BoiRepository.gerar_resumo()
        return resumo
