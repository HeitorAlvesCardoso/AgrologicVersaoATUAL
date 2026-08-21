from models.boi_model import Boi
from services.calcular_valor_boi_service import CalcularValorBoiService


class CriarBoiService:
    def executar(self, dados):
        campos_obrigatorios = ["raca", "categoria", "peso_kg", "idade_meses", "valor_arroba"]

        for campo in campos_obrigatorios:
            if dados.get(campo) is None:
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        peso_kg = float(dados["peso_kg"])
        valor_arroba = float(dados["valor_arroba"])

        calculo = CalcularValorBoiService()
        preco_estimado = calculo.executar(peso_kg, valor_arroba)

        boi = Boi(
            nome=dados.get("nome"),
            raca=dados["raca"],
            categoria=dados["categoria"],
            peso_kg=peso_kg,
            idade_meses=dados["idade_meses"],
            valor_arroba=valor_arroba,
            preco_estimado=preco_estimado,
        )

        boi.salvar()
        return boi.to_dict()
