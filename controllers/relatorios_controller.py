from models.relatorios_model import RelatoriosModel

class RelatorioContrroler():
    def __init__(self):
        
        self.relatorio_model = RelatoriosModel()

    def listar_relatorio(self):
        return self.relatorio_model.listar_relatórios()