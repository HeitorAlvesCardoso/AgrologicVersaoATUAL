from models.boi_model import Boi


class DeletarBoiService:
    def executar(self, boi_id):
        boi = Boi.buscar_por_id(boi_id)

        if boi is None:
            return False

        boi.deletar()
        return True
