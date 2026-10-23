from repositories.boi_repository import BoiRepository


class ListarAvaliacoesRecentesService:
    """Service para listar as avaliações mais recentes primeiro."""

    def executar(self, limite=None):
        """Lista avaliações ordenadas da mais recente para a mais antiga.

        Args:
            limite: Quantidade máxima de avaliações a retornar. Opcional.

        Returns:
            Lista de dicionários com as avaliações mais recentes.

        Raises:
            ValueError: Se o limite informado for menor que 1.
        """
        if limite is not None and limite < 1:
            raise ValueError("O parâmetro 'limite' deve ser maior ou igual a 1.")

        bois = BoiRepository.listar_recentes(limite)
        return [boi.to_dict() for boi in bois]
