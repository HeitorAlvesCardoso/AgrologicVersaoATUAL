from repositories.boi_repository import BoiRepository


class FiltrarPorPrecoMinimoService:
    """Service para filtrar avaliações com preço estimado mínimo."""

    def executar(self, preco_min):
        """Filtra bois com preço estimado igual ou superior ao informado.

        Args:
            preco_min: Valor mínimo do preço estimado.

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        if preco_min is None:
            raise ValueError("O parâmetro 'preco_min' é obrigatório.")

        bois = BoiRepository.filtrar_por_preco_minimo(preco_min)
        return [boi.to_dict() for boi in bois]
