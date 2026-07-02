from models.boi_model import Boi


class AtualizarBoiService:
    def executar(self, boi_id, dados):
        boi = Boi.buscar_por_id(boi_id)

        if boi is None:
            return None

        peso_kg = dados.get("peso_kg")
        if peso_kg is not None and float(peso_kg) <= 0:
            raise ValueError("O peso do boi deve ser maior que zero.")

        valor_arroba = dados.get("valor_arroba")
        if valor_arroba is not None and float(valor_arroba) <= 0:
            raise ValueError("O valor da arroba deve ser maior que zero.")

        boi.atualizar(
            raca=dados.get("raca"),
            categoria=dados.get("categoria"),
            peso_kg=peso_kg,
            idade_meses=dados.get("idade_meses"),
            valor_arroba=valor_arroba,
        )

        return boi.to_dict()
