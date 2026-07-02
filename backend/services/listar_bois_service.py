from models.boi_model import Boi


class ListarBoisService:
    def executar(self):
        bois = Boi.listar_todos()
        return [boi.to_dict() for boi in bois]
