from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from services.criar_boi_service import CriarBoiService
from services.listar_bois_service import ListarBoisService
from services.buscar_boi_por_id_service import BuscarBoiPorIdService
from services.atualizar_boi_service import AtualizarBoiService
from services.deletar_boi_service import DeletarBoiService
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
