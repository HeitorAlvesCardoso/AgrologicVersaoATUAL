from models.boi_model import Boi


class CriarBoiService:
    def executar(self, dados):
        campos_obrigatorios = ["raca", "categoria", "peso_kg", "idade_meses", "valor_arroba"]

        for campo in campos_obrigatorios:
            if dados.get(campo) is None:
                raise ValueError(f"O campo '{campo}' é obrigatório.")

        peso_kg = float(dados["peso_kg"])
        valor_arroba = float(dados["valor_arroba"])

        if peso_kg <= 0:
            raise ValueError("O peso do boi deve ser maior que zero.")

        if valor_arroba <= 0:
            raise ValueError("O valor da arroba deve ser maior que zero.")

        preco_estimado = Boi.calcular_preco(peso_kg, valor_arroba)

        boi = Boi(
            raca=dados["raca"],
            categoria=dados["categoria"],
            peso_kg=peso_kg,
            idade_meses=dados["idade_meses"],
            valor_arroba=valor_arroba,
            preco_estimado=preco_estimado,
        )

        boi.salvar()
        return boi.to_dict()
