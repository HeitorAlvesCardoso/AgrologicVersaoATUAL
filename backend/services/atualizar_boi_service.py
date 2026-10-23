from models.boi_model import Boi
from services.calcular_valor_boi_service import CalcularValorBoiService


class AtualizarBoiService:
    def executar(self, boi_id, dados):
        """Valida os campos informados e atualiza a avaliação (item 20)."""
        boi = Boi.buscar_por_id(boi_id)

        if boi is None:
            return None

        obrigatorios = ["raca", "categoria", "peso_kg", "idade_meses", "valor_arroba"]
        campos_invalidos = [
            campo for campo in obrigatorios
            if campo in dados and (
                dados.get(campo) is None or str(dados.get(campo)).strip() == ""
            )
        ]

        if campos_invalidos:
            campos = ", ".join(f"'{campo}'" for campo in campos_invalidos)
            raise ValueError(f"Os campos obrigatórios não foram preenchidos: {campos}.")

        peso_kg = dados.get("peso_kg", boi.peso_kg)
        valor_arroba = dados.get("valor_arroba", boi.valor_arroba)

        try:
            peso_kg = float(peso_kg)
            valor_arroba = float(valor_arroba)
        except (TypeError, ValueError):
            raise ValueError("Os campos 'peso_kg' e 'valor_arroba' devem ser números.")

        if "idade_meses" in dados and dados["idade_meses"] is not None:
            try:
                idade_meses = int(dados["idade_meses"])
            except (TypeError, ValueError):
                raise ValueError("O campo 'idade_meses' deve ser um número inteiro.")

            if idade_meses < 0:
                raise ValueError("O campo 'idade_meses' não pode ser negativo.")

        if peso_kg <= 0:
            raise ValueError("O campo 'peso_kg' deve ser maior que zero.")
        if valor_arroba <= 0:
            raise ValueError("O campo 'valor_arroba' deve ser maior que zero.")

        calculo = CalcularValorBoiService()
        preco_estimado = calculo.executar(peso_kg, valor_arroba)

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
