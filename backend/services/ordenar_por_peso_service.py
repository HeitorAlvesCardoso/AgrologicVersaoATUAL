from repositories.boi_repository import BoiRepository


class OrdenarPorPesoService:
    """Service para organizar os animais do mais leve ao mais pesado (ou o contrário)."""

    def executar(self, direcao="asc"):
        """Ordena as avaliações pelo peso do animal.

        Args:
            direcao: "asc" do mais leve ao mais pesado (padrão),
                "desc" do mais pesado ao mais leve.

        Returns:
            Lista de dicionários com as avaliações ordenadas por peso.

        Raises:
            ValueError: Se a direção informada não for "asc" nem "desc".
        """
        if direcao not in ("asc", "desc"):
            raise ValueError("O parâmetro 'direcao' deve ser 'asc' ou 'desc'.")

        bois = BoiRepository.ordenar_por_peso(direcao)
        return [boi.to_dict() for boi in bois]
