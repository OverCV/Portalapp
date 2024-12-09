# frontend\deudores\presenter.py
from backend.data.managers.csv_manager import CSVManager
from backend.models.deudor import Deudor
from backend.models.deuda import Deuda
from backend.models.abono import Abono
from datetime import datetime


class DeudoresPresenter:
    """Presentador para gestionar operaciones relacionadas con deudores y deudas.

    Esta clase actúa como intermediario entre la vista y los datos de deudores,
    proporcionando métodos para consultar y manipular información de deudas y abonos.

    Attributes:
        view: La vista asociada con el presentador.
        data_manager (CSVManager): Gestor de datos para manejar operaciones
        de lectura y escritura de datos.
        deudores (list): Lista de deudores cargados desde el gestor de datos.
        deudas (list): Lista de deudas cargadas desde el gestor de datos.
    """

    def __init__(self, view, data_manager: CSVManager):
        """Inicializa el presentador de deudores.

        Args:
            view: La vista asociada con este presentador.
            data_manager (CSVManager): Gestor de datos para manejar
            operaciones de datos.
        """
        self.view = view
        self.data_manager = data_manager
        self.deudores = self.data_manager.get_data(Deudor)
        self.deudas = self.data_manager.get_data(Deuda)

    def obtener_deudores_con_deuda(self):
        """Obtiene la lista de deudores que tienen deudas pendientes.

        Returns:
            list: Lista de deudores con al menos una deuda asociada.
        """
        deudores_con_deuda = {d.id_deudor for d in self.deudas}
        return [d for d in self.deudores if d.id in deudores_con_deuda]

    def total_deudas_de_deudor(self, deudor_id: int) -> int:
        """Calcula el total de deudas para un deudor específico.

        Args:
            deudor_id (int): Identificador único del deudor.

        Returns:
            int: Suma total de las deudas del deudor.
        """
        deudas_de_deudor = [d for d in self.deudas if d.id_deudor == deudor_id]
        return sum(d.valor_deuda for d in deudas_de_deudor)

    def total_abonos_de_deudor(self, deudor_id: int) -> int:
        """Calcula el total de abonos realizados por un deudor.

        Args:
            deudor_id (int): Identificador único del deudor.

        Returns:
            int: Suma total de los abonos del deudor.
        """
        abonos = self.data_manager.get_data(Abono)
        abonos_de_deudor = [a for a in abonos if a.id_deudor == deudor_id]
        return sum(a.valor_abono for a in abonos_de_deudor)

    def saldo_de_deudor(self, deudor_id: int) -> int:
        """Calcula el saldo pendiente de un deudor.

        Args:
            deudor_id (int): Identificador único del deudor.

        Returns:
            int: Saldo pendiente del deudor (deudas menos abonos).
            Nunca retorna valores negativos.
        """
        return max(
            self.total_deudas_de_deudor(deudor_id) - self.total_abonos_de_deudor(deudor_id), 0
        )

    def registrar_abono_deudor(self, deudor_id: int, valor_abono: int):
        """Registra un nuevo abono para un deudor.

        Args:
            deudor_id (int): Identificador único del deudor.
            valor_abono (int): Monto del abono a registrar.

        Notas:
            - Crea un nuevo registro de abono con la fecha actual.
            - Actualiza la vista después de registrar el abono.
        """
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
        """Recupera todos los abonos de un deudor específico.

        Args:
            deudor_id (int): Identificador único del deudor.

        Returns:
            list: Lista de abonos realizados por el deudor.
        """
        abonos = self.data_manager.get_data(Abono)
        return [a for a in abonos if a.id_deudor == deudor_id]

    def obtener_deudas_de_deudor(self, deudor_id: int):
        """Recupera todas las deudas de un deudor específico.

        Args:
            deudor_id (int): Identificador único del deudor.

        Returns:
            list: Lista de deudas asociadas al deudor.
        """
        return [d for d in self.deudas if d.id_deudor == deudor_id]
