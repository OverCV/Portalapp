# from backend.data.managers.csv_manager import CSVManager
# from backend.models.deudor import Deudor
# from backend.models.deuda import Deuda


# class DeudoresPresenter:
#     def __init__(self, view, data_manager: CSVManager):
#         self.view = view
#         self.data_manager = data_manager

#         # Cargamos los datos iniciales
#         self.deudores = self.data_manager.get_data(Deudor)
#         self.deudas = self.data_manager.get_data(Deuda)

#     def obtener_deudores_con_deuda(self):
#         # Filtramos los deudores que tienen deudas pendientes
#         deudor_ids_con_deuda = set(deuda.id_deudor for deuda in self.deudas)
#         deudores_con_deuda = [
#             deudor for deudor in self.deudores if deudor.id in deudor_ids_con_deuda
#         ]
#         return deudores_con_deuda

#     def obtener_deudas_de_deudor(self, deudor_id):
#         # Obtenemos las deudas de un deudor específico
#         return [deuda for deuda in self.deudas if deuda.id_deudor == deudor_id]

#     def pagar_deuda(self, deuda):
#         # Lógica para pagar la deuda (por implementar)
#         # Por ahora, simplemente eliminaremos la deuda de la lista
#         self.deudas.remove(deuda)
#         # Actualizamos los datos en el CSVManager
#         self.data_manager.put_data(Deuda, self.deudas)
#         # Actualizamos la vista
#         self.view.actualizar_vista()
