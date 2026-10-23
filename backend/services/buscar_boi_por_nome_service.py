from repositories.boi_repository import BoiRepository


class BuscarBoiPorNomeService:
    """Service para buscar avaliações pelo nome do animal cadastrado."""

    def executar(self, nome):
        """Busca bois pelo nome (busca parcial, case-insensitive).

        Args:
            nome: Nome (ou trecho do nome) do animal para busca.

        Returns:
            Lista de dicionários com as avaliações encontradas.
        """
        if not nome or not nome.strip():
            raise ValueError("O parâmetro 'nome' é obrigatório.")

        bois = BoiRepository.buscar_por_nome(nome.strip())
        return [boi.to_dict() for boi in bois]
