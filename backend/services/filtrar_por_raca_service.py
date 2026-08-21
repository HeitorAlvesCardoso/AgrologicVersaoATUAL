from repositories.boi_repository import BoiRepository


class FiltrarPorRacaService:
    """Service para filtrar avaliações de bois por raça."""

    def executar(self, raca):
        """Filtra bois por raça (busca parcial, case-insensitive).

        Args:
            raca: Nome da raça para busca.

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        bois = BoiRepository.filtrar_por_raca(raca)
        return [boi.to_dict() for boi in bois]
