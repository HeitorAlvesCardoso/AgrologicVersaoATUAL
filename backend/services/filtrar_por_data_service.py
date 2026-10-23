from datetime import datetime

from repositories.boi_repository import BoiRepository


class FiltrarPorDataService:
    """Service para filtrar avaliações realizadas em um período."""

    def executar(self, data_inicio=None, data_fim=None):
        """Filtra bois avaliados entre duas datas (formato AAAA-MM-DD).

        Args:
            data_inicio: Data inicial do período (inclusive). Opcional.
            data_fim: Data final do período (inclusive). Opcional.

        Returns:
            Lista de dicionários com os bois filtrados,
            do mais recente para o mais antigo.

        Raises:
            ValueError: Se nenhuma data for informada ou se o formato
                de alguma data for inválido.
        """
        if not data_inicio and not data_fim:
            raise ValueError(
                "Informe a data inicial e/ou a data final no formato AAAA-MM-DD."
            )

        for rotulo, data in (("data_inicio", data_inicio), ("data_fim", data_fim)):
            if data:
                try:
                    datetime.strptime(data, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(
                        f"O parâmetro '{rotulo}' deve estar no formato AAAA-MM-DD."
                    )

        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValueError("A data inicial não pode ser posterior à data final.")

        bois = BoiRepository.filtrar_por_periodo(data_inicio, data_fim)
        return [boi.to_dict() for boi in bois]
