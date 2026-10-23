from repositories.boi_repository import BoiRepository


class OrdenarPorPrecoDecrescenteService:
    """Service para exibir as avaliações começando pelo maior preço estimado."""

    def executar(self):
        """Ordena as avaliações do maior para o menor preço estimado.

        Returns:
            Lista de dicionários com as avaliações ordenadas por preço decrescente.
        """
        bois = BoiRepository.ordenar_por_preco_decrescente()
        return [boi.to_dict() for boi in bois]
