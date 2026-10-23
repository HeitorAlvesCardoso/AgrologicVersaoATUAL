from repositories.boi_repository import BoiRepository


class OrdenarPorPrecoCrescenteService:
    """Service para exibir as avaliações começando pelo menor preço estimado."""

    def executar(self):
        """Ordena as avaliações do menor para o maior preço estimado.

        Returns:
            Lista de dicionários com as avaliações ordenadas por preço crescente.
        """
        bois = BoiRepository.ordenar_por_preco_crescente()
        return [boi.to_dict() for boi in bois]
