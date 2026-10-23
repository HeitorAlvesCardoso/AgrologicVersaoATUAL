from repositories.boi_repository import BoiRepository


class PaginarBoisService:
    """Service para dividir a listagem de avaliações em páginas."""

    def executar(self, pagina=1, por_pagina=10):
        """Retorna uma página da listagem de avaliações.

        Args:
            pagina: Número da página (inicia em 1).
            por_pagina: Quantidade de registros por página.

        Returns:
            Dicionário com paginação e a lista de itens da página.
        """
        pagina = int(pagina)
        por_pagina = int(por_pagina)

        if pagina < 1:
            raise ValueError("O parâmetro 'pagina' deve ser maior ou igual a 1.")
        if por_pagina < 1 or por_pagina > 100:
            raise ValueError("O parâmetro 'por_pagina' deve estar entre 1 e 100.")

        itens, total = BoiRepository.paginar(pagina, por_pagina)
        total_paginas = (total + por_pagina - 1) // por_pagina

        return {
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": total_paginas,
            "resultados": [boi.to_dict() for boi in itens],
        }
