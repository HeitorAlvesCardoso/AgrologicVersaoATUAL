from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from services.criar_boi_service import CriarBoiService
from services.listar_bois_service import ListarBoisService
from services.buscar_boi_por_id_service import BuscarBoiPorIdService
from services.atualizar_boi_service import AtualizarBoiService
from services.deletar_boi_service import DeletarBoiService
from services.filtrar_bois_service import FiltrarBoisService
from services.gerar_resumo_service import GerarResumoService
from models.database import db

boi_controller = Blueprint("boi_controller", __name__)


@boi_controller.post("/bois")
def criar_boi():
    try:
        dados = request.get_json() or {}
        service = CriarBoiService()
        boi = service.executar(dados)
        return jsonify(boi), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar boi no banco de dados."}), 500


@boi_controller.get("/bois")
def listar_bois():
    service = ListarBoisService()
    bois = service.executar()
    return jsonify(bois), 200


@boi_controller.get("/bois/<int:boi_id>")
def buscar_boi_por_id(boi_id):
    service = BuscarBoiPorIdService()
    boi = service.executar(boi_id)

    if boi is None:
        return jsonify({"erro": "Boi não encontrado."}), 404

    return jsonify(boi), 200


@boi_controller.put("/bois/<int:boi_id>")
def atualizar_boi(boi_id):
    try:
        dados = request.get_json() or {}
        service = AtualizarBoiService()
        boi = service.executar(boi_id, dados)

        if boi is None:
            return jsonify({"erro": "Boi não encontrado."}), 404

        return jsonify(boi), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar boi no banco de dados."}), 500


@boi_controller.delete("/bois/<int:boi_id>")
def deletar_boi(boi_id):
    try:
        service = DeletarBoiService()
        boi_deletado = service.executar(boi_id)

        if boi_deletado is False:
            return jsonify({"erro": "Boi não encontrado."}), 404

        return "", 204

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar boi no banco de dados."}), 500


# ── Rotas de Filtro ──────────────────────────────────────────────────────────


@boi_controller.get("/bois/filtrar")
def filtrar_bois():
    """Filtra avaliações por raça, categoria e/ou faixa de peso.

    Query params:
        raca (str): Nome da raça (busca parcial).
        categoria (str): Nome da categoria (busca parcial).
        peso_min (float): Peso mínimo em kg.
        peso_max (float): Peso máximo em kg.
    """
    try:
        raca = request.args.get("raca")
        categoria = request.args.get("categoria")
        peso_min = request.args.get("peso_min", type=float)
        peso_max = request.args.get("peso_max", type=float)

        service = FiltrarBoisService()
        bois = service.executar(
            raca=raca,
            categoria=categoria,
            peso_min=peso_min,
            peso_max=peso_max,
        )

        return jsonify({
            "total": len(bois),
            "filtros_aplicados": {
                "raca": raca,
                "categoria": categoria,
                "peso_min": peso_min,
                "peso_max": peso_max,
            },
            "resultados": bois,
        }), 200

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

    except Exception as erro:
        return jsonify({"erro": f"Erro ao filtrar bois: {str(erro)}"}), 500


# ── Rota de Resumo ───────────────────────────────────────────────────────────


@boi_controller.get("/bois/resumo")
def gerar_resumo():
    """Gera um resumo estatístico de todas as avaliações.

    Retorna total de avaliações, peso médio, valor médio da arroba,
    preço médio estimado, menor e maior preço, e totais por categoria/raça.
    """
    try:
        service = GerarResumoService()
        resumo = service.executar()

        return jsonify(resumo), 200

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao gerar resumo no banco de dados."}), 500

    except Exception as erro:
        return jsonify({"erro": f"Erro ao gerar resumo: {str(erro)}"}), 500
