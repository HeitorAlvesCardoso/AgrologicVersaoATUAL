from repositories.boi_repository import BoiRepository


class FiltrarBoisService:
    """Service responsável por filtrar avaliações de bois.

    Coordena a lógica de negócio dos filtros, delegando todas
    as consultas ao Repository conforme a arquitetura definida.
    """

    def executar(self, raca=None, categoria=None, peso_min=None, peso_max=None):
        """Executa o filtro com base nos parâmetros informados.

        Pode filtrar por raça, categoria e/ou faixa de peso.
        Todos os parâmetros são opcionais.

        Args:
            raca: Nome da raça (busca parcial, case-insensitive).
            categoria: Nome da categoria (busca parcial, case-insensitive).
            peso_min: Peso mínimo em kg (inclusive).
            peso_max: Peso máximo em kg (inclusive).

        Returns:
            Lista de dicionários com os bois filtrados.
        """
        bois = BoiRepository.filtrar(
            raca=raca,
            categoria=categoria,
            peso_min=peso_min,
            peso_max=peso_max,
        )

        return [boi.to_dict() for boi in bois]
