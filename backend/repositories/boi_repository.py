from sqlalchemy import select, text

from models.database import db
from models.boi_model import Boi


class BoiRepository:
    """Repository para consultas especiais que vão além do CRUD básico.

    Utilizado para filtros, relatórios e consultas complexas,
    conforme a arquitetura definida no projeto.

    Todas as consultas são escritas em SQL e executadas com
    ``db.session.execute(text(...))``, usando parâmetros vinculados
    (``:nome``) para evitar SQL Injection. Nos SELECTs de bois o
    resultado é convertido em objetos ``Boi`` com
    ``select(Boi).from_statement(text(...))``, que aplica os tipos
    das colunas (ex.: ``data_avaliacao`` como datetime).
    """

    # ── Auxiliares ──

    @staticmethod
    def _executar(sql, parametros=None):
        """Executa um SELECT e devolve a lista de bois encontrados."""
        comando = select(Boi).from_statement(text(sql))
        return db.session.execute(comando, parametros or {}).scalars().all()

    @staticmethod
    def _executar_um(sql, parametros=None):
        """Executa um SELECT e devolve a primeira linha (ou None)."""
        resultado = db.session.execute(text(sql), parametros or {})
        return resultado.mappings().first()

    # ── Filtros individuais ──

    @staticmethod
    def filtrar_por_raca(raca):
        """Filtra avaliações por raça do boi (busca parcial)."""
        sql = """
            SELECT *
              FROM bois
             WHERE LOWER(raca) LIKE LOWER(:raca)
             ORDER BY id ASC
        """
        return BoiRepository._executar(sql, {"raca": f"%{raca}%"})

    @staticmethod
    def filtrar_por_categoria(categoria):
        """Filtra avaliações por categoria (busca parcial)."""
        sql = """
            SELECT *
              FROM bois
             WHERE LOWER(categoria) LIKE LOWER(:categoria)
             ORDER BY id ASC
        """
        return BoiRepository._executar(sql, {"categoria": f"%{categoria}%"})

    @staticmethod
    def filtrar_por_faixa_de_peso(peso_min=None, peso_max=None):
        """Filtra avaliações por faixa de peso (em kg)."""
        sql = """
            SELECT *
              FROM bois
             WHERE (:peso_min IS NULL OR peso_kg >= :peso_min)
               AND (:peso_max IS NULL OR peso_kg <= :peso_max)
             ORDER BY peso_kg ASC
        """
        return BoiRepository._executar(
            sql, {"peso_min": peso_min, "peso_max": peso_max}
        )

    # ── Ordenações ──

    @staticmethod
    def ordenar_por_preco_crescente():
        """Retorna as avaliações do menor para o maior preço estimado."""
        sql = """
            SELECT *
              FROM bois
             ORDER BY preco_estimado ASC
        """
        return BoiRepository._executar(sql)

    @staticmethod
    def ordenar_por_preco_decrescente():
        """Retorna as avaliações do maior para o menor preço estimado."""
        sql = """
            SELECT *
              FROM bois
             ORDER BY preco_estimado DESC
        """
        return BoiRepository._executar(sql)

    @staticmethod
    def ordenar_por_peso(direcao="asc"):
        """Retorna as avaliações ordenadas por peso (asc ou desc)."""
        # Só "ASC" ou "DESC" entram no SQL, nunca o texto do usuário.
        ordem = "ASC" if direcao == "asc" else "DESC"
        sql = f"""
            SELECT *
              FROM bois
             ORDER BY peso_kg {ordem}
        """
        return BoiRepository._executar(sql)

    # ── Pesquisa e gerenciamento ──

    @staticmethod
    def buscar_por_nome(nome):
        """Busca avaliações pelo nome do animal (busca parcial, case-insensitive)."""
        sql = """
            SELECT *
              FROM bois
             WHERE LOWER(nome) LIKE LOWER(:nome)
             ORDER BY id ASC
        """
        return BoiRepository._executar(sql, {"nome": f"%{nome}%"})

    @staticmethod
    def filtrar_por_preco_minimo(preco_min):
        """Filtra avaliações com preço estimado igual ou superior ao informado."""
        sql = """
            SELECT *
              FROM bois
             WHERE preco_estimado >= :preco_min
             ORDER BY preco_estimado ASC
        """
        return BoiRepository._executar(sql, {"preco_min": preco_min})

    @staticmethod
    def filtrar_por_preco_maximo(preco_max):
        """Filtra avaliações com preço estimado igual ou inferior ao informado."""
        sql = """
            SELECT *
              FROM bois
             WHERE preco_estimado <= :preco_max
             ORDER BY preco_estimado DESC
        """
        return BoiRepository._executar(sql, {"preco_max": preco_max})

    @staticmethod
    def filtrar_por_periodo(inicio=None, fim=None):
        """Filtra avaliações realizadas em um período (AAAA-MM-DD)."""
        sql = """
            SELECT *
              FROM bois
             WHERE (:inicio IS NULL OR DATE(data_avaliacao) >= :inicio)
               AND (:fim IS NULL OR DATE(data_avaliacao) <= :fim)
             ORDER BY data_avaliacao DESC
        """
        return BoiRepository._executar(sql, {"inicio": inicio, "fim": fim})

    @staticmethod
    def listar_recentes(limite=None):
        """Lista as avaliações cadastradas mais recentemente primeiro."""
        sql = """
            SELECT *
              FROM bois
             ORDER BY data_avaliacao DESC, id DESC
        """
        parametros = {}

        if limite:
            sql += "\n             LIMIT :limite"
            parametros["limite"] = limite

        return BoiRepository._executar(sql, parametros)

    @staticmethod
    def paginar(pagina, por_pagina):
        """Divide a listagem em páginas e retorna os itens e o total."""
        total = BoiRepository._executar_um("SELECT COUNT(*) AS total FROM bois")["total"]

        sql = """
            SELECT *
              FROM bois
             ORDER BY id DESC
             LIMIT :limite OFFSET :deslocamento
        """
        itens = BoiRepository._executar(
            sql,
            {
                "limite": por_pagina,
                "deslocamento": (pagina - 1) * por_pagina,
            },
        )

        return itens, total

    # ── Relatórios ──

    @staticmethod
    def gerar_resumo():
        """Gera um resumo geral de todas as avaliações cadastradas."""
        resultado = BoiRepository._executar_um(
            """
            SELECT COUNT(id)          AS total_avaliacoes,
                   AVG(peso_kg)       AS peso_medio,
                   AVG(valor_arroba)  AS valor_arroba_medio,
                   AVG(preco_estimado) AS preco_medio,
                   MIN(preco_estimado) AS menor_preco,
                   MAX(preco_estimado) AS maior_preco,
                   SUM(preco_estimado) AS valor_total
              FROM bois
            """
        )

        # Resumo por categoria
        categorias = db.session.execute(text(
            """
            SELECT categoria,
                   COUNT(id)           AS quantidade,
                   AVG(peso_kg)        AS peso_medio,
                   AVG(preco_estimado) AS preco_medio
              FROM bois
             GROUP BY categoria
            """
        )).mappings().all()

        resumo_categorias = []
        for cat in categorias:
            resumo_categorias.append({
                "categoria": cat["categoria"],
                "quantidade": cat["quantidade"],
                "peso_medio": round(float(cat["peso_medio"]), 2) if cat["peso_medio"] else 0,
                "preco_medio": round(float(cat["preco_medio"]), 2) if cat["preco_medio"] else 0,
            })

        # Resumo por raça
        racas = db.session.execute(text(
            """
            SELECT raca,
                   COUNT(id)           AS quantidade,
                   AVG(peso_kg)        AS peso_medio,
                   AVG(preco_estimado) AS preco_medio
              FROM bois
             GROUP BY raca
            """
        )).mappings().all()

        resumo_racas = []
        for raca in racas:
            resumo_racas.append({
                "raca": raca["raca"],
                "quantidade": raca["quantidade"],
                "peso_medio": round(float(raca["peso_medio"]), 2) if raca["peso_medio"] else 0,
                "preco_medio": round(float(raca["preco_medio"]), 2) if raca["preco_medio"] else 0,
            })

        return {
            "total_avaliacoes": resultado["total_avaliacoes"] or 0,
            "peso_medio": round(float(resultado["peso_medio"]), 2) if resultado["peso_medio"] else 0,
            "valor_arroba_medio": round(float(resultado["valor_arroba_medio"]), 2) if resultado["valor_arroba_medio"] else 0,
            "preco_medio": round(float(resultado["preco_medio"]), 2) if resultado["preco_medio"] else 0,
            "menor_preco": round(float(resultado["menor_preco"]), 2) if resultado["menor_preco"] else 0,
            "maior_preco": round(float(resultado["maior_preco"]), 2) if resultado["maior_preco"] else 0,
            "valor_total": round(float(resultado["valor_total"]), 2) if resultado["valor_total"] else 0,
            "por_categoria": resumo_categorias,
            "por_raca": resumo_racas,
        }
