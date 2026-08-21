from repositories.boi_repository import BoiRepository


class FiltrarPorFaixaPesoService:
    """Service para filtrar avaliações de bois por faixa de peso."""

    def executar(self, peso_min=None, peso_max=None):
        """Filtra bois dentro de uma faixa de peso.

        Args:
            peso_min: Peso mínimo em kg (inclusive). Opcional.
            peso_max: Peso máximo em kg (inclusive). Opcional.

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        bois = BoiRepository.filtrar_por_faixa_de_peso(peso_min, peso_max)
        return [boi.to_dict() for boi in bois]
