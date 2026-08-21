from repositories.boi_repository import BoiRepository


class FiltrarPorCategoriaService:
    """Service para filtrar avaliações de bois por categoria."""

    def executar(self, categoria):
        """Filtra bois por categoria (busca parcial, case-insensitive).

        Args:
            categoria: Nome da categoria para busca (ex: Boi Gordo, Novilho).

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        bois = BoiRepository.filtrar_por_categoria(categoria)
        return [boi.to_dict() for boi in bois]
