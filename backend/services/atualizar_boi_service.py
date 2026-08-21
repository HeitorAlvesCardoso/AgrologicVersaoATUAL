from models.boi_model import Boi
from services.calcular_valor_boi_service import CalcularValorBoiService


class AtualizarBoiService:
    def executar(self, boi_id, dados):
        boi = Boi.buscar_por_id(boi_id)

        if boi is None:
            return None

        peso_kg = dados.get("peso_kg", boi.peso_kg)
        valor_arroba = dados.get("valor_arroba", boi.valor_arroba)

        calculo = CalcularValorBoiService()
        preco_estimado = calculo.executar(float(peso_kg), float(valor_arroba))

        boi.atualizar(
            nome=dados.get("nome"),
            raca=dados.get("raca"),
            categoria=dados.get("categoria"),
            peso_kg=dados.get("peso_kg"),
            idade_meses=dados.get("idade_meses"),
            valor_arroba=dados.get("valor_arroba"),
            preco_estimado=preco_estimado,
        )

        return boi.to_dict()
