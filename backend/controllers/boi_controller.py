from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from services.criar_boi_service import CriarBoiService
from services.listar_bois_service import ListarBoisService
from services.buscar_boi_por_id_service import BuscarBoiPorIdService
from services.atualizar_boi_service import AtualizarBoiService
from services.deletar_boi_service import DeletarBoiService
from services.calcular_valor_boi_service import CalcularValorBoiService
from services.filtrar_por_raca_service import FiltrarPorRacaService
from services.filtrar_por_categoria_service import FiltrarPorCategoriaService
from services.filtrar_por_faixa_peso_service import FiltrarPorFaixaPesoService
from services.gerar_resumo_service import GerarResumoService
from services.buscar_boi_por_nome_service import BuscarBoiPorNomeService
from services.filtrar_por_preco_minimo_service import FiltrarPorPrecoMinimoService
from services.filtrar_por_preco_maximo_service import FiltrarPorPrecoMaximoService
from services.filtrar_por_data_service import FiltrarPorDataService
from services.listar_avaliacoes_recentes_service import ListarAvaliacoesRecentesService
from services.paginar_bois_service import PaginarBoisService
from services.ordenar_por_preco_crescente_service import OrdenarPorPrecoCrescenteService
from services.ordenar_por_preco_decrescente_service import OrdenarPorPrecoDecrescenteService
from services.ordenar_por_peso_service import OrdenarPorPesoService
from models.database import db


class BoiController:
    """Controller responsável por receber requisições HTTP,
    chamar o Service correspondente e retornar a resposta.

    Não contém regra de negócio — apenas orquestra a comunicação
    entre a API Flask e a camada de Services.
    """

    def __init__(self):
        self.blueprint = Blueprint("boi_controller", __name__)
        self._registrar_rotas()

    def _registrar_rotas(self):
        bp = self.blueprint

        # ── Cálculo (sem salvar) ──────────────────────────────────────────

        @bp.post("/bois/calcular")
        def calcular_valor_boi():
            """Calcula o preço estimado sem salvar no banco."""
            try:
                dados = request.get_json() or {}
                peso_kg = float(dados.get("peso_kg", 0))
                valor_arroba = float(dados.get("valor_arroba", 0))

                service = CalcularValorBoiService()
                preco_estimado = service.executar(peso_kg, valor_arroba)

                return jsonify({
                    "peso_kg": peso_kg,
                    "valor_arroba": valor_arroba,
                    "preco_estimado": preco_estimado,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

        # ── CRUD ──────────────────────────────────────────────────────────

        @bp.post("/bois")
        def criar_boi():
            """Cadastra um boi e calcula o preço estimado."""
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

        @bp.get("/bois")
        def listar_bois():
            """Lista todos os bois cadastrados."""
            try:
                service = ListarBoisService()
                bois = service.executar()
                return jsonify(bois), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao listar bois no banco de dados."}), 500

        @bp.get("/bois/<int:boi_id>")
        def buscar_boi_por_id(boi_id):
            """Busca um boi pelo ID."""
            try:
                service = BuscarBoiPorIdService()
                boi = service.executar(boi_id)

                if boi is None:
                    return jsonify({"erro": "Boi não encontrado."}), 404

                return jsonify(boi), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao buscar boi no banco de dados."}), 500

        @bp.put("/bois/<int:boi_id>")
        def atualizar_boi(boi_id):
            """Atualiza um boi e recalcula o preço."""
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

        @bp.delete("/bois/<int:boi_id>")
        def deletar_boi(boi_id):
            """Remove um boi do banco."""
            try:
                service = DeletarBoiService()
                boi_deletado = service.executar(boi_id)

                if boi_deletado is False:
                    return jsonify({"erro": "Boi não encontrado."}), 404

                return "", 204

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao deletar boi no banco de dados."}), 500

        # ── Filtros ───────────────────────────────────────────────────────

        @bp.get("/bois/filtrar/raca")
        def filtrar_por_raca():
            """Filtra avaliações por raça."""
            try:
                raca = request.args.get("raca")
                if not raca:
                    return jsonify({"erro": "O parâmetro 'raca' é obrigatório."}), 400

                service = FiltrarPorRacaService()
                bois = service.executar(raca)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"raca": raca},
                    "resultados": bois,
                }), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        @bp.get("/bois/filtrar/categoria")
        def filtrar_por_categoria():
            """Filtra avaliações por categoria."""
            try:
                categoria = request.args.get("categoria")
                if not categoria:
                    return jsonify({"erro": "O parâmetro 'categoria' é obrigatório."}), 400

                service = FiltrarPorCategoriaService()
                bois = service.executar(categoria)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"categoria": categoria},
                    "resultados": bois,
                }), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        @bp.get("/bois/filtrar/peso")
        def filtrar_por_faixa_peso():
            """Filtra avaliações por faixa de peso."""
            try:
                peso_min = request.args.get("peso_min", type=float)
                peso_max = request.args.get("peso_max", type=float)

                service = FiltrarPorFaixaPesoService()
                bois = service.executar(peso_min=peso_min, peso_max=peso_max)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"peso_min": peso_min, "peso_max": peso_max},
                    "resultados": bois,
                }), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        # ── Ordenações ────────────────────────────────────────────────────

        @bp.get("/bois/ordenar/preco-crescente")
        def ordenar_por_preco_crescente():
            """Exibe as avaliações começando pelo menor preço (item 1)."""
            try:
                service = OrdenarPorPrecoCrescenteService()
                bois = service.executar()

                return jsonify({
                    "total": len(bois),
                    "ordenacao": {"campo": "preco_estimado", "direcao": "crescente"},
                    "resultados": bois,
                }), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao ordenar avaliações no banco de dados."}), 500

        @bp.get("/bois/ordenar/preco-decrescente")
        def ordenar_por_preco_decrescente():
            """Exibe as avaliações começando pelo maior preço (item 2)."""
            try:
                service = OrdenarPorPrecoDecrescenteService()
                bois = service.executar()

                return jsonify({
                    "total": len(bois),
                    "ordenacao": {"campo": "preco_estimado", "direcao": "decrescente"},
                    "resultados": bois,
                }), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao ordenar avaliações no banco de dados."}), 500

        @bp.get("/bois/ordenar/peso")
        def ordenar_por_peso():
            """Organiza os animais do mais leve ao mais pesado (item 3)."""
            try:
                direcao = request.args.get("direcao", "asc")

                service = OrdenarPorPesoService()
                bois = service.executar(direcao)

                return jsonify({
                    "total": len(bois),
                    "ordenacao": {"campo": "peso_kg", "direcao": direcao},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao ordenar avaliações no banco de dados."}), 500

        # ── Pesquisa e gerenciamento ────────────────────────────────────────────────────────

        @bp.get("/bois/buscar")
        def buscar_avaliacao_por_nome():
            """Busca avaliações pelo nome do animal (item 11)."""
            try:
                nome = request.args.get("nome")
                if not nome:
                    return jsonify({"erro": "O parâmetro 'nome' é obrigatório."}), 400

                service = BuscarBoiPorNomeService()
                bois = service.executar(nome)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"nome": nome},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao buscar avaliações no banco de dados."}), 500

        @bp.get("/bois/filtrar/preco-minimo")
        def filtrar_por_preco_minimo():
            """Filtra avaliações com preço estimado mínimo (item 13)."""
            try:
                preco_min = request.args.get("preco_min", type=float)

                service = FiltrarPorPrecoMinimoService()
                bois = service.executar(preco_min)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"preco_min": preco_min},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        @bp.get("/bois/filtrar/preco-maximo")
        def filtrar_por_preco_maximo():
            """Filtra avaliações com preço estimado máximo (item 14)."""
            try:
                preco_max = request.args.get("preco_max", type=float)

                service = FiltrarPorPrecoMaximoService()
                bois = service.executar(preco_max)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"preco_max": preco_max},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        @bp.get("/bois/filtrar/data")
        def filtrar_por_data():
            """Filtra avaliações por período de cadastro (item 15)."""
            try:
                data_inicio = request.args.get("data_inicio")
                data_fim = request.args.get("data_fim")

                service = FiltrarPorDataService()
                bois = service.executar(data_inicio, data_fim)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"data_inicio": data_inicio, "data_fim": data_fim},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao filtrar bois no banco de dados."}), 500

        @bp.get("/bois/recentes")
        def listar_avaliacoes_recentes():
            """Lista as avaliações mais recentes primeiro (item 16)."""
            try:
                limite = request.args.get("limite", type=int)

                service = ListarAvaliacoesRecentesService()
                bois = service.executar(limite)

                return jsonify({
                    "total": len(bois),
                    "filtro": {"limite": limite},
                    "resultados": bois,
                }), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao listar avaliações no banco de dados."}), 500

        @bp.get("/bois/paginar")
        def paginar_bois():
            """Divide a listagem de avaliações em páginas (item 17)."""
            try:
                pagina = request.args.get("pagina", default=1, type=int)
                por_pagina = request.args.get("por_pagina", default=10, type=int)

                service = PaginarBoisService()
                pagina_dados = service.executar(pagina, por_pagina)

                return jsonify(pagina_dados), 200

            except ValueError as erro:
                return jsonify({"erro": str(erro)}), 400

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao paginar bois no banco de dados."}), 500

        # ── Resumo ────────────────────────────────────────────────────

        @bp.get("/bois/resumo")
        def gerar_resumo():
            """Gera um resumo estatístico de todas as avaliações."""
            try:
                service = GerarResumoService()
                resumo = service.executar()
                return jsonify(resumo), 200

            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({"erro": "Erro ao gerar resumo no banco de dados."}), 500

            except Exception as erro:
                return jsonify({"erro": f"Erro ao gerar resumo: {str(erro)}"}), 500
