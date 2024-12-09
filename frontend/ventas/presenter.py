from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import flet as ft

from backend.data.managers.csv_manager import CSVManager
from backend.models.deudor import Deudor
from backend.models.producto import Producto
from backend.models.venta import Venta

from backend.app.routes.productos import ProductoRoutes
from backend.app.services.productos import ProductoService
from backend.app.routes.ventas import VentaRoutes
from backend.app.services.ventas import VentaService


@dataclass
class ItemVenta:
    """Clase auxiliar para representar un producto en una venta.

    Permite manejar los productos seleccionados durante el proceso de venta.

    Attributes:
        producto (Producto): El producto seleccionado.
        cantidad (int): Número de unidades del producto.

    Properties:
        total (float): Calcula el total del producto multiplicando precio por cantidad.
    """

    producto: Producto
    cantidad: int

    @property
    def total(self) -> float:
        """Calcula el total del producto.

        Returns:
            float: Precio total del producto (precio * cantidad).
        """
        return self.producto.precio * self.cantidad


class VentasPresenter:
    """Presentador para manejar la lógica de ventas.

    Responsable de gestionar la selección de productos,
    cálculo de totales y procesamiento de ventas.

    Attributes:
        view: Vista asociada al presentador.
        data_manager (CSVManager): Gestor de datos para operaciones CRUD.
        productos_venta (List[ItemVenta]): Lista de productos en la venta actual.
        productos (List[Producto]): Lista de productos disponibles.
        total_actual (float): Monto total de la venta actual.
    """

    def __init__(self, view, data_manager: CSVManager):
        """Inicializa el presentador de ventas.

        Args:
            view: La vista asociada al presentador.
            data_manager (CSVManager): Gestor de datos para operaciones de persistencia.

        Notes:
            - Carga los productos iniciales
            - Configura el diálogo de deuda
        """
        self.view = view
        self.productos_venta: List[ItemVenta] = []
        self.total_actual = 0.0

        self.venta_service = VentaService(data_manager)
        self.producto_service = ProductoService(data_manager)

        self.venta_routes = VentaRoutes(self.venta_service)
        self.producto_routes = ProductoRoutes(self.producto_service)

        self.productos = self.producto_routes.get_productos_disponibles()

        self.deudores: list[Deudor] = data_manager.get_data(Deudor)

        self.indice_deudor: Deudor | None = None

        self._init_deuda_dialog()

    def _init_deuda_dialog(self):
        """Inicializa el diálogo de gestión de deudas.

        Configura los componentes necesarios para el diálogo de deudas,
        incluyendo campos de entrada para nombre y teléfono,
        y un botón de búsqueda/adición de deudores.

        Attributes:
            busqueda_activa (bool): Indica si está en modo búsqueda o adición de deudor.
            nombre_input (ft.AutoComplete): Campo de entrada de nombre con autocompletado.
            telefono_input (ft.TextField): Campo de entrada de teléfono.
            buscar_icon (ft.IconButton): Botón para alternar modos de búsqueda/adición.
            deuda_dialog (ft.AlertDialog): Diálogo principal para gestionar deudas.

        Notes:
            - Utiliza AutoComplete para sugerencias de deudores existentes.
            - Incluye un botón para cambiar entre búsqueda y adición de nuevos deudores.
        """
        self.busqueda_activa = True

        self.nombre_input = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=deudor.nombre, value=deudor.nombre)
                for deudor in self.deudores
            ],
            on_select=lambda e: self.set_deudor_seleccionado(e.control),
        )

        self.telefono_input = ft.TextField(label='Teléfono', width=200)

        self.buscar_icon = ft.IconButton(
            ft.icons.ADD,
            width=40,
            height=40,
            on_click=self.toggle_busqueda,
        )

        self.deuda_dialog = ft.AlertDialog(
            title=ft.Text("Generar deuda"),
            content=ft.Column(
                [
                    ft.Text(
                        "El monto ingresado es insuficiente para realizar la venta."
                    ),
                    # Primera fila con el nombre_input y el botón de búsqueda
                    ft.Row(
                        [
                            ft.Column([self.nombre_input], width=200),
                            ft.Column([self.buscar_icon], width=80),
                        ],
                    ),
                    ft.Row([ft.Column([self.telefono_input], width=200)]),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Confirmar deuda", on_click=self._confirmar_deuda),
                ft.TextButton("Cancelar", on_click=lambda _: self._cerrar_dialog()),
            ],
        )

    def toggle_busqueda(self, e):
        """Alterna entre modos de búsqueda y adición de nuevo deudor.

        Cambia dinámicamente entre:
        - Modo búsqueda: Usa AutoComplete con lista de deudores existentes
        - Modo adición: Usa TextField para ingresar nuevo deudor

        Args:
            e: Evento de cambio (no utilizado directamente).

        Notes:
            - Modifica el input de nombre y el ícono del botón.
            - Actualiza el contenido del diálogo.
            - Fuerza una actualización de la página.
        """
        self.busqueda_activa = not self.busqueda_activa
        if self.busqueda_activa:
            self.nombre_input = ft.AutoComplete(
                suggestions=[
                    ft.AutoCompleteSuggestion(key=deudor.nombre, value=deudor.nombre)
                    for deudor in self.deudores
                ],
                on_select=lambda e: self.set_deudor_seleccionado(e.control),
            )
            self.buscar_icon.icon = ft.icons.ADD
        else:
            # Cambiar a agregar nuevo deudor (TextField)
            self.nombre_input = ft.TextField(label="Nombre del Deudor", width=200)
            self.buscar_icon.icon = ft.icons.SEARCH  # Cambiar el ícono a "+"

        self.deuda_dialog.content = self._get_deuda_dialog_content()
        self.view.page.update()

    def _get_deuda_dialog_content(self):
        """Establece el índice del deudor seleccionado.

        Args:
            datos_deudor (ft.AutoComplete): Control de autocompletado con el deudor seleccionado.

        Notes:
            - Imprime información de depuración.
            - Guarda el índice del deudor seleccionado.
        """
        return ft.Column(
            [
                ft.Text("El monto ingresado es insuficiente para realizar la venta."),
                # Primera fila con nombre_input y botón de búsqueda
                ft.Row(
                    [
                        ft.Column([self.nombre_input], width=200),
                        ft.Column([self.buscar_icon], width=80),
                    ],
                ),
                ft.Row([ft.Column([self.telefono_input], width=200)]),
            ],
            tight=True,
        )

    def set_deudor_seleccionado(self, datos_deudor: ft.AutoComplete):
        """
            Establece el índice del deudor seleccionado.

        Args:
            datos_deudor (ft.AutoComplete): Objeto de autocompletado con información del deudor.
        """

        print(datos_deudor)
        print(datos_deudor.data)
        self.indice_deudor = datos_deudor.selected_index

    def filtrar_productos_con_stock(self) -> List[ft.dropdown.Option]:
        """
        Crea las opciones del dropdown solo con productos que tienen stock.

        Returns:
            List[ft.dropdown.Option]: Lista de opciones de dropdown para productos con stock disponible.
        """
        return [
            ft.dropdown.Option(key=str(p.id), text=p.nombre)
            for p in self.productos
            if p.stock > 0
        ]

    def handle_producto_seleccionado(self, producto_id: str):
        """
        Maneja la selección de un producto para la venta.

        Añade el producto a la lista de productos vendidos o incrementa su cantidad.
        Verifica la disponibilidad de stock antes de agregar.

        Args:
            producto_id (str): Identificador del producto seleccionado.
        """
        if not producto_id:
            return

        producto = next((p for p in self.productos if p.id == int(producto_id)), None)
        if not producto:
            return

        # Buscar si el producto ya está en la venta
        producto_venta = next(
            (pv for pv in self.productos_venta if pv.producto.id == producto.id), None
        )

        if producto_venta:
            if producto_venta.cantidad < producto.stock:
                producto_venta.cantidad += 1
            else:
                self.view.mostrar_error(f"Stock insuficiente para {producto.nombre}")
                return
        else:
            self.productos_venta.append(ItemVenta(producto=producto, cantidad=1))

        self._actualizar_vista()

    def modificar_cantidad(self, producto_id: int, delta: int):
        """
        Modifica la cantidad de un producto en la venta.

        Incrementa o decrementa la cantidad de un producto.
        Verifica límites de stock y elimina el producto si la cantidad llega a cero.

        Args:
            producto_id (int): Identificador del producto.
            delta (int): Cambio en la cantidad (positivo o negativo).
        """

        producto_venta = next(
            (pv for pv in self.productos_venta if pv.producto.id == producto_id), None
        )

        if not producto_venta:
            return

        nueva_cantidad = producto_venta.cantidad + delta

        if delta > 0 and nueva_cantidad > producto_venta.producto.stock:
            self.view.mostrar_error(
                f"Stock insuficiente para {producto_venta.producto.nombre}"
            )
            return

        if nueva_cantidad < 1:
            self.productos_venta.remove(producto_venta)
        else:
            producto_venta.cantidad = nueva_cantidad

        self._actualizar_vista()

    def calcular_devolucion(self, monto: str):
        """
        Calcula la devolución basada en el monto ingresado.

        Args:
            monto (str): Monto pagado como cadena.

        Returns:
            float: Monto de la devolución. Retorna 0 si hay un error en la conversión.
        """
        try:
            monto_pagado = float(monto or 0)
            devolucion = monto_pagado - self.total_actual

            # Actualizar UI con el resultado
            self.view.actualizar_devolucion(devolucion)
            return devolucion
        except ValueError:
            self.view.mostrar_error("El monto debe ser un número válido")
            self.view.limpiar_formulario()
            return 0

    def _actualizar_vista(self):
        """
        Procesa una venta, ya sea completa o a crédito.

        Verifica si hay productos en la venta y si el monto pagado es suficiente.
        Si no es suficiente, muestra un diálogo para crear una deuda.

        Args:
            monto_pagado (float, optional): Monto pagado por el cliente. Defaults to 0.
        """
        # Calcular nuevo total
        self.total_actual = sum(pv.total for pv in self.productos_venta)
        self.view.actualizar_total(self.total_actual)

        # Actualizar lista de ventas
        items_venta = [
            {
                "nombre": pv.producto.nombre,
                "cantidad": pv.cantidad,
                "total": pv.total,
                "producto_id": pv.producto.id,
            }
            for pv in self.productos_venta
        ]
        self.view.venta_list.update_items(items_venta)

        # Actualizar opciones del dropdown
        self.view.actualizar_productos_disponibles(self.filtrar_productos_con_stock())

        # Forzar actualización de la página
        self.view.page.update()

    def handle_vender(self, monto_pagado: float = 0):
        """
        Procesa una venta de productos, manejando pagos completos o parciales.

        Verifica la existencia de productos en la venta y procesa el pago.
        Si el monto pagado es insuficiente, inicia el proceso de creación de deuda.

        Args:
            monto_pagado (float, optional): Monto pagado por el cliente. Defaults to 0.

        Raises:
            ValueError: Si ocurre un error de validación durante la venta.
            Exception: Si ocurre un error inesperado al procesar la venta.
        """
        if not self.productos_venta:
            self.view.mostrar_error("No hay productos en la venta")
            return

        try:
            if monto_pagado < self.total_actual:
                self._mostrar_dialog_deuda()
                return

            productos = [
                {"id_producto": item.producto.id, "cantidad": item.cantidad}
                for item in self.productos_venta
            ]

            self.venta_routes.create_venta(
                {"productos": productos, "monto_pagado": monto_pagado}
            )

            # Recargar productos para tener el stock actualizado
            self.productos = self.producto_routes.get_productos_disponibles()

            # Limpiar estado y UI
            self.productos_venta.clear()
            self._actualizar_vista()
            self.view.limpiar_formulario()
            self.view.mostrar_error("Venta registrada correctamente")

        except ValueError as e:
            self.view.mostrar_error(str(e))
        except Exception as e:
            print(e)
            self.view.mostrar_error(f"Error al procesar la venta: {str(e)}")

    def _mostrar_dialog_deuda(self):
        """
        Muestra el diálogo para crear una deuda cuando el pago es insuficiente.

        Abre el diálogo de deuda y actualiza la vista de la página.
        """
        self.view.page.dialog = self.deuda_dialog
        self.deuda_dialog.open = True
        self.view.page.update()

    def _confirmar_deuda(self, e):
        """
        Procesa la confirmación de una deuda, manejando dos escenarios:
        1. Selección de un deudor existente
        2. Creación de un nuevo deudor

        Args:
            e: Evento que desencadena la confirmación de la deuda.

        Raises:
            Exception: Si ocurre un error al registrar la venta a crédito.
        """
        if self.busqueda_activa:
            # Si es búsqueda, se usa el AutoComplete para seleccionar
            if self.indice_deudor is None:
                # Mostrar un error si no se seleccionó un deudor
                self.view.show_error("Por favor, seleccione un deudor.")
                return
            nombre_deudor = self.deudores[self.indice_deudor].nombre
            telefono_deudor = self.deudores[self.indice_deudor].telefono
        else:
            # Si no es búsqueda, se usa el TextField para agregar un nuevo deudor
            nombre_deudor = self.nombre_input.value.strip()
            telefono_deudor = self.telefono_input.value.strip()
            if not self.validar_deudor(nombre_deudor, telefono_deudor):
                return
            # Guardar nuevo deudor en el sistema
            nuevo_deudor = Deudor(id=-1, nombre=nombre_deudor, telefono=telefono_deudor)
            self.deudores.append(nuevo_deudor)
            self.view.mostrar_error(f"Nuevo deudor agregado: {nombre_deudor}")

        if not nombre_deudor:
            self.view.mostrar_error("El nombre del cliente es obligatorio")
            return

        try:
            # Preparar datos
            productos = [
                {"id_producto": item.producto.id, "cantidad": item.cantidad}
                for item in self.productos_venta
            ]

            # Crear venta a crédito
            self.venta_routes.create_venta(
                {
                    "productos": productos,
                    "monto_pagado": 0,
                    "deudor_info": {
                        "nombre": nombre_deudor,
                        "telefono": telefono_deudor,
                    },
                }
            )

            # Limpiar estado y UI
            self.productos_venta.clear()
            self._actualizar_vista()
            self.view.limpiar_formulario()
            self._cerrar_dialog()
            self.view.mostrar_error("Venta a crédito registrada correctamente")

        except Exception as e:
            self.view.mostrar_error(f"Error al registrar la venta a crédito: {str(e)}")

    def validar_deudor(self, nombre: str, telefono: str):
        """Valida los datos de un deudor antes de guardarlo.

        Args:
            nombre (str): Nombre del deudor.
            telefono (str): Teléfono del deudor.
        """
        if not nombre:
            self.view.mostrar_error("El nombre del deudor es obligatorio.")
            return False

        if len(nombre) > 50:
            self.view.mostrar_error(
                "El nombre del deudor no puede exceder los 50 caracteres."
            )
            return False

        if telefono and (not telefono.isdigit() or len(telefono) > 10):
            self.view.mostrar_error(
                "El teléfono debe ser un número de hasta 10 dígitos."
            )
            return False

        return True

    def _cerrar_dialog(self):
        """
        Cierra el diálogo de deuda actual.

        Establece el diálogo como cerrado y actualiza la vista de la página.
        """
        if self.deuda_dialog:
            self.deuda_dialog.open = False
            self.view.page.update()
