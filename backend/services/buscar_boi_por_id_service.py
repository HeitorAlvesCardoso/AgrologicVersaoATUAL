from models.boi_model import Boi


class BuscarBoiPorIdService:
    def executar(self, boi_id):
        boi = Boi.buscar_por_id(boi_id)

        if boi is None:
            return None

        return boi.to_dict()
