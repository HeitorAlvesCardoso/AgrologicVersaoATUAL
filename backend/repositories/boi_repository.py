from sqlalchemy import func
from models.database import db
from models.boi_model import Boi


class BoiRepository:
    """Repository para consultas especiais que vão além do CRUD básico.

    Utilizado para filtros específicos, relatórios e consultas complexas,
    conforme a arquitetura definida no projeto.
    """

    @staticmethod
    def filtrar(raca=None, categoria=None, peso_min=None, peso_max=None):
        """Filtra avaliações com base em um ou mais critérios.

        Pode filtrar por raça, categoria e/ou faixa de peso.
        Parâmetros None ou vazios são ignorados.
        """
        query = Boi.query

        if raca:
            query = query.filter(Boi.raca.ilike(f"%{raca}%"))
        if categoria:
            query = query.filter(Boi.categoria.ilike(f"%{categoria}%"))
        if peso_min is not None:
            query = query.filter(Boi.peso_kg >= peso_min)
        if peso_max is not None:
            query = query.filter(Boi.peso_kg <= peso_max)

        return query.order_by(Boi.id.asc()).all()

    @staticmethod
    def gerar_resumo():
        """Gera um resumo geral de todas as avaliações cadastradas.

        Retorna total de avaliações, peso médio, valor médio da arroba,
        preço médio estimado, menor e maior preço, e totais por categoria/raça.
        """
        resultado = db.session.query(
            func.count(Boi.id).label("total_avaliacoes"),
            func.avg(Boi.peso_kg).label("peso_medio"),
            func.avg(Boi.valor_arroba).label("valor_arroba_medio"),
            func.avg(Boi.preco_estimado).label("preco_medio"),
            func.min(Boi.preco_estimado).label("menor_preco"),
            func.max(Boi.preco_estimado).label("maior_preco"),
            func.sum(Boi.preco_estimado).label("valor_total"),
        ).first()

        # Resumo por categoria
        categorias = db.session.query(
            Boi.categoria,
            func.count(Boi.id).label("quantidade"),
            func.avg(Boi.peso_kg).label("peso_medio"),
            func.avg(Boi.preco_estimado).label("preco_medio"),
        ).group_by(Boi.categoria).all()

        resumo_categorias = []
        for cat in categorias:
            resumo_categorias.append({
                "categoria": cat.categoria,
                "quantidade": cat.quantidade,
                "peso_medio": round(float(cat.peso_medio), 2) if cat.peso_medio else 0,
                "preco_medio": round(float(cat.preco_medio), 2) if cat.preco_medio else 0,
            })

        # Resumo por raça
        racas = db.session.query(
            Boi.raca,
            func.count(Boi.id).label("quantidade"),
            func.avg(Boi.peso_kg).label("peso_medio"),
            func.avg(Boi.preco_estimado).label("preco_medio"),
        ).group_by(Boi.raca).all()

        resumo_racas = []
        for raca in racas:
            resumo_racas.append({
                "raca": raca.raca,
                "quantidade": raca.quantidade,
                "peso_medio": round(float(raca.peso_medio), 2) if raca.peso_medio else 0,
                "preco_medio": round(float(raca.preco_medio), 2) if raca.preco_medio else 0,
            })

        return {
            "total_avaliacoes": resultado.total_avaliacoes or 0,
            "peso_medio": round(float(resultado.peso_medio), 2) if resultado.peso_medio else 0,
            "valor_arroba_medio": round(float(resultado.valor_arroba_medio), 2) if resultado.valor_arroba_medio else 0,
            "preco_medio": round(float(resultado.preco_medio), 2) if resultado.preco_medio else 0,
            "menor_preco": round(float(resultado.menor_preco), 2) if resultado.menor_preco else 0,
            "maior_preco": round(float(resultado.maior_preco), 2) if resultado.maior_preco else 0,
            "valor_total": round(float(resultado.valor_total), 2) if resultado.valor_total else 0,
            "por_categoria": resumo_categorias,
            "por_raca": resumo_racas,
        }
