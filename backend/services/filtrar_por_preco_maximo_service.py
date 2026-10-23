from repositories.boi_repository import BoiRepository


class FiltrarPorPrecoMaximoService:
    """Service para filtrar avaliações com preço estimado máximo."""

    def executar(self, preco_max):
        """Filtra bois com preço estimado igual ou inferior ao informado.

        Args:
            preco_max: Valor máximo do preço estimado.

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        if preco_max is None:
            raise ValueError("O parâmetro 'preco_max' é obrigatório.")

        bois = BoiRepository.filtrar_por_preco_maximo(preco_max)
        return [boi.to_dict() for boi in bois]
