# frontend\deudores\presenter.py
from backend.data.managers.csv_manager import CSVManager
from backend.models.deudor import Deudor
from backend.models.deuda import Deuda
from backend.models.abono import Abono
from datetime import datetime


class DeudoresPresenter:
    def __init__(self, view, data_manager: CSVManager):
        self.view = view
        self.data_manager = data_manager
        self.deudores = self.data_manager.get_data(Deudor)
        self.deudas = self.data_manager.get_data(Deuda)

    def obtener_deudores_con_deuda(self):
        deudores_con_deuda = {d.id_deudor for d in self.deudas}
        return [d for d in self.deudores if d.id in deudores_con_deuda]

    def total_deudas_de_deudor(self, deudor_id: int) -> int:
        deudas_de_deudor = [d for d in self.deudas if d.id_deudor == deudor_id]
        return sum(d.valor_deuda for d in deudas_de_deudor)

    def total_abonos_de_deudor(self, deudor_id: int) -> int:
        abonos = self.data_manager.get_data(Abono)
        abonos_de_deudor = [a for a in abonos if a.id_deudor == deudor_id]
        return sum(a.valor_abono for a in abonos_de_deudor)

    def saldo_de_deudor(self, deudor_id: int) -> int:
        return max(
            self.total_deudas_de_deudor(deudor_id) - self.total_abonos_de_deudor(deudor_id), 0
        )

    def registrar_abono_deudor(self, deudor_id: int, valor_abono: int):
        # Agregar un abono a nivel de deudor
        nuevo_abono = Abono(
            id=-1,
            id_deudor=deudor_id,
            valor_abono=valor_abono,
            fecha_abono=datetime.now(),
        )
        self.data_manager.add_data(nuevo_abono)
        self.view.actualizar_vista()

    def obtener_abonos_de_deudor(self, deudor_id: int):
        abonos = self.data_manager.get_data(Abono)
        return [a for a in abonos if a.id_deudor == deudor_id]

    def obtener_deudas_de_deudor(self, deudor_id: int):
        return [d for d in self.deudas if d.id_deudor == deudor_id]
