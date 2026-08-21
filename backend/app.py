import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from models.database import db
from controllers.boi_controller import BoiController


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///agrologic.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Registra a Controller (classe)
    boi_controller = BoiController()
    app.register_blueprint(boi_controller.blueprint)

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API AgroLogic funcionando.",
            "rotas": {
                "calcular_valor_boi": "POST /bois/calcular",
                "criar_boi": "POST /bois",
                "listar_bois": "GET /bois",
                "buscar_boi": "GET /bois/<id>",
                "atualizar_boi": "PUT /bois/<id>",
                "deletar_boi": "DELETE /bois/<id>",
                "filtrar_por_raca": "GET /bois/filtrar/raca?raca=...",
                "filtrar_por_categoria": "GET /bois/filtrar/categoria?categoria=...",
                "filtrar_por_peso": "GET /bois/filtrar/peso?peso_min=...&peso_max=...",
                "gerar_resumo": "GET /bois/resumo",
            }
        })

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug, host="0.0.0.0", port=5000)
