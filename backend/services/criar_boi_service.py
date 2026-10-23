from models.boi_model import Boi
from services.calcular_valor_boi_service import CalcularValorBoiService


class CriarBoiService:
    CAMPOS_OBRIGATORIOS = ["raca", "categoria", "peso_kg", "idade_meses", "valor_arroba"]

    def executar(self, dados):
        """Valida os campos obrigatórios e cadastra a avaliação (item 20)."""
        campos_invalidos = [
            campo for campo in self.CAMPOS_OBRIGATORIOS
            if dados.get(campo) is None or str(dados.get(campo)).strip() == ""
        ]

        if campos_invalidos:
            campos = ", ".join(f"'{campo}'" for campo in campos_invalidos)
            raise ValueError(f"Os campos obrigatórios não foram preenchidos: {campos}.")

        try:
            peso_kg = float(dados["peso_kg"])
            valor_arroba = float(dados["valor_arroba"])
            idade_meses = int(dados["idade_meses"])
        except (TypeError, ValueError):
            raise ValueError(
                "Valores inválidos: 'peso_kg' e 'valor_arroba' devem ser números "
                "e 'idade_meses' deve ser um número inteiro."
            )

        if peso_kg <= 0:
            raise ValueError("O campo 'peso_kg' deve ser maior que zero.")
        if valor_arroba <= 0:
            raise ValueError("O campo 'valor_arroba' deve ser maior que zero.")
        if idade_meses < 0:
            raise ValueError("O campo 'idade_meses' não pode ser negativo.")

        calculo = CalcularValorBoiService()
        preco_estimado = calculo.executar(peso_kg, valor_arroba)

        boi = Boi(
            nome=dados.get("nome") or None,
            raca=dados["raca"],
            categoria=dados["categoria"],
            peso_kg=peso_kg,
            idade_meses=idade_meses,
            valor_arroba=valor_arroba,
            preco_estimado=preco_estimado,
        )

        boi.salvar()
        return boi.to_dict()
