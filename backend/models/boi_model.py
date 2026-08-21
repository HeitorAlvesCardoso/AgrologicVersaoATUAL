from .database import db


class Boi(db.Model):
    __tablename__ = "bois"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=True)
    raca = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    peso_kg = db.Column(db.Float, nullable=False)
    idade_meses = db.Column(db.Integer, nullable=False)
    valor_arroba = db.Column(db.Float, nullable=False)
    preco_estimado = db.Column(db.Float, nullable=False)
    data_avaliacao = db.Column(db.DateTime, server_default=db.func.now())

    # ── CRUD básico (somente persistência, sem regra de negócio) ──

    def salvar(self):
        """CREATE: salva um novo boi no banco."""
        db.session.add(self)
        db.session.commit()

    def atualizar(self, nome=None, raca=None, categoria=None, peso_kg=None,
                  idade_meses=None, valor_arroba=None, preco_estimado=None):
        """UPDATE: altera apenas os campos informados."""
        if nome is not None:
            self.nome = nome
        if raca is not None:
            self.raca = raca
        if categoria is not None:
            self.categoria = categoria
        if peso_kg is not None:
            self.peso_kg = peso_kg
        if idade_meses is not None:
            self.idade_meses = idade_meses
        if valor_arroba is not None:
            self.valor_arroba = valor_arroba
        if preco_estimado is not None:
            self.preco_estimado = preco_estimado

        db.session.commit()

    def deletar(self):
        """DELETE: remove o boi do banco."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """READ: retorna todos os bois cadastrados."""
        return Boi.query.order_by(Boi.id.asc()).all()

    @staticmethod
    def buscar_por_id(boi_id):
        """READ: busca um boi pelo id."""
        return Boi.query.get(boi_id)

    def to_dict(self):
        """Converte o objeto Boi para dicionário/JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "raca": self.raca,
            "categoria": self.categoria,
            "peso_kg": self.peso_kg,
            "idade_meses": self.idade_meses,
            "valor_arroba": self.valor_arroba,
            "preco_estimado": self.preco_estimado,
            "data_avaliacao": self.data_avaliacao.isoformat() if self.data_avaliacao else None,
        }
